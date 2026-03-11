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
        rx.text(label, font_size="0.7em", color="#4a7fa5", font_weight="600", letter_spacing="0.1em", text_transform="uppercase"),
        component,
        align_items="start",
        width="100%",
        spacing="1",
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.text("M", font_family="Georgia, serif", font_size="1.1em", font_weight="bold", color="#c0c8d8"),
                        width="28px", height="28px", background="#0a0a0d",
                        border="1px solid #4a7fa5", border_radius="5px",
                        display="flex", align_items="center", justify_content="center",
                    ),
                    rx.text("El Club de los Marginalistas", font_size="0.9em", color="#c0c8d8", font_weight="600", letter_spacing="0.02em", font_family="Georgia, serif"),
                    spacing="2", align="center",
                ),
                href="/", text_decoration="none",
            ),
            rx.hstack(
                rx.text("PANEL ADMIN", font_size="0.75em", color="#4a7fa5", letter_spacing="0.15em", font_weight="600"),
                rx.link("← Ver blog", href="/", color="#8896aa", font_size="0.8em", _hover={"color": "#c0c8d8"}),
                spacing="4", align="center",
            ),
            justify="between", align="center", width="100%", max_width="1200px", margin="0 auto", padding="0 2em",
        ),
        position="sticky", top="0", z_index="100",
        background="rgba(10,10,13,0.92)", backdrop_filter="blur(20px)",
        border_bottom="1px solid #1e2030", height="64px",
        display="flex", align_items="center", width="100%",
    )


def admin_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                # HEADER
                rx.box(
                    rx.hstack(
                        rx.box(width="3px", height="20px", background="#4a7fa5", border_radius="2px"),
                        rx.vstack(
                            rx.text("NUEVO POST", font_size="0.7em", color="#4a7fa5", letter_spacing="0.15em", font_weight="600"),
                            rx.heading("Crear entrada", size="6", color="#e8eaf0", font_family="Georgia, serif"),
                            align_items="start", spacing="0",
                        ),
                        spacing="3", align="center",
                    ),
                    margin_bottom="2em",
                ),
                # MESSAGE
                rx.cond(
                    AdminState.message != "",
                    rx.box(
                        rx.text(AdminState.message, font_size="0.875em", color="#4a7fa5"),
                        background="#0a0a0d",
                        border="1px solid #4a7fa5",
                        border_radius="4px",
                        padding="0.75em 1.25em",
                        width="100%",
                        margin_bottom="1.5em",
                    ),
                ),
                # FORM
                rx.box(
                    rx.vstack(
                        rx.grid(
                            field("Título", rx.input(
                                value=AdminState.title, on_change=AdminState.set_title,
                                placeholder="Título del post",
                                background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                                border_radius="4px", width="100%",
                                _focus={"border_color": "#4a7fa5"}, _placeholder={"color": "#4a5568"},
                            )),
                            field("Slug (URL)", rx.input(
                                value=AdminState.post_slug, on_change=AdminState.set_post_slug,
                                placeholder="2025-03-01-mi-post",
                                background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                                border_radius="4px", width="100%",
                                _focus={"border_color": "#4a7fa5"}, _placeholder={"color": "#4a5568"},
                            )),
                            field("Autor", rx.input(
                                value=AdminState.author, on_change=AdminState.set_author,
                                placeholder="Tu nombre",
                                background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                                border_radius="4px", width="100%",
                                _focus={"border_color": "#4a7fa5"}, _placeholder={"color": "#4a5568"},
                            )),
                            field("Fecha", rx.input(
                                value=AdminState.date, on_change=AdminState.set_date,
                                placeholder="2025-03-09",
                                background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                                border_radius="4px", width="100%",
                                _focus={"border_color": "#4a7fa5"}, _placeholder={"color": "#4a5568"},
                            )),
                            field("Categoría", rx.select(
                                ["General", "Teoría", "Macro", "Micro"],
                                value=AdminState.category, on_change=AdminState.set_category,
                                background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                                border_radius="4px", width="100%",
                            )),
                            field("Descripción", rx.input(
                                value=AdminState.description, on_change=AdminState.set_description,
                                placeholder="Breve descripción del post",
                                background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                                border_radius="4px", width="100%",
                                _focus={"border_color": "#4a7fa5"}, _placeholder={"color": "#4a5568"},
                            )),
                            columns="2", spacing="4", width="100%",
                        ),
                        field("Contenido (Markdown)", rx.text_area(
                            value=AdminState.content, on_change=AdminState.set_content,
                            placeholder="Escribe el contenido en Markdown...",
                            background="#0a0a0d", border="1px solid #1e2030", color="#e8eaf0",
                            border_radius="4px", width="100%", min_height="280px",
                            _focus={"border_color": "#4a7fa5"}, _placeholder={"color": "#4a5568"},
                        )),
                        rx.button(
                            "Publicar entrada",
                            on_click=AdminState.create_new_post,
                            background="#4a7fa5", color="#e8eaf0",
                            font_weight="600", font_size="0.875em",
                            letter_spacing="0.05em", border_radius="4px",
                            padding="0.65em 1.75em", cursor="pointer", border="none",
                            _hover={"background": "#5a8fb5"}, transition="background 0.2s",
                        ),
                        align_items="start", width="100%", spacing="4",
                    ),
                    background="#0f1219",
                    border="1px solid #1e2030",
                    border_radius="6px",
                    padding="2em",
                    width="100%",
                ),
                # POSTS LIST
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.box(width="3px", height="16px", background="#4a7fa5", border_radius="2px"),
                            rx.text("ENTRADAS PUBLICADAS", font_size="0.7em", color="#8896aa", letter_spacing="0.15em", font_weight="600"),
                            spacing="3", align="center",
                            margin_bottom="1em",
                        ),
                        rx.foreach(
                            AdminState.posts,
                            lambda post: rx.hstack(
                                rx.vstack(
                                    rx.text(post.title, font_weight="500", color="#e8eaf0", font_size="0.9em", font_family="Georgia, serif"),
                                    rx.hstack(
                                        rx.text(post.slug, color="#4a5568", font_size="0.72em"),
                                        rx.text("·", color="#1e2030"),
                                        rx.text(post.category, color="#4a7fa5", font_size="0.72em"),
                                        spacing="2",
                                    ),
                                    align_items="start", spacing="0",
                                ),
                                rx.button(
                                    "Eliminar",
                                    on_click=lambda: AdminState.delete_existing_post(post.slug),
                                    background="transparent",
                                    border="1px solid #2a1a1a",
                                    color="#6b3a3a",
                                    font_size="0.72em",
                                    letter_spacing="0.05em",
                                    border_radius="3px",
                                    padding="0.3em 0.75em",
                                    cursor="pointer",
                                    _hover={"background": "#2a1a1a", "color": "#ef4444", "border_color": "#ef4444"},
                                    transition="all 0.2s",
                                ),
                                justify="between", align="center", width="100%",
                                padding="1em 0", border_bottom="1px solid #1e2030",
                            ),
                        ),
                        align_items="start", width="100%", spacing="0",
                    ),
                    background="#0f1219",
                    border="1px solid #1e2030",
                    border_radius="6px",
                    padding="2em",
                    width="100%",
                    margin_top="2em",
                ),
                align_items="start", width="100%",
            ),
            max_width="960px",
            margin="0 auto",
            padding="3em 2em 6em",
        ),
        min_height="100vh",
        background="#0a0a0d",
        color="#e8eaf0",
        on_mount=AdminState.load_posts,
    )