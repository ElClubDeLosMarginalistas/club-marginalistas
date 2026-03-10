import reflex as rx
from club_marginalistas.utils import get_all_posts, create_post, delete_post
from club_marginalistas.models import Post


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


def field(label: str, component) -> rx.Component:
    return rx.vstack(
        rx.text(label, font_size="0.75em", color="#9ca3af", font_weight="500", letter_spacing="0.05em"),
        component,
        align_items="start",
        width="100%",
        spacing="1",
    )


def admin_page() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.text("el club de los", font_size="0.9em", color="#86efac", font_weight="400"),
                        rx.text("marginalistas", font_size="0.9em", color="white", font_weight="700"),
                        spacing="1",
                    ),
                    href="/",
                ),
                rx.text("Panel Admin", font_size="0.875em", color="#6b7280"),
                justify="between",
                align="center",
                width="100%",
                max_width="1100px",
                margin="0 auto",
                padding="0 2em",
            ),
            position="sticky",
            top="0",
            z_index="100",
            background="rgba(12,12,15,0.85)",
            backdrop_filter="blur(20px)",
            border_bottom="1px solid #2a2a3a",
            height="60px",
            display="flex",
            align_items="center",
            width="100%",
        ),
        rx.box(
            rx.vstack(
                # CREAR POST
                rx.box(
                    rx.vstack(
                        rx.text(
                            "NUEVO POST",
                            font_size="0.7em",
                            color="#86efac",
                            letter_spacing="0.12em",
                            font_weight="600",
                        ),
                        rx.heading("Crear entrada", size="6", color="white", margin_bottom="1em"),
                        rx.cond(
                            AdminState.message != "",
                            rx.text(AdminState.message, font_size="0.875em", color="#86efac"),
                        ),
                        rx.grid(
                            field("Título", rx.input(
                                value=AdminState.title,
                                on_change=AdminState.set_title,
                                placeholder="Título del post",
                                background="#1a1a24",
                                border="1px solid #2a2a3a",
                                color="white",
                                width="100%",
                                _focus={"border_color": "#86efac"},
                            )),
                            field("Slug (URL)", rx.input(
                                value=AdminState.post_slug,
                                on_change=AdminState.set_post_slug,
                                placeholder="2025-03-01-mi-post",
                                background="#1a1a24",
                                border="1px solid #2a2a3a",
                                color="white",
                                width="100%",
                                _focus={"border_color": "#86efac"},
                            )),
                            field("Autor", rx.input(
                                value=AdminState.author,
                                on_change=AdminState.set_author,
                                placeholder="Tu nombre",
                                background="#1a1a24",
                                border="1px solid #2a2a3a",
                                color="white",
                                width="100%",
                                _focus={"border_color": "#86efac"},
                            )),
                            field("Fecha", rx.input(
                                value=AdminState.date,
                                on_change=AdminState.set_date,
                                placeholder="2025-03-09",
                                background="#1a1a24",
                                border="1px solid #2a2a3a",
                                color="white",
                                width="100%",
                                _focus={"border_color": "#86efac"},
                            )),
                            field("Categoría", rx.select(
                                ["General", "Teoría", "Macro", "Micro"],
                                value=AdminState.category,
                                on_change=AdminState.set_category,
                                background="#1a1a24",
                                border="1px solid #2a2a3a",
                                color="white",
                                width="100%",
                            )),
                            field("Descripción", rx.input(
                                value=AdminState.description,
                                on_change=AdminState.set_description,
                                placeholder="Breve descripción del post",
                                background="#1a1a24",
                                border="1px solid #2a2a3a",
                                color="white",
                                width="100%",
                                _focus={"border_color": "#86efac"},
                            )),
                            columns="2",
                            spacing="4",
                            width="100%",
                        ),
                        field("Contenido (Markdown)", rx.text_area(
                            value=AdminState.content,
                            on_change=AdminState.set_content,
                            placeholder="Escribe el contenido en Markdown...",
                            background="#1a1a24",
                            border="1px solid #2a2a3a",
                            color="white",
                            width="100%",
                            min_height="250px",
                            _focus={"border_color": "#86efac"},
                        )),
                        rx.button(
                            "Publicar entrada",
                            on_click=AdminState.create_new_post,
                            background="#86efac",
                            color="#0c0c0f",
                            font_weight="600",
                            border_radius="8px",
                            padding="0.65em 1.5em",
                            cursor="pointer",
                            _hover={"opacity": "0.9"},
                        ),
                        align_items="start",
                        width="100%",
                        spacing="4",
                    ),
                    background="#13131a",
                    border="1px solid #2a2a3a",
                    border_radius="12px",
                    padding="2em",
                    width="100%",
                ),
                # LISTA DE POSTS
                rx.box(
                    rx.vstack(
                        rx.text(
                            "ENTRADAS PUBLICADAS",
                            font_size="0.7em",
                            color="#6b7280",
                            letter_spacing="0.12em",
                            font_weight="500",
                        ),
                        rx.foreach(
                            AdminState.posts,
                            lambda post: rx.hstack(
                                rx.vstack(
                                    rx.text(post.title, font_weight="500", color="white", font_size="0.9em"),
                                    rx.text(post.slug, color="#6b7280", font_size="0.75em"),
                                    align_items="start",
                                    spacing="0",
                                ),
                                rx.button(
                                    "Eliminar",
                                    on_click=lambda: AdminState.delete_existing_post(post.slug),
                                    background="transparent",
                                    border="1px solid #ef4444",
                                    color="#ef4444",
                                    font_size="0.75em",
                                    border_radius="6px",
                                    padding="0.3em 0.75em",
                                    cursor="pointer",
                                    _hover={"background": "#ef4444", "color": "white"},
                                ),
                                justify="between",
                                align="center",
                                width="100%",
                                padding="1em 0",
                                border_bottom="1px solid #2a2a3a",
                            ),
                        ),
                        align_items="start",
                        width="100%",
                        spacing="2",
                    ),
                    background="#13131a",
                    border="1px solid #2a2a3a",
                    border_radius="12px",
                    padding="2em",
                    width="100%",
                    margin_top="1.5em",
                ),
                align_items="start",
                width="100%",
            ),
            max_width="900px",
            margin="0 auto",
            padding="3em 2em 5em",
        ),
        min_height="100vh",
        background="#0c0c0f",
        color="white",
        on_mount=AdminState.load_posts,
    )