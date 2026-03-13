from sqlmodel import Session, create_engine, select
from club_marginalistas.models import Post, Usuario, SQLModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

# --- DB ---
engine = create_engine(os.getenv("DATABASE_URL"))

# --- Supabase Auth ---
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)


def create_db():
    SQLModel.metadata.create_all(engine)


# ============================================
# AUTH
# ============================================

def auth_login(email: str, password: str) -> dict:
    """Intenta login con Supabase Auth. Retorna {"ok": True, "user": ...} o {"ok": False, "error": ...}"""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"ok": True, "user": res.user}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def auth_logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass


def get_usuario_by_email(email: str) -> Usuario | None:
    with Session(engine) as session:
        return session.exec(select(Usuario).where(Usuario.email == email)).first()


def create_usuario(usuario: Usuario) -> Usuario:
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario


def delete_usuario(email: str):
    with Session(engine) as session:
        u = session.exec(select(Usuario).where(Usuario.email == email)).first()
        if u:
            session.delete(u)
            session.commit()


def get_all_usuarios() -> list[Usuario]:
    with Session(engine) as session:
        return list(session.exec(select(Usuario)).all())


# ============================================
# POSTS
# ============================================

def get_all_posts(status: str = "published") -> list[Post]:
    with Session(engine) as session:
        return list(session.exec(
            select(Post)
            .where(Post.status == status)
            .order_by(Post.date.desc())
        ).all())


def get_pending_posts() -> list[Post]:
    return get_all_posts(status="pending")


def get_all_posts_admin() -> list[Post]:
    """Todos los posts sin filtrar por status, para el panel admin."""
    with Session(engine) as session:
        return list(session.exec(select(Post).order_by(Post.date.desc())).all())


def get_post_by_slug(slug: str) -> Post | None:
    with Session(engine) as session:
        return session.exec(select(Post).where(Post.slug == slug)).first()


def create_post(post: Post) -> Post:
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


def update_post_status(slug: str, status: str):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.slug == slug)).first()
        if post:
            post.status = status
            session.add(post)
            session.commit()


def delete_post(slug: str):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.slug == slug)).first()
        if post:
            session.delete(post)
            session.commit()