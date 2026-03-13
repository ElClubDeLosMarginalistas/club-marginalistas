import reflex as rx
from club_marginalistas.utils import create_post, get_all_posts
from club_marginalistas.models import Post
from club_marginalistas.auth import AuthState
from club_marginalistas.styles import (
    page_wrapper, navbar, footer,
    panel, form_field, btn_primary, feedback_message,
    section_header, input_style, textarea_style, select_style,
    page_section_title, post_list_item,
    admin_content_wrapper, CATEGORIES_FORM,
)


class PortalState(AuthState):
    posts:     list[Post] = []
    title:     str = ""
    description: str = ""
    date:      str = ""
    category:  str = "General"
    content:   str = ""
    post_slug: str = ""
    message:   str = ""

    def set_title(self, v):       self.title = v
    def set_description(self, v): self.description = v
    def set_date(self, v):        self.date = v
    def set_category(self, v):    self.category = v
    def set_content(self, v):     self.content = v
    def set_post_slug(self, v):   self.post_slug = v

    def load_posts(self):
        if not self.logged_in:
            return rx.redirect("/login")
        all_posts = get_all_posts("pending") + get_all_posts("published")
        self.posts = [p for p in all_posts if p.author == self.user_email]

    def submit_post(self):
        if not self.title or not self.post_slug or not self.content:
            self.message = "❌ Título, slug y contenido son obligatorios."
            return
        create_post(Post(
            slug=self.post_slug, title=self.title,
            description=self.description,
            author=self.user_email,
            date=self.date, category=self.category,
            content=self.content,
            status="pending",
        ))
        self.message = "✅ Post enviado. Quedará publicado una vez que el admin lo apruebe."
        self.title = self.description = ""
        self.date = self.post_slug = self.content = ""
        self.category = "General"
        self.load_posts()


def submit_form() -> rx.Component:
    return panel(
        rx.vstack(
            rx.grid(
                form_field("Título",      rx.input(value=PortalState.title,       on_change=PortalState.set_title,       placeholder="Título del post",    **input_style)),
                form_field("Slug (URL)",  rx.input(value=PortalState.post_slug,   on_change=PortalState.set_post_slug,   placeholder="2025-03-01-mi-post", **input_style)),
                form_field("Fecha",       rx.input(value=PortalState.date,        on_change=PortalState.set_date,        placeholder="2025-03-09",         **input_style)),
                form_field("Categoría",   rx.select(CATEGORIES_FORM, value=PortalState.category, on_change=PortalState.set_category, **select_style)),
                form_field("Descripción", rx.input(value=PortalState.description, on_change=PortalState.set_description, placeholder="Breve descripción",  **input_style)),
                columns="2", spacing="4", width="100%",
            ),
            form_field("Contenido (Markdown)",
                rx.text_area(value=PortalState.content, on_change=PortalState.set_content,
                             placeholder="Escribe el contenido en Markdown...", **textarea_style),
            ),
            btn_primary("Enviar para revisión", on_click=PortalState.submit_post),
            align_items="start", width="100%", spacing="4",
        ),
    )


def my_posts() -> rx.Component:
    return panel(
        rx.vstack(
            section_header("MIS ENTRADAS"),
            rx.foreach(PortalState.posts, lambda post: post_list_item(post, None)),
            align_items="start", width="100%", spacing="0",
        ),
        margin_top="2em",
    )


def portal_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        admin_content_wrapper(
            page_section_title("PORTAL COLABORADOR", "Nueva entrada"),
            feedback_message(PortalState.message),
            submit_form(),
            my_posts(),
        ),
        footer(),
        on_mount=PortalState.load_posts,
    )