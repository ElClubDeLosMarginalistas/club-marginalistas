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


class Colaborador(SQLModel, table=True):
    id:          Optional[int] = Field(default=None, primary_key=True)
    slug:        str = Field(unique=True, index=True)
    email:       str = Field(unique=True, index=True)  

    # Datos básicos
    name:        str
    initials:    str
    role:        str = ""   # título/rol ej: "Economista · Analista de Datos"
    bio:         str = ""   # resumen profesional

    # Perfil profesional (JSON como string)
    education:   str = "[]"  
    experience:  str = "[]"   

    # Skills e idiomas (separado por comas)
    skills:      str = ""   # "Python,SQL,Power BI,Excel"
    languages:   str = ""   # "Español (Nativo),Inglés (C1)"

    # Redes sociales (todas opcionales)
    linkedin:    str = ""
    github:      str = ""
    twitter:     str = ""
    instagram:   str = ""
    youtube:     str = ""
    email_public: str = "" 

    order:       int = 0    # orden de aparición en la página