import os
import motor.motor_asyncio
from beanie import Document
from pydantic import BaseModel

from beanie import Document
from fastapi_users.db import BeanieBaseUser
from fastapi_users_db_beanie import BeanieUserDatabase

DATABASE_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["tareas_db"]

class User(BeanieBaseUser, Document):
    pass

class Task(Document):
    name: str
    status: str

class TaskSchema(BaseModel):
    id: str = None
    name: str
    status: str

async def get_user_db():
    yield BeanieUserDatabase(User)