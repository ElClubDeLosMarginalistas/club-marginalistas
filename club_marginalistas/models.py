from dataclasses import dataclass
from datetime import date


@dataclass
class Post:
    slug: str
    title: str
    description: str
    author: str
    date: str
    image: str
    category: str
    content: str