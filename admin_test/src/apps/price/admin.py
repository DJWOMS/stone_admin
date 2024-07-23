from pydantic import BaseModel

from core import BaseAdmin


class PriceInput(BaseModel):
    name: str
    description: str
    is_active: bool


class PriceOutput(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool


class PriceAdmin(BaseAdmin):
    schema_input = PriceInput
    schema_output = PriceOutput
    schema_update = PriceInput
