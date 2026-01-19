from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.core.db import get_db





router = APIRouter(prefix = "todos", tags=["todos"])

# @router.get("/")
# async def create_todo(db: Session = Depends(get_db)):
#     todo_service =
#     return

