from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_chat(db: AsyncSession, chat: schemas.ChatCreate):
    db_chat = models.Chat(**chat.dict())
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat


async def create_message(db: AsyncSession, message: schemas.MessageCreate, chat_id: int):
    db_message = models.Message(chat_id=chat_id, **message.dict())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


async def get_user_chats(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Chat).filter(models.Chat.user_id == user_id))
    return result.scalars().all()


async def get_chat_messages(db: AsyncSession, chat_id: int):
    result = await db.execute(select(models.Message).filter(models.Message.chat_id == chat_id))
    return result.scalars().all()
