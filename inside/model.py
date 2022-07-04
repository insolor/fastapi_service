from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(...)
    password: str = Field(...)


class UserLoginSchema(BaseModel):
    name: str = Field(...)
    password: str = Field(...)


class MessageSchema(BaseModel):
    name: str
    message: str


class Error(BaseModel):
    error: str
