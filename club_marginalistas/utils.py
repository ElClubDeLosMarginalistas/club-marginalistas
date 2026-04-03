from sqlmodel import Session, create_engine, select
from club_marginalistas.models import Post, Usuario, Colaborador, SQLModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import resend

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


def update_colaborador(slug: str, data: dict):
    """Actualiza los campos del colaborador. No modifica email ni acceso Auth."""
    with Session(engine) as session:
        c = session.exec(select(Colaborador).where(Colaborador.slug == slug)).first()
        if not c:
            return
        for key, value in data.items():
            setattr(c, key, value)
        session.add(c)
        session.commit()


# ============================================
# NEWSLETTER
# ============================================

def subscribe_newsletter(email: str) -> dict:
    """Añade un contacto al Audience de Resend."""
    resend.api_key = os.getenv("RESEND_API_KEY")
    try:
        resend.Contacts.create({
            "email": email,
            "audience_id": os.getenv("RESEND_AUDIENCE_ID"),
            "unsubscribed": False,
        })
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _newsletter_html(post: Post, post_url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#0a0a0d;font-family:Georgia,serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a0d;padding:40px 20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

        <!-- Header -->
        <tr><td style="padding-bottom:24px;border-bottom:1px solid #1e2030;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td style="width:36px;">
                <div style="width:36px;height:36px;background:#0a0a0d;border:1px solid #4a7fa5;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;text-align:center;line-height:36px;">
                  <span style="font-family:Georgia,serif;font-size:1.1em;font-weight:bold;color:#c0c8d8;">M</span>
                </div>
              </td>
              <td style="padding-left:12px;">
                <span style="font-family:Georgia,serif;font-size:0.95em;font-weight:600;color:#c0c8d8;letter-spacing:0.02em;">El Club de los Marginalistas</span>
              </td>
            </tr>
          </table>
        </td></tr>

        <!-- Eyebrow -->
        <tr><td style="padding-top:32px;padding-bottom:8px;">
          <span style="font-size:0.7em;color:#4a7fa5;letter-spacing:0.2em;font-weight:600;font-family:system-ui,sans-serif;text-transform:uppercase;">NUEVA ENTRADA</span>
        </td></tr>

        <!-- Title -->
        <tr><td style="padding-bottom:16px;">
          <h1 style="margin:0;font-family:Georgia,serif;font-size:1.75em;font-weight:700;color:#e8eaf0;line-height:1.2;letter-spacing:-0.02em;">{post.title}</h1>
        </td></tr>

        <!-- Meta -->
        <tr><td style="padding-bottom:20px;">
          <span style="font-size:0.72em;color:#4a7fa5;letter-spacing:0.1em;font-family:system-ui,sans-serif;text-transform:uppercase;">{post.category}</span>
          <span style="color:#1e2030;margin:0 8px;">·</span>
          <span style="font-size:0.72em;color:#6b7a8d;font-family:system-ui,sans-serif;">{post.date}</span>
          <span style="color:#1e2030;margin:0 8px;">·</span>
          <span style="font-size:0.72em;color:#6b7a8d;font-family:system-ui,sans-serif;">{post.author}</span>
        </td></tr>

        <!-- Divider -->
        <tr><td style="padding-bottom:20px;">
          <div style="height:1px;background:linear-gradient(90deg,#4a7fa5,transparent);width:100%;"></div>
        </td></tr>

        <!-- Description -->
        <tr><td style="padding-bottom:28px;">
          <p style="margin:0;font-size:0.95em;color:#8896aa;line-height:1.75;font-family:system-ui,sans-serif;">{post.description}</p>
        </td></tr>

        <!-- CTA -->
        <tr><td style="padding-bottom:40px;">
          <a href="{post_url}" style="display:inline-block;background:#4a7fa5;color:#e8eaf0;text-decoration:none;font-size:0.875em;font-weight:600;letter-spacing:0.05em;border-radius:4px;padding:0.65em 1.75em;font-family:system-ui,sans-serif;">Leer entrada →</a>
        </td></tr>

        <!-- Footer -->
        <tr><td style="border-top:1px solid #1e2030;padding-top:24px;">
          <p style="margin:0;font-size:0.72em;color:#4a5568;line-height:1.6;font-family:system-ui,sans-serif;">
            Recibiste este correo porque te suscribiste al newsletter de elclubdelosmarginalistas.com.<br>
            Para darte de baja responde a este correo con el asunto "Cancelar suscripción".
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_newsletter_post(post: Post) -> None:
    """Envía notificación del nuevo post a todos los suscriptores activos."""
    resend.api_key = os.getenv("RESEND_API_KEY")
    audience_id = os.getenv("RESEND_AUDIENCE_ID")
    try:
        contacts_resp = resend.Contacts.list(audience_id=audience_id)
        recipients = [
            c["email"] for c in contacts_resp.get("data", [])
            if not c.get("unsubscribed", False)
        ]
        if not recipients:
            return
        post_url = f"https://elclubdelosmarginalistas.com/blog/{post.slug}"
        html = _newsletter_html(post, post_url)
        batch = [
            {
                "from": "El Club de los Marginalistas <newsletter@elclubdelosmarginalistas.com>",
                "to": [email],
                "subject": f"Nueva entrada: {post.title}",
                "html": html,
            }
            for email in recipients
        ]
        resend.Batch.send(batch)
    except Exception:
        pass  # No bloquear la aprobación del post si falla el envío


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