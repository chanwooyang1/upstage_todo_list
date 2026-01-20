from app.repositories.todo_repository import TodoRepository
from app.models.schemas.todo import TodoCreateRequest


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def get_todos(self):
        return self.repository.get_todos()

    def create_todo(self, payload: TodoCreateRequest):
        return self.repository.create_todo(payload)

    def delete_todo(self, todo_id: int):
        return self.repository.delete_todo(todo_id)
