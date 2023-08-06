import typing
from datetime import date, datetime
from inspect import getdoc
from itertools import count
from typing import List, Type
from uuid import UUID

from aiohttp.web import Response, json_response
from aiohttp.web_app import Application

from aiohttp_pydantic.oas.struct import OpenApiSpec3, OperationObject, PathItem

from ..injectors import _parse_func_signature
from ..utils import is_pydantic_base_model
from ..view import PydanticView, is_pydantic_view
from .typing import is_status_code_type

JSON_SCHEMA_TYPES = {
    float: {"type": "number"},
    str: {"type": "string"},
    int: {"type": "integer"},
    UUID: {"type": "string", "format": "uuid"},
    bool: {"type": "boolean"},
    datetime: {"type": "string", "format": "date-time"},
    date: {"type": "string", "format": "date"},
}


def _handle_optional(type_):
    """
    Returns the type wrapped in Optional or None.

    >>>  _handle_optional(int)
    >>>  _handle_optional(Optional[str])
    <class 'str'>
    """
    if typing.get_origin(type_) is typing.Union:
        args = typing.get_args(type_)
        if len(args) == 2 and type(None) in args:
            return next(iter(set(args) - {type(None)}))
    return None


class _OASResponseBuilder:
    """
    Parse the type annotated as returned by a function and
    generate the OAS operation response.
    """

    def __init__(self, oas_operation):
        self._oas_operation = oas_operation

    @staticmethod
    def _handle_pydantic_base_model(obj):
        if is_pydantic_base_model(obj):
            return obj.schema()
        return {}

    def _handle_list(self, obj):
        if typing.get_origin(obj) is list:
            return {
                "type": "array",
                "items": self._handle_pydantic_base_model(typing.get_args(obj)[0]),
            }
        return self._handle_pydantic_base_model(obj)

    def _handle_status_code_type(self, obj):
        if is_status_code_type(typing.get_origin(obj)):
            status_code = typing.get_origin(obj).__name__[1:]
            self._oas_operation.responses[status_code].content = {
                "application/json": {
                    "schema": self._handle_list(typing.get_args(obj)[0])
                }
            }

        elif is_status_code_type(obj):
            status_code = obj.__name__[1:]
            self._oas_operation.responses[status_code].content = {}

    def _handle_union(self, obj):
        if typing.get_origin(obj) is typing.Union:
            for arg in typing.get_args(obj):
                self._handle_status_code_type(arg)
        self._handle_status_code_type(obj)

    def build(self, obj):
        self._handle_union(obj)


def _add_http_method_to_oas(
    oas_path: PathItem, http_method: str, view: Type[PydanticView]
):
    http_method = http_method.lower()
    oas_operation: OperationObject = getattr(oas_path, http_method)
    handler = getattr(view, http_method)
    path_args, body_args, qs_args, header_args = _parse_func_signature(handler)
    description = getdoc(handler)
    if description:
        oas_operation.description = description

    if body_args:
        oas_operation.request_body.content = {
            "application/json": {"schema": next(iter(body_args.values())).schema()}
        }

    indexes = count()
    for args_location, args in (
        ("path", path_args.items()),
        ("query", qs_args.items()),
        ("header", header_args.items()),
    ):
        for name, type_ in args:
            i = next(indexes)
            oas_operation.parameters[i].in_ = args_location
            oas_operation.parameters[i].name = name
            optional_type = _handle_optional(type_)
            if optional_type is None:
                oas_operation.parameters[i].schema = JSON_SCHEMA_TYPES[type_]
                oas_operation.parameters[i].required = True
            else:
                oas_operation.parameters[i].schema = JSON_SCHEMA_TYPES[optional_type]
                oas_operation.parameters[i].required = False

    return_type = handler.__annotations__.get("return")
    if return_type is not None:
        _OASResponseBuilder(oas_operation).build(return_type)


def generate_oas(apps: List[Application]) -> dict:
    """
    Generate and return Open Api Specification from PydanticView in application.
    """
    oas = OpenApiSpec3()
    for app in apps:
        for resources in app.router.resources():
            for resource_route in resources:
                if is_pydantic_view(resource_route.handler):
                    view: Type[PydanticView] = resource_route.handler
                    info = resource_route.get_info()
                    path = oas.paths[info.get("path", info.get("formatter"))]
                    if resource_route.method == "*":
                        for method_name in view.allowed_methods:
                            _add_http_method_to_oas(path, method_name, view)
                    else:
                        _add_http_method_to_oas(path, resource_route.method, view)

    return oas.spec


async def get_oas(request):
    """
    View to generate the Open Api Specification from PydanticView in application.
    """
    apps = request.app["apps to expose"]
    return json_response(generate_oas(apps))


async def oas_ui(request):
    """
    View to serve the swagger-ui to read open api specification of application.
    """
    template = request.app["index template"]

    static_url = request.app.router["static"].url_for(filename="")
    spec_url = request.app.router["spec"].url_for()
    host = request.url.origin()

    return Response(
        text=template.render(
            {
                "openapi_spec_url": host.with_path(str(spec_url)),
                "static_url": host.with_path(str(static_url)),
            }
        ),
        content_type="text/html",
        charset="utf-8",
    )
