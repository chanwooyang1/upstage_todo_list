from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository
from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends

def get_todo_repository(db: Session = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)

def get_todo_service(todo_repo: TodoRepository = Depends(get_todo_repository)) -> TodoService:
    return TodoService(todo_repo)