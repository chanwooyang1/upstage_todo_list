from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.todo_service import TodoService
from app import schemas




router = APIRouter(prefix = "todos", tags=["todos"])

def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(db)

@router.post("/")
async def create_todo(payload: schemas.TodoCreate, service: TodoService = Depends(get_todo_service)):
    return service.create_todo(payload)

@router.get("/")
async def get_todos(service : TodoService = Depends(get_todo_service)) :
    return service.get_todos()


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    return service.delete_todo(todo_id)

