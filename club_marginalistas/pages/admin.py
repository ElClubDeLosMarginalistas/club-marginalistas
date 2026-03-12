import reflex as rx
from club_marginalistas.utils import get_all_posts, create_post, delete_post
from club_marginalistas.models import Post
from club_marginalistas.styles import (
    page_wrapper, admin_navbar, footer,
    section_header, input_style, textarea_style, select_style,
    btn_primary, panel, form_field, feedback_message,
    post_list_item, page_section_title, admin_content_wrapper,
    CATEGORIES_FORM,
)


class AdminState(rx.State):
    posts: list[Post] = []
    title: str = ""
    description: str = ""
    author: str = ""
    date: str = ""
    category: str = "General"
    content: str = ""
    post_slug: str = ""
    message: str = ""

    # --- setters compactos ---
    def set_title(self, v):       self.title = v
    def set_description(self, v): self.description = v
    def set_author(self, v):      self.author = v
    def set_date(self, v):        self.date = v
    def set_category(self, v):    self.category = v
    def set_content(self, v):     self.content = v
    def set_post_slug(self, v):   self.post_slug = v

    def load_posts(self):
        self.posts = get_all_posts()

    def create_new_post(self):
        if not self.title or not self.post_slug or not self.content:
            self.message = "❌ Título, slug y contenido son obligatorios."
            return
        create_post(Post(
            slug=self.post_slug, title=self.title,
            description=self.description, author=self.author,
            date=self.date, category=self.category, content=self.content,
        ))
        self.message = "✅ Post creado exitosamente."
        self.title = self.description = self.author = ""
        self.date = self.post_slug = self.content = ""
        self.category = "General"
        self.load_posts()

    def delete_post(self, slug: str):
        delete_post(slug)
        self.message = "🗑️ Post eliminado."
        self.load_posts()


def create_form() -> rx.Component:
    return panel(
        rx.vstack(
            rx.grid(
                form_field("Título",       rx.input(value=AdminState.title,       on_change=AdminState.set_title,       placeholder="Título del post",        **input_style)),
                form_field("Slug (URL)",   rx.input(value=AdminState.post_slug, on_change=AdminState.set_post_slug, placeholder="2025-03-01-mi-post",     **input_style)),
                form_field("Autor",        rx.input(value=AdminState.author,      on_change=AdminState.set_author,      placeholder="Tu nombre",              **input_style)),
                form_field("Fecha",        rx.input(value=AdminState.date,        on_change=AdminState.set_date,        placeholder="2025-03-09",             **input_style)),
                form_field("Categoría",    rx.select(CATEGORIES_FORM, value=AdminState.category, on_change=AdminState.set_category, **select_style)),
                form_field("Descripción",  rx.input(value=AdminState.description, on_change=AdminState.set_description, placeholder="Breve descripción",      **input_style)),
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


def posts_list() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("ENTRADAS PUBLICADAS"),
            rx.foreach(
                AdminState.posts,
                # Patrón correcto: pasar el método con el slug como argumento explícito
                lambda post: post_list_item(
                    post,
                    AdminState.delete_post(post.slug),
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
            posts_list(),
        ),
        footer(),
        on_mount=AdminState.load_posts,
    )