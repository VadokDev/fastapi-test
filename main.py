import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from fastapi import FastAPI
from mangum import Mangum
from app.db import User, Task, db
from app.auth import auth_backend, fastapi_users, UserCreate, UserRead
from app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            User,
            Task
        ],
    )
    yield


app = FastAPI(
    lifespan=lifespan, 
    title="API Tareas",
    root_path='/api',
    openapi_url='/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router, prefix="/tasks", tags=["tasks"])

handler = Mangum(app, api_gateway_base_path="/api")