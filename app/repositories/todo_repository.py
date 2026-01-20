from sqlalchemy.orm import Session
from app.models.entities.todos import Todo
from app.models.schemas.todo import TodoCreateRequest

class TodoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_todos(self):
        """모든 Todo 항목 조회"""
        return self.db.query(Todo).order_by(Todo.id.desc()).all()

    def create_todo(self, payload: TodoCreateRequest) -> Todo:
        """새로운 Todo 항목 생성"""
        todo = Todo(content=payload.content)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def get_todo_by_id(self, todo_id: int) -> Todo:
        """ID로 Todo 항목 조회"""
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def delete_todo(self, todo_id: int) -> bool:
        """Todo 항목 삭제"""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            self.db.delete(todo)
            self.db.commit()
            return True
        return False

