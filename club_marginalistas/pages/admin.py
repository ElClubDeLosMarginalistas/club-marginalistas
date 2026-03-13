import reflex as rx
from club_marginalistas.utils import (
    get_all_posts_admin, get_pending_posts,
    create_post, delete_post, update_post_status,
    get_all_usuarios, create_usuario, delete_usuario,
)
from club_marginalistas.models import Post, Usuario
from club_marginalistas.auth import AuthState
from club_marginalistas.styles import (
    page_wrapper, admin_navbar, footer,
    section_header, input_style, textarea_style, select_style,
    btn_primary, btn_danger, panel, form_field,
    feedback_message, post_list_item, page_section_title,
    admin_content_wrapper, accent_divider, CATEGORIES_FORM, C,
)


class AdminState(AuthState):
    posts:         list[Post]    = []
    pending_posts: list[Post]    = []
    usuarios:      list[Usuario] = []

    title:       str = ""
    description: str = ""
    author:      str = ""
    date:        str = ""
    category:    str = "General"
    content:     str = ""
    post_slug:   str = ""

    new_user_email: str = ""
    new_user_name:  str = ""
    new_user_role:  str = "colaborador"

    message: str = ""

    def set_title(self, v):          self.title = v
    def set_description(self, v):    self.description = v
    def set_author(self, v):         self.author = v
    def set_date(self, v):           self.date = v
    def set_category(self, v):       self.category = v
    def set_content(self, v):        self.content = v
    def set_post_slug(self, v):      self.post_slug = v
    def set_new_user_email(self, v): self.new_user_email = v
    def set_new_user_name(self, v):  self.new_user_name = v
    def set_new_user_role(self, v):  self.new_user_role = v

    def load_data(self):
        if not self.logged_in or self.user_role != "admin":
            return rx.redirect("/login")
        self.posts         = get_all_posts_admin()
        self.pending_posts = get_pending_posts()
        self.usuarios      = get_all_usuarios()

    def create_new_post(self):
        if not self.title or not self.post_slug or not self.content:
            self.message = "❌ Título, slug y contenido son obligatorios."
            return
        create_post(Post(
            slug=self.post_slug, title=self.title,
            description=self.description, author=self.author,
            date=self.date, category=self.category,
            content=self.content, status="published",
        ))
        self.message = "✅ Post publicado."
        self.title = self.description = self.author = ""
        self.date = self.post_slug = self.content = ""
        self.category = "General"
        self.load_data()

    def delete_post(self, slug: str):
        delete_post(slug)
        self.message = "🗑️ Post eliminado."
        self.load_data()

    def approve_post(self, slug: str):
        update_post_status(slug, "published")
        self.message = "✅ Post aprobado y publicado."
        self.load_data()

    def reject_post(self, slug: str):
        update_post_status(slug, "draft")
        self.message = "🗑️ Post rechazado."
        self.load_data()

    def create_new_usuario(self):
        if not self.new_user_email:
            self.message = "❌ El email es obligatorio."
            return
        create_usuario(Usuario(
            email=self.new_user_email,
            name=self.new_user_name,
            role=self.new_user_role,
        ))
        self.message = f"✅ Usuario {self.new_user_email} creado."
        self.new_user_email = self.new_user_name = ""
        self.new_user_role = "colaborador"
        self.load_data()

    def delete_usuario(self, email: str):
        delete_usuario(email)
        self.message = "🗑️ Usuario eliminado."
        self.load_data()


