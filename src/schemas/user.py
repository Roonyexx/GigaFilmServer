from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    username: str
    password: str

class userLogin(UserCreateSchema):
    pass

class UserSchema(UserCreateSchema):
    id: str

class UserWithToken(BaseModel):
    username: str
    token: str

