from typing import Protocol, TYPE_CHECKING, Type

if TYPE_CHECKING:  # pragma: no cover
    from edgy import Model
    from pydantic import BaseModel


class BaseWriteService(Protocol):
    model: Type["Model"]

    async def create(self, data: "BaseModel") -> None:
        raise NotImplementedError

    async def delete(self, pk: int) -> None:
        ...

    async def update(self, pk: int, data: "BaseModel") -> None:
        ...


class BaseReadService(Protocol):
    model: Type["Model"]

    async def list(self) -> list["BaseModel"]:
        ...

    async def detail(self, pk: int) -> "BaseModel":
        ...


class BaseService(Protocol):
    model: Type["Model"]

    async def create(self, data: "BaseModel") -> None:
        ...

    async def delete(self, pk: int) -> None:
        ...

    async def update(self, pk: int, data: "BaseModel") -> None:
        ...

    async def list(self) -> list["BaseModel"]:
        ...

    async def detail(self, pk: int) -> "BaseModel":
        ...
