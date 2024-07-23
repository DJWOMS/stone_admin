from pathlib import Path
from typing import Optional, Annotated, Sequence, List

from esmerald import ChildEsmerald, Esmerald, Extension, Include
from esmerald.config.template import TemplateConfig
from esmerald.template.jinja import JinjaTemplateEngine

from esmerald.types import DictAny
from typing_extensions import Doc

from config import StoneSettings
from middleware.jwt import JWTAuthMiddleware


class StoneAdminExtension(Extension):
    def __init__(self, app: Optional["Esmerald"] = None, **kwargs: "DictAny"):
        super().__init__(app, **kwargs)
        self.app = app
        self.kwargs = kwargs

    def extend(
            self,
            admin: "BaseAdmin",
            title: str = "Stone Admin",
            path: Annotated[
                Optional[str],
                Doc(
                    """
                    Relative path of the Plugable.
                    The path can contain parameters in a dictionary like format
                    and if the path is not provided, it will default to `/`.
        
                    **Example**
        
                    ```python
                    Pluugable(SimpleJWTExtension, path="/{age: int}"))
                    ```
                    """
                ),
            ] = "/admin",
            route_name: str = "admin",
            name: Annotated[
                Optional[str],
                Doc(
                    """
                    The name for the Gateway. The name can be reversed by `url_path_for()`.
                    """
                ),
            ] = None,
            logo_url: Optional[str] = None,
            login_logo_url: Optional[str] = None,
            templates_dir: str = "templates",
            statics_dir: Optional[str] = None,
            # index_view: Optional[CustomView] = None,
            # auth_provider: Optional[BaseAuthProvider] = None,
            debug: bool = False,
            favicon_url: Optional[str] = None,

            settings_module: Annotated[
                Optional["SettingsType"],
                Doc(
                    """
                    Alternative settings parameter. This parameter is an alternative to
                    `ESMERALD_SETTINGS_MODULE` way of loading your settings into an Esmerald application.

                    When the `settings_module` is provided, it will make sure it takes priority over
                    any other settings provided for the instance.

                    Read more about the [settings module](https://esmerald.dev/application/settings/)
                    and how you can leverage it in your application.

                    !!! Tip
                        The settings module can be very useful if you want to have, for example, a
                        [ChildEsmerald](https://esmerald.dev/routing/router/?h=childe#child-esmerald-application) that needs completely different settings
                        from the main app.

                        Example: A `ChildEsmerald` that takes care of the authentication into a cloud
                        provider such as AWS and handles the `boto3` module.
                    """
                ),
            ] = StoneSettings,
            middleware: Annotated[
                Optional[Sequence["Middleware"]],
                Doc(
                    """
                    A list of middleware to run for every request. The middlewares of a Gateway will be checked from top-down or [Starlette Middleware](https://www.starlette.io/middleware/) as they are both converted internally. Read more about [Python Protocols](https://peps.python.org/pep-0544/).
                    """
                ),
            ] = None,
            jwt_middleware: Annotated[
                Optional[Sequence["Middleware"]],
                Doc(
                    """
                    A list of middleware to run for every JWT request.
                    """
                ),
            ] = JWTAuthMiddleware,
            dependencies: Annotated[
                Optional["Dependencies"],
                Doc(
                    """
                    A dictionary of string and [Inject](https://esmerald.dev/dependencies/) instances enable application level dependency injection.
                    """
                ),
            ] = None,
            exception_handlers: Annotated[
                Optional["ExceptionHandlerMap"],
                Doc(
                    """
                    A dictionary of [exception types](https://esmerald.dev/exceptions/) (or custom exceptions) and the handler functions on an application top level. Exception handler callables should be of the form of `handler(request, exc) -> response` and may be be either standard functions, or async functions.
                    """
                ),
            ] = None,
            interceptors: Annotated[
                Optional[List["Interceptor"]],
                Doc(
                    """
                    A list of [interceptors](https://esmerald.dev/interceptors/) to serve the application incoming requests (HTTP and Websockets).
                    """
                ),
            ] = None,
            permissions: Annotated[
                Optional[List["Permission"]],
                Doc(
                    """
                    A list of [permissions](https://esmerald.dev/permissions/) to serve the application incoming requests (HTTP and Websockets).
                    """
                ),
            ] = None,
            include_in_schema: Annotated[
                Optional[bool],
                Doc(
                    """
                    Boolean flag indicating if it should be added to the OpenAPI docs.
                    """
                ),
            ] = True,
            enable_openapi: Annotated[
                Optional[bool],
                Doc(
                    """
                    Boolean flag indicating if the OpenAPI documentation should
                    be generated or not.

                    When `False`, no OpenAPI documentation is accessible.

                    !!! Tip
                        Disable this option if you run in production and no one should access the
                        documentation unless behind an authentication.
                    ```
                    """
                ),
            ] = True,
    ) -> None:
        """
        Add a child Esmerald into the main application.
        """
        admin.init_routes()
        template_config = TemplateConfig(
            directory=Path("templates"),
            engine=JinjaTemplateEngine,
        )
        stone_admin = ChildEsmerald(
            title=title,
            routes=[
                Include(path="/", routes=[*admin.routes], middleware=[jwt_middleware]),
                Include(path="/auth", namespace="esmerald_simple_jwt.urls"),
            ],
            middleware=middleware,
            dependencies=dependencies,
            exception_handlers=exception_handlers,
            interceptors=interceptors,
            permissions=permissions,
            include_in_schema=include_in_schema,
            enable_openapi=enable_openapi,
            settings_module=settings_module,
            template_config=template_config,
            debug=True
        )
        self.app.add_child_esmerald(name=name, path=path, child=stone_admin)
