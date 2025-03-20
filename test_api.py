
from fastapi.testclient import TestClient
from main import app
from app.auth import current_active_user
from unittest.mock import patch

client = TestClient(app)

def mock_user():
    return {
        "id": "sedfgm",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedpassword",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    }


@patch("app.api.Task", autospec=True)
def test_create_task(mock_task):
  app.dependency_overrides[current_active_user] = mock_user

  mock_task.return_value = mock_task
  mock_task.model_dump.return_value.id = "id"
  mock_task.model_dump.return_value.name = "Test Task"
  mock_task.model_dump.return_value.status = "Pending"

  headers = {"Authorization": "Bearer testtoken"}
  response = client.post("/tasks", json={"name": "Task", "status": "Pending"}, headers=headers)

  assert response.status_code == 200
  assert response.json() == {"id": "id", "name": "Test Task", "status": "Pending"}

@patch("app.api.Task", autospec=True)
def test_get_all_tasks(mock_task):
  app.dependency_overrides[current_active_user] = mock_user

  async def mock_find():
    return [
      {"name": "Test Task 1", "status": "Pending"},
      {"name": "Test Task 2", "status": "Completed"},
    ]

  mock_task.find.return_value.to_list = mock_find

  headers = {"Authorization": "Bearer testtoken"}
  response = client.get("/tasks", headers=headers)

  assert response.status_code == 200
  assert response.json() == [
    {"name": "Test Task 1", "status": "Pending"},
    {"name": "Test Task 2", "status": "Completed"},
  ]


@patch("app.api.Task", autospec=True)
def test_get_task_by_id(mock_task):
  app.dependency_overrides[current_active_user] = mock_user

  mock_task.get.return_value = {"name": "Test Task", "status": "Pending"}

  headers = {"Authorization": "Bearer testtoken"}
  response = client.get("/tasks/some-task-id", headers=headers)

  assert response.status_code == 200
  assert response.json() == {"name": "Test Task", "status": "Pending"}


@patch("app.api.Task", autospec=True)
def test_update_task(mock_task):
  app.dependency_overrides[current_active_user] = mock_user

  mock_task.get.return_value = mock_task
  mock_task.update.return_value = None
  mock_task.name = "Updated Task"
  mock_task.status = "Completed"

  headers = {"Authorization": "Bearer testtoken"}
  response = client.put("/tasks/some-task-id", json={"name": "Updated Task", "status": "Completed"}, headers=headers)

  assert response.status_code == 200
  assert response.json() == {"message": "Task updated"}


@patch("app.api.Task", autospec=True)
def test_delete_task(mock_task):
  app.dependency_overrides[current_active_user] = mock_user

  mock_task.get.return_value = mock_task
  mock_task.delete.return_value = None

  headers = {"Authorization": "Bearer testtoken"}
  response = client.delete("/tasks/some-task-id", headers=headers)

  assert response.status_code == 200
  assert response.json() == {"message": "Task deleted"}
