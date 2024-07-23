from typing import Optional

from esmerald import Gateway


class StoneAdmin:
    """Base class for implementing Admin interface."""

    def __init__(
            self,
            title: str = "Stone Admin",
            base_url: str = "/admin",
            route_name: str = "admin",
            logo_url: Optional[str] = None,
            login_logo_url: Optional[str] = None,
            templates_dir: str = "templates",
            statics_dir: Optional[str] = None,
            # index_view: Optional[CustomView] = None,
            # auth_provider: Optional[BaseAuthProvider] = None,
            # middlewares: Optional[Sequence[Middleware]] = None,
            debug: bool = False,
            favicon_url: Optional[str] = None,
    ):
        self.title = title
        self.base_url = base_url
        self.route_name = route_name
        self.logo_url = logo_url
        self.login_logo_url = login_logo_url
        self.templates_dir = templates_dir
        self.statics_dir = statics_dir
        # self.index_view = index_view
        # self.auth_provider = auth_provider
        # self.middlewares = middlewares
        self.debug = debug
        self.favicon_url = favicon_url
        self._views = []
        self.routes = []

    def add_view(self, view) -> None:
        """
        Add View to the Admin interface.
        """
        view_instance = view  # if isinstance(view, BaseModelAdmin)  else view()
        # view_instance.redirect_path = f"{self.base_url}/{view_instance.path}"
        self._views.append(view_instance)

    def init_routes(self):
        for view in self._views:
            self.routes.append(Gateway(handler=view.controller))
