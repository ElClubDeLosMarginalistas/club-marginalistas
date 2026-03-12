import reflex as rx
from club_marginalistas.utils import get_all_posts, create_post, delete_post
from club_marginalistas.models import Post
from club_marginalistas.styles import (
    colors, fonts, admin_navbar, footer, section_header,
    input_style, btn_primary, btn_danger, panel, form_field, page_wrapper
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

    def set_title(self, value: str): self.title = value
    def set_description(self, value: str): self.description = value
    def set_author(self, value: str): self.author = value
    def set_date(self, value: str): self.date = value
    def set_category(self, value: str): self.category = value
    def set_content(self, value: str): self.content = value
    def set_post_slug(self, value: str): self.post_slug = value

    def load_posts(self):
        self.posts = get_all_posts()

    def create_new_post(self):
        if not self.title or not self.post_slug or not self.content:
            self.message = "❌ Título, slug y contenido son obligatorios."
            return
        post = Post(
            slug=self.post_slug,
            title=self.title,
            description=self.description,
            author=self.author,
            date=self.date,
            category=self.category,
            content=self.content,
        )
        create_post(post)
        self.message = "✅ Post creado exitosamente."
        self.title = ""
        self.description = ""
        self.author = ""
        self.date = ""
        self.post_slug = ""
        self.content = ""
        self.load_posts()

    def delete_existing_post(self, slug: str):
        delete_post(slug)
        self.message = "🗑️ Post eliminado."
        self.load_posts()


def admin_page() -> rx.Component:
    return page_wrapper(
        admin_navbar(),
        rx.box(
            rx.vstack(
                # HEADER
                rx.hstack(
                    rx.box(width="3px", height="20px", background=colors["accent"], border_radius="2px"),
                    rx.vstack(
                        rx.text("NUEVO POST", font_size="0.7em", color=colors["accent"], letter_spacing="0.15em", font_weight="600"),
                        rx.heading("Crear entrada", size="6", color=colors["text"], font_family=fonts["serif"]),
                        align_items="start", spacing="0",
                    ),
                    spacing="3", align="center",
                    margin_bottom="2em",
                ),
                # MENSAJE
                rx.cond(
                    AdminState.message != "",
                    rx.box(
                        rx.text(AdminState.message, font_size="0.875em", color=colors["accent"]),
                        background=colors["bg"],
                        border=f"1px solid {colors['accent']}",
                        border_radius="4px",
                        padding="0.75em 1.25em",
                        width="100%",
                        margin_bottom="1.5em",
                    ),
                ),
                # FORMULARIO
                panel(
                    rx.vstack(
                        rx.grid(
                            form_field("Título", rx.input(value=AdminState.title, on_change=AdminState.set_title, placeholder="Título del post", **input_style)),
                            form_field("Slug (URL)", rx.input(value=AdminState.post_slug, on_change=AdminState.set_post_slug, placeholder="2025-03-01-mi-post", **input_style)),
                            form_field("Autor", rx.input(value=AdminState.author, on_change=AdminState.set_author, placeholder="Tu nombre", **input_style)),
                            form_field("Fecha", rx.input(value=AdminState.date, on_change=AdminState.set_date, placeholder="2025-03-09", **input_style)),
                            form_field("Categoría", rx.select(
                                ["General", "Teoría", "Macro", "Micro"],
                                value=AdminState.category, on_change=AdminState.set_category,
                                background=colors["bg"], border=f"1px solid {colors['border']}",
                                color=colors["text"], border_radius="4px", width="100%",
                            )),
                            form_field("Descripción", rx.input(value=AdminState.description, on_change=AdminState.set_description, placeholder="Breve descripción", **input_style)),
                            columns="2", spacing="4", width="100%",
                        ),
                        form_field("Contenido (Markdown)", rx.text_area(
                            value=AdminState.content, on_change=AdminState.set_content,
                            placeholder="Escribe el contenido en Markdown...",
                            background=colors["bg"], border=f"1px solid {colors['border']}",
                            color=colors["text"], border_radius="4px", width="100%",
                            min_height="280px", _focus={"border_color": colors["accent"]},
                            _placeholder={"color": colors["dim"]},
                        )),
                        btn_primary("Publicar entrada", on_click=AdminState.create_new_post),
                        align_items="start", width="100%", spacing="4",
                    ),
                ),
                # LISTA DE POSTS
                panel(
                    rx.vstack(
                        section_header("ENTRADAS PUBLICADAS"),
                        rx.foreach(
                            AdminState.posts,
                            lambda post: rx.hstack(
                                rx.vstack(
                                    rx.text(post.title, font_weight="500", color=colors["text"], font_size="0.9em", font_family=fonts["serif"]),
                                    rx.hstack(
                                        rx.text(post.slug, color=colors["dim"], font_size="0.72em"),
                                        rx.text("·", color=colors["border"]),
                                        rx.text(post.category, color=colors["accent"], font_size="0.72em"),
                                        spacing="2",
                                    ),
                                    align_items="start", spacing="0",
                                ),
                                btn_danger("Eliminar", on_click=lambda: AdminState.delete_existing_post(post.slug)),
                                justify="between", align="center", width="100%",
                                padding="1em 0", border_bottom=f"1px solid {colors['border']}",
                            ),
                        ),
                        align_items="start", width="100%", spacing="0",
                    ),
                    margin_top="2em",
                ),
                align_items="start", width="100%",
            ),
            max_width="960px", margin="0 auto", padding="3em 2em 6em",
        ),
        footer(),
        on_mount=AdminState.load_posts,
    )