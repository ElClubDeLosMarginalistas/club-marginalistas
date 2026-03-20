import reflex as rx
from club_marginalistas.utils import (
    get_all_posts_admin, get_pending_posts,
    delete_post, update_post_status,
    get_all_usuarios, create_usuario, delete_usuario,
)
from club_marginalistas.models import Post, Usuario
from club_marginalistas.auth import AuthState
from club_marginalistas.styles import (
    page_wrapper, portal_navbar, 
    section_header, input_style, select_style,
    btn_primary, btn_danger, panel, form_field,
    feedback_message, page_section_title,
    admin_content_wrapper, accent_divider,
    markdown_content, post_meta_header, C,
)


class AdminState(AuthState):
    posts:         list[Post]    = []
    pending_posts: list[Post]    = []
    usuarios:      list[Usuario] = []
    preview_post:  Post          = Post()
    show_preview:  bool          = False

    new_user_email: str = ""
    new_user_name:  str = ""
    new_user_role:  str = "colaborador"

    message: str = ""

    def set_new_user_email(self, v): self.new_user_email = v
    def set_new_user_name(self, v):  self.new_user_name = v
    def set_new_user_role(self, v):  self.new_user_role = v

    def load_data(self):
        if not self.logged_in or self.user_role != "admin":
            return rx.redirect("/login")
        self.posts         = get_all_posts_admin()
        self.pending_posts = get_pending_posts()
        self.usuarios      = get_all_usuarios()

    def preview(self, slug: str):
        for p in self.pending_posts:
            if p.slug == slug:
                self.preview_post = p
                self.show_preview = True
                return

    def close_preview(self):
        self.show_preview = False
        self.preview_post = Post()

    def approve_post(self, slug: str):
        update_post_status(slug, "published")
        self.message = "✅ Post aprobado y publicado."
        self.show_preview = False
        self.load_data()

    def reject_post(self, slug: str):
        update_post_status(slug, "draft")
        self.message = "🗑️ Post rechazado."
        self.show_preview = False
        self.load_data()

    def confirm_delete_post(self, slug: str):
        delete_post(slug)
        self.message = "🗑️ Post eliminado."
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

    def confirm_delete_usuario(self, email: str):
        delete_usuario(email)
        self.message = "🗑️ Usuario eliminado."
        self.load_data()


def post_preview_modal() -> rx.Component:
    return rx.cond(
        AdminState.show_preview,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        page_section_title("VISTA PREVIA", AdminState.preview_post.title),
                        rx.button(
                            "✕", on_click=AdminState.close_preview,
                            background="transparent", color=C["muted"],
                            border="none", font_size="1.2em", cursor="pointer",
                            _hover={"color": C["text"]},
                        ),
                        justify="between", align="center", width="100%",
                    ),
                    accent_divider(),
                    post_meta_header(
                        AdminState.preview_post.category,
                        AdminState.preview_post.date,
                        AdminState.preview_post.title,
                        AdminState.preview_post.author,
                    ),
                    markdown_content(AdminState.preview_post.content),
                    accent_divider(),
                    rx.hstack(
                        btn_primary("✅ Aprobar y publicar", on_click=AdminState.approve_post(AdminState.preview_post.slug)),
                        btn_danger("❌ Rechazar",            on_click=AdminState.reject_post(AdminState.preview_post.slug)),
                        spacing="3",
                    ),
                    align_items="start", width="100%", spacing="4",
                ),
                background=C["surface"],
                border=f"1px solid {C['border']}",
                border_radius="8px",
                padding="2em",
                max_width="760px",
                width="90%",
                max_height="85vh",
                overflow_y="auto",
            ),
            position="fixed", top="0", left="0",
            width="100%", height="100%",
            background="rgba(0,0,0,0.75)",
            display="flex", align_items="center", justify_content="center",
            z_index="200",
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
                        rx.text(post.title,  font_weight="500", font_size="0.9em", color=C["text"]),
                        rx.text(post.author, font_size="0.75em", color=C["muted"]),
                        align_items="start", spacing="0",
                    ),
                    rx.hstack(
                        btn_primary("Ver post", on_click=AdminState.preview(post.slug)),
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
            section_header("TODAS LAS ENTRADAS PUBLICADAS"),
            rx.foreach(
                AdminState.posts,
                lambda post: rx.hstack(
                    rx.vstack(
                        rx.text(post.title, font_weight="500", color=C["text"], font_size="0.9em"),
                        rx.hstack(
                            rx.text(post.slug,     color=C["dim"],    font_size="0.72em"),
                            rx.text("·",           color=C["border"], font_size="0.72em"),
                            rx.text(post.category, color=C["accent"], font_size="0.72em"),
                            rx.text("·",           color=C["border"], font_size="0.72em"),
                            rx.text(post.status,   color=C["muted"],  font_size="0.72em"),
                            spacing="2",
                        ),
                        align_items="start", spacing="0",
                    ),
                    rx.alert_dialog.root(
                        rx.alert_dialog.trigger(
                            btn_danger("Eliminar"),
                        ),
                        rx.alert_dialog.content(
                            rx.alert_dialog.title("¿Eliminar este post?"),
                            rx.alert_dialog.description(f"Esta acción no se puede deshacer."),
                            rx.hstack(
                                rx.alert_dialog.cancel(rx.button("Cancelar", background="transparent", color=C["muted"], border=f"1px solid {C['border']}", cursor="pointer")),
                                rx.alert_dialog.action(btn_danger("Sí, eliminar", on_click=AdminState.confirm_delete_post(post.slug))),
                                spacing="3", justify="end",
                            ),
                            background=C["surface"], color=C["text"],
                            border=f"1px solid {C['border']}",
                        ),
                    ),
                    justify="between", align="center", width="100%",
                    padding="1em 0", border_bottom=f"1px solid {C['border']}",
                ),
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
                        rx.text(u.name,  font_weight="500", font_size="0.9em", color=C["text"]),
                        rx.hstack(
                            rx.text(u.email, font_size="0.72em", color=C["dim"]),
                            rx.text("·",     font_size="0.72em", color=C["border"]),
                            rx.text(u.role,  font_size="0.72em", color=C["accent"]),
                            spacing="2",
                        ),
                        align_items="start", spacing="0",
                    ),
                    rx.alert_dialog.root(
                        rx.alert_dialog.trigger(btn_danger("Eliminar")),
                        rx.alert_dialog.content(
                            rx.alert_dialog.title("¿Eliminar este usuario?"),
                            rx.alert_dialog.description("Esta acción no se puede deshacer."),
                            rx.hstack(
                                rx.alert_dialog.cancel(rx.button("Cancelar", background="transparent", color=C["muted"], border=f"1px solid {C['border']}", cursor="pointer")),
                                rx.alert_dialog.action(btn_danger("Sí, eliminar", on_click=AdminState.confirm_delete_usuario(u.email))),
                                spacing="3", justify="end",
                            ),
                            background=C["surface"], color=C["text"],
                            border=f"1px solid {C['border']}",
                        ),
                    ),
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
        portal_navbar("PANEL ADMIN", AdminState.logout),
        post_preview_modal(),
        admin_content_wrapper(
            page_section_title("POSTS", "Gestión de entradas"),
            feedback_message(AdminState.message),
            pending_list(),
            posts_list(),
            accent_divider(),
            page_section_title("USUARIOS", "Gestionar colaboradores"),
            usuarios_form(),
            usuarios_list(),
        ),
        on_mount=AdminState.load_data,
    )