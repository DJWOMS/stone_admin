from typing import cast, List, Type

from edgy import Model
from esmerald import Redirect, post, Inject, Form, Template, get, APIView, delete, put
from esmerald.openapi.datastructures import OpenAPIResponse
from esmerald.openapi.security.http import Bearer
from esmerald.types import View
from lilya import status
from pydantic import BaseModel

from contrib.auth.permissions import IsUserAdmin
from services.abstract import BaseService


def create_controller_class(
        path_for_controller: str,
        # redirect_path: str,
        schema_input: BaseModel,
        schema_update: BaseModel,
        object_name: str,
        list_object_name: str,
        template_form_create: str,
        template_list: str,
        template_detail: str,
        template_form_update: str,
        template_delete: str,
        base_service: BaseService,
        form: BaseModel,
) -> Type[View]:
    """ Create a controller class """
    class DynamicAdminController(View):
        path = path_for_controller
        dependencies = {
            "service": Inject(base_service),
        }

        @post('/create', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        async def create(
                self,
                service: base_service,
                data: schema_input = Form()
        ) -> Redirect:
            await service.create(data)
            return Redirect(path=path_for_controller)

        @get('/create')
        async def get_form(self) -> Template:
            return Template(name=template_form_create, context={"form": form()})

        @get('/')
        async def list(self, service: base_service) -> Template:
            query = await service.list()
            return Template(name=template_list, context={list_object_name: query})

        @get('/{pk:int}')
        async def detail(self, pk: int, service: base_service) -> Template:
            query = await service.detail(pk)
            return Template(name=template_detail, context={object_name: query})

        @get('/update/{pk:int}')
        async def get_form_update(self, pk: int, service: base_service) -> Template:
            query = await service.detail(pk)
            return Template(name=template_form_update, context={object_name: query})

        @post('/update/{pk:int}', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        async def update(
                self,
                pk: int,
                service: base_service,
                data: schema_update = Form()
        ) -> Redirect:
            await service.update(pk, data)
            return Redirect(path=path_for_controller)

        @get('/delete/{pk:int}')
        async def get_form_delete(self, pk: int, service: base_service) -> Template:
            await service.detail(pk)
            return Template(name=template_delete)

        @post('/delete/{pk:int}', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        async def delete(self, pk: int, service: base_service) -> Redirect:
            await service.delete(pk)
            return Redirect(path=path_for_controller)

    return DynamicAdminController


def create_api_controller_class(
        path_for_controller: str,
        schema_input: BaseModel,
        schema_update: BaseModel,
        schema_output: BaseModel,
        base_service: BaseService,
) -> Type[APIView]:
    """ Create a api controller class """
    class DynamicAdminAPIController(APIView):
        path = path_for_controller
        security = [Bearer]
        permissions = [IsUserAdmin]
        dependencies = {
            "service": Inject(base_service),
        }

        @post(responses={201: OpenAPIResponse(model=schema_output)})
        async def create(self, data: schema_input, service: base_service) -> schema_output:
            return await service.create(data)

        @get('/', responses={200: OpenAPIResponse(model=[schema_output])})
        async def list(self, service: base_service) -> List[schema_output]:
            return await service.list()

        @get('/{pk:int}', responses={200: OpenAPIResponse(model=schema_output)})
        async def detail(self, pk: int, service: base_service) -> schema_output:
            return await service.detail(pk)

        @put('/{pk:int}', responses={201: OpenAPIResponse(model=schema_output)})
        async def update(
                self,
                pk: int,
                service: base_service,
                data: schema_update
        ) -> schema_output:
            return await service.update(pk, data)

        @delete('/{pk:int}', status_code=status.HTTP_204_NO_CONTENT)
        async def delete(self, pk: int, service: base_service) -> None:
            return await service.delete(pk)

    return DynamicAdminAPIController


def create_service_class(
        edgy_model: Model,
        schema_input: BaseModel,
        schema_update: BaseModel,
        schema_out: BaseModel
) -> Type["DynamicAdminService"]:
    """ Create a service class """
    class DynamicAdminService:
        model = edgy_model

        async def create(self, data: schema_input) -> None:
            return await self.model.query.create(**data.model_dump())

        async def delete(self, pk) -> None:
            return await self.model.query.filter(id=pk).delete()

        async def update(self, pk, data: schema_update) -> None:
            return await self.model.query.filter(id=pk).update(**data.model_dump())

        async def list(self) -> list[schema_out]:
            return await self.model.query.all()

        async def detail(self, pk: int) -> schema_out:
            return await self.model.query.get(id=pk)

    return DynamicAdminService
