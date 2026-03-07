from sqlmodel import Session, create_engine, select
from club_marginalistas.models import Post, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_all_posts() -> list[Post]:
    with Session(engine) as session:
        posts = session.exec(
            select(Post).order_by(Post.date.desc())
        ).all()
        return list(posts)


def get_post_by_slug(slug: str) -> Post | None:
    with Session(engine) as session:
        post = session.exec(
            select(Post).where(Post.slug == slug)
        ).first()
        return post


def create_post(post: Post) -> Post:
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


def delete_post(slug: str):
    with Session(engine) as session:
        post = session.exec(
            select(Post).where(Post.slug == slug)
        ).first()
        if post:
            session.delete(post)
            session.commit()