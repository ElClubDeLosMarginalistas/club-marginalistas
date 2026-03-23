from sqlmodel import Session, create_engine, select
from club_marginalistas.models import Post, Usuario, Colaborador, SQLModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

# --- Supabase Auth (cliente público) ---
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

# --- Supabase Admin (service role — solo para operaciones de backend) ---
supabase_admin: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY"),
)


def create_db():
    SQLModel.metadata.create_all(engine)


# ============================================
# AUTH
# ============================================

def auth_login(email: str, password: str) -> dict:
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


def get_all_usuarios() -> list[Usuario]:
    with Session(engine) as session:
        return list(session.exec(select(Usuario)).all())


def delete_usuario(email: str):
    with Session(engine) as session:
        u = session.exec(select(Usuario).where(Usuario.email == email)).first()
        if u:
            session.delete(u)
            session.commit()


# ============================================
# POSTS
# ============================================

def get_all_posts(status: str = "published") -> list[Post]:
    with Session(engine) as session:
        return list(session.exec(
            select(Post).where(Post.status == status).order_by(Post.date.desc())
        ).all())


def get_pending_posts() -> list[Post]:
    return get_all_posts(status="pending")


def get_all_posts_admin() -> list[Post]:
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


def get_posts_by_author(author_name: str) -> list[Post]:
    with Session(engine) as session:
        return list(session.exec(
            select(Post)
            .where(Post.author == author_name)
            .where(Post.status == "published")
            .order_by(Post.date.desc())
        ).all())


# ============================================
# COLABORADORES
# ============================================

def get_all_colaboradores() -> list[Colaborador]:
    with Session(engine) as session:
        return list(session.exec(
            select(Colaborador).order_by(Colaborador.order)
        ).all())


def get_colaborador_by_slug(slug: str) -> Colaborador | None:
    with Session(engine) as session:
        return session.exec(select(Colaborador).where(Colaborador.slug == slug)).first()


def create_colaborador_completo(colaborador: Colaborador, password: str) -> dict:
    """
    Crea el colaborador completo:
    1. Crea usuario en Supabase Auth
    2. Crea registro en tabla usuario
    3. Crea registro en tabla colaborador
    """
    # 1. Crear en Supabase Auth con cliente admin
    try:
        supabase_admin.auth.admin.create_user({
            "email": colaborador.email,
            "password": password,
            "email_confirm": True,
        })
    except Exception as e:
        return {"ok": False, "error": f"Error en Supabase Auth: {str(e)}"}

    # 2. Crear en tabla usuario
    with Session(engine) as session:
        usuario = Usuario(email=colaborador.email, name=colaborador.name, role="colaborador")
        session.add(usuario)
        session.commit()

    # 3. Crear en tabla colaborador
    with Session(engine) as session:
        session.add(colaborador)
        session.commit()
        session.refresh(colaborador)

    return {"ok": True}


def delete_colaborador(slug: str):
    """Elimina colaborador, su usuario y su acceso en Supabase Auth."""
    with Session(engine) as session:
        c = session.exec(select(Colaborador).where(Colaborador.slug == slug)).first()
        if not c:
            return
        email = c.email

        # Eliminar de tabla colaborador
        session.delete(c)
        session.commit()

    # Eliminar de tabla usuario
    delete_usuario(email)

    # Eliminar de Supabase Auth
    try:
        users = supabase_admin.auth.admin.list_users()
        for u in users:
            if u.email == email:
                supabase_admin.auth.admin.delete_user(u.id)
                break
    except Exception:
        pass