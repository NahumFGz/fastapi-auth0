from typing import List

from pydantic import BaseModel


class MessageBase(BaseModel):
    sender: str
    message: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int

    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    user_id: int
    bot_id: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    messages: List[Message] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    chats: List[Chat] = []

    class Config:
        orm_mode = True
