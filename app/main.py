from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.database import Base, engine, get_db


# Crear las tablas en la base de datos
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(on_startup=[init_db])


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)


@app.post("/chats/", response_model=schemas.Chat)
async def start_chat(chat: schemas.ChatCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_chat(db, chat)


@app.get("/chats/{user_id}", response_model=List[schemas.Chat])
async def get_user_chats(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_chats(db, user_id)


@app.get("/messages/{chat_id}", response_model=List[schemas.Message])
async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_chat_messages(db, chat_id)


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await crud.create_message(db, schemas.MessageCreate(sender="user", message=data), chat_id=user_id)
            bot_reply = f"Bot: You said '{data}'"
            await crud.create_message(db, schemas.MessageCreate(sender="bot", message=bot_reply), chat_id=user_id)
            await websocket.send_text(bot_reply)
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
