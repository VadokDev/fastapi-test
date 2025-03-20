from fastapi import APIRouter, Depends
from app.db import Task, TaskSchema
from app.auth import current_active_user, User

router = APIRouter()

@router.post("", response_model=TaskSchema)
async def create(task_data: TaskSchema, user: User = Depends(current_active_user)):
  task = Task(**task_data.model_dump())
  await task.insert()
  task_dict = task.model_dump()
  task_dict["id"] = str(task_dict.pop("id"))
  return task_dict

@router.get("")
async def getAll():
    return await Task.find().to_list()

@router.get("/{id}")
async def get(id: str):
    return await Task.get(id)

@router.put("/{id}")
async def update(id: str, task_data: TaskSchema, user: User = Depends(current_active_user)):
    task = await Task.get(id)
    await task.update({"$set": task_data.model_dump()})
    return {"message": "Task updated"}

@router.delete("/{id}")
async def delete(id: str, user: User = Depends(current_active_user)):
    task = await Task.get(id)
    await task.delete()
    return {"message": "Task deleted"}

