from sqlmodel import SQLModel, Field
from typing import Optional


class Post(SQLModel, table=True):
    id:          Optional[int] = Field(default=None, primary_key=True)
    slug:        str = Field(unique=True, index=True)
    title:       str
    description: str
    author:      str
    date:        str
    image:       str = ""
    category:    str = "General"
    content:     str
    status:      str = "published"  # draft | pending | published


class Usuario(SQLModel, table=True):
    id:    Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    role:  str = "colaborador"  # admin | colaborador
    name:  str = ""