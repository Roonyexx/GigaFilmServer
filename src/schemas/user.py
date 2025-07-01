from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    username: str
    password: str

class UserSchema(UserCreateSchema):
    id: str