def create_form() -> rx.Component:
    return panel(
        rx.vstack(
            rx.grid(
                form_field("Título",      rx.input(value=AdminState.title,       on_change=AdminState.set_title,       placeholder="Título del post",    **input_style)),
                form_field("Slug (URL)",  rx.input(value=AdminState.post_slug,   on_change=AdminState.set_post_slug,   placeholder="2025-03-01-mi-post", **input_style)),
                form_field("Autor",       rx.input(value=AdminState.author,      on_change=AdminState.set_author,      placeholder="Tu nombre",          **input_style)),
                form_field("Fecha",       rx.input(value=AdminState.date,        on_change=AdminState.set_date,        placeholder="2025-03-09",         **input_style)),
                form_field("Categoría",   rx.select(CATEGORIES_FORM, value=AdminState.category, on_change=AdminState.set_category, **select_style)),
                form_field("Descripción", rx.input(value=AdminState.description, on_change=AdminState.set_description, placeholder="Breve descripción",  **input_style)),
                columns="2", spacing="4", width="100%",
            ),
            form_field("Contenido (Markdown)",
                rx.text_area(value=AdminState.content, on_change=AdminState.set_content,
                             placeholder="Escribe el contenido en Markdown...", **textarea_style),
            ),
            btn_primary("Publicar entrada", on_click=AdminState.create_new_post),
            align_items="start", width="100%", spacing="4",
        ),
    )


def pending_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("PENDIENTES DE APROBACIÓN"),
            rx.foreach(
                AdminState.pending_posts,
                lambda post: rx.hstack(
                    rx.vstack(
                        rx.text(post.title,  font_weight="500", font_size="0.9em"),
                        rx.text(post.author, font_size="0.75em"),
                        align_items="start", spacing="0",
                    ),
                    rx.hstack(
                        btn_primary("Aprobar",  on_click=AdminState.approve_post(post.slug)),
                        btn_danger("Rechazar",  on_click=AdminState.reject_post(post.slug)),
                        spacing="2",
                    ),
                    justify="between", align="center", width="100%",
                    padding="1em 0", border_bottom=f"1px solid {C['border']}",
                ),
            ),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def posts_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("TODAS LAS ENTRADAS"),
            rx.foreach(
                AdminState.posts,
                lambda post: post_list_item(post, AdminState.delete_post(post.slug)),
            ),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def usuarios_form() -> rx.Component:
    return panel(
        rx.vstack(
            rx.grid(
                form_field("Email",  rx.input(value=AdminState.new_user_email, on_change=AdminState.set_new_user_email, placeholder="colaborador@correo.com", **input_style)),
                form_field("Nombre", rx.input(value=AdminState.new_user_name,  on_change=AdminState.set_new_user_name,  placeholder="Nombre completo",        **input_style)),
                form_field("Rol",    rx.select(["colaborador", "admin"], value=AdminState.new_user_role, on_change=AdminState.set_new_user_role, **select_style)),
                columns="2", spacing="4", width="100%",
            ),
            btn_primary("Crear usuario", on_click=AdminState.create_new_usuario),
            align_items="start", width="100%", spacing="4",
        ),
    )


def usuarios_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("USUARIOS REGISTRADOS"),
            rx.foreach(
                AdminState.usuarios,
                lambda u: rx.hstack(
                    rx.vstack(
                        rx.text(u.name,  font_weight="500", font_size="0.9em"),
                        rx.hstack(
                            rx.text(u.email, font_size="0.72em"),
                            rx.text("·",     font_size="0.72em"),
                            rx.text(u.role,  font_size="0.72em"),
                            spacing="2",
                        ),
                        align_items="start", spacing="0",
                    ),
                    btn_danger("Eliminar", on_click=AdminState.delete_usuario(u.email)),
                    justify="between", align="center", width="100%",
                    padding="1em 0", border_bottom=f"1px solid {C['border']}",
                ),
            ),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def admin_page() -> rx.Component:
    return page_wrapper(
        admin_navbar(),
        admin_content_wrapper(
            page_section_title("NUEVO POST", "Crear entrada"),
            feedback_message(AdminState.message),
            create_form(),
            pending_list(),
            posts_list(),
            accent_divider(),
            page_section_title("USUARIOS", "Gestionar colaboradores"),
            usuarios_form(),
            usuarios_list(),
        ),
        footer(),
        on_mount=AdminState.load_data,
    )