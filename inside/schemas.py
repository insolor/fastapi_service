from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class Message(BaseModel):
    user_id: int
    message: str

    class Config:
        orm_mode = True


class Error(BaseModel):
    error: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Message] = []

    class Config:
        orm_mode = True
