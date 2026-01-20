from fastapi import FastAPI
from app.routers.todo_router import router as todo_router

app = FastAPI(title="Todo API", version="1.0.0")
app.include_router(todo_router)
