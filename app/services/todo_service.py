from sqlalchemy.orm import Session
from app.repositories.todo_repository import TodoRepository
from app.schemas import TodoCreate
class TodoService:
    def __init__(self, db: Session):
        self.repository = TodoRepository(db)

    def get_todos(self):
        return self.repository.get_todos()

    def create_todo(self, payload: TodoCreate):
        return self.repository.create_todo(payload)

    def delete_todo(self, todo_id: int):
        return self.repository.delete_todo(todo_id)
