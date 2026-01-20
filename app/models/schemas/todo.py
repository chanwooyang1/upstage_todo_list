from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreateRequest(BaseModel):
    content: str


class TodoResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
