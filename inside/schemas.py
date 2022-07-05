from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class MessageBase(BaseModel):
    message: str


class Message(MessageBase):
    name: str

    class Config:
        orm_mode = True


class Result(BaseModel):
    message: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[MessageBase] = []

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    token: str
