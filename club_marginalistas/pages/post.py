import reflex as rx
from club_marginalistas.utils import get_all_posts


class PostState(rx.State):
    post_slug: str = ""
    title: str = ""
    description: str = ""
    author: str = ""
    date: str = ""
    category: str = ""
    content: str = ""
    found: bool = False

    def load_post(self):
        slug = self.router.page.params.get("slug", "")
        self.post_slug = slug
        for post in get_all_posts():
            if post.slug == slug:
                self.title = post.title
                self.description = post.description
                self.author = post.author
                self.date = post.date
                self.category = post.category
                self.content = post.content
                self.found = True
                return
        self.found = False


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.text(
                        "el club de los",
                        font_size="0.9em",
                        color="#86efac",
                        font_weight="400",
                    ),
                    rx.text(
                        "marginalistas",
                        font_size="0.9em",
                        color="white",
                        font_weight="700",
                    ),
                    spacing="1",
                ),
                href="/",
            ),
            rx.hstack(
                rx.link("Inicio", href="/", color="#9ca3af", font_size="0.875em", _hover={"color": "white"}),
                rx.link("Teoría", href="/", color="#9ca3af", font_size="0.875em", _hover={"color": "white"}),
                rx.link("Macro", href="/", color="#9ca3af", font_size="0.875em", _hover={"color": "white"}),
                rx.link("Micro", href="/", color="#9ca3af", font_size="0.875em", _hover={"color": "white"}),
                rx.link("Acerca", href="/", color="#9ca3af", font_size="0.875em", _hover={"color": "white"}),
                spacing="6",
            ),
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
    )


def post_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.link(
                    "← Volver al blog",
                    href="/",
                    color="#86efac",
                    font_size="0.875em",
                    margin_bottom="2em",
                    _hover={"color": "white"},
                ),
                rx.cond(
                    PostState.found,
                    rx.vstack(
                        rx.text(
                            PostState.category,
                            font_size="0.7em",
                            color="#86efac",
                            font_weight="600",
                            letter_spacing="0.12em",
                            text_transform="uppercase",
                            margin_bottom="0.75em",
                        ),
                        rx.heading(
                            PostState.title,
                            size="8",
                            font_weight="700",
                            line_height="1.15",
                            color="white",
                            margin_bottom="0.75em",
                        ),
                        rx.hstack(
                            rx.text(PostState.author, font_size="0.9em", font_weight="500", color="#e5e7eb"),
                            rx.text("·", color="#6b7280"),
                            rx.text(PostState.date, font_size="0.9em", color="#6b7280"),
                            margin_bottom="2em",
                            spacing="2",
                        ),
                        rx.divider(border_color="#2a2a3a", margin_bottom="2em"),
                        rx.markdown(
                            PostState.content,
                            width="100%",
                            color="#d1d5db",
                        ),
                        align_items="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.heading("Post no encontrado", size="7", color="white"),
                        rx.link("← Volver al blog", href="/", color="#86efac"),
                        align_items="start",
                    ),
                ),
                align_items="start",
                width="100%",
                max_width="720px",
                margin="0 auto",
                padding="3em 2em 5em",
            ),
        ),
        rx.box(
            rx.hstack(
                rx.text(
                    "© 2025 El Club de los Marginalistas",
                    font_size="0.8em",
                    color="#6b7280",
                ),
                rx.text(
                    "elclubdelosmarginalistas.com",
                    font_size="0.8em",
                    color="#6b7280",
                ),
                justify="between",
                width="100%",
                max_width="1100px",
                margin="0 auto",
                padding="0 2em",
            ),
            border_top="1px solid #2a2a3a",
            padding="2em 0",
            width="100%",
        ),
        min_height="100vh",
        background="#0c0c0f",
        color="white",
        on_mount=PostState.load_post,
    )