from pydantic import BaseModel

from core import BaseAdmin


class UserIn(BaseModel):
    name: str
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str
    first_name: str
    last_name: str
    username: str


class UserOut(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    username: str
    email: str


class UserForm(BaseModel):
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserAdmin(BaseAdmin):
    schema_input = UserIn
    schema_output = UserOut
    schema_update = UserUpdate
