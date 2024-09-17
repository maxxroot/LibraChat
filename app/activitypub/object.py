from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List

class Object(BaseModel):
    id: HttpUrl
    type: str
    attributedTo: Optional[HttpUrl] = None
    content: Optional[str] = None
    published: Optional[datetime] = None
    to: Optional[List[HttpUrl]] = None
    cc: Optional[List[HttpUrl]] = None

class Note(Object):
    type: str = "Note"

class Article(Object):
    type: str = "Article"
