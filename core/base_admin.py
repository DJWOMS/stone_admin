from typing import Type, TYPE_CHECKING

from esmerald.types import View
from lilya.exceptions import ImproperlyConfigured
from pydantic import BaseModel

from .factory import create_service_class, create_api_controller_class


if TYPE_CHECKING:
    from ..services import BaseService


class BaseAdmin:
    controller: View | None = None
    service: Type["BaseService"] | None = None
    path: str | None = None
    enable_openapi: bool = True
    schema_input: Type[BaseModel] | None = None
    schema_output: Type[BaseModel] | None = None
    schema_update: Type[BaseModel] | None = None
    form: Type[BaseModel] | None = None
    object_name: str | None = None
    list_object_name: str | None = None

    def __init__(self, model):
        self.model = model
        self.path = f"/{self.model.__name__.lower()}s/"
        self.list_object_name = f"{self.model.__name__.lower()}s"
        self.object_name = self.model.__name__.lower()
        self.generate_service()
        self.generate_controller()

    def generate_service(self) -> None:
        if self.service is None:
            self.service = create_service_class(
                self.model,
                self.schema_input,
                self.schema_update,
                self.schema_output
            )

    def generate_controller(self) -> None:
        if self.controller is None and self.enable_openapi:
            self.controller = create_api_controller_class(
                path_for_controller=self.path,
                schema_input=self.schema_input,
                schema_update=self.schema_update,
                schema_output=self.schema_output,
                base_service=self.service,
            )
