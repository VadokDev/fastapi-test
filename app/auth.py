
import os 
from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, schemas
from fastapi_users.authentication import ( AuthenticationBackend, BearerTransport, JWTStrategy)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from app.db import User, get_user_db

JWT_SECRET = os.getenv("JWT_SECRET")

class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    pass

async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)