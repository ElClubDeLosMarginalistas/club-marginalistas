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
                rx.link("Inicio", href="/", color="#8896aa", font_size="0.8em", letter_spacing="0.05em", text_transform="uppercase", _hover={"color": "#c0c8d8"}, transition="color 0.2s"),
                rx.link("Acerca", href="/acerca", color="#8896aa", font_size="0.8em", letter_spacing="0.05em", text_transform="uppercase", _hover={"color": "#c0c8d8"}, transition="color 0.2s"),
                rx.link("Colaboradores", href="/colaboradores", color="#8896aa", font_size="0.8em", letter_spacing="0.05em", text_transform="uppercase", _hover={"color": "#c0c8d8"}, transition="color 0.2s"),
                rx.link("Trading", href="/trading", color="#8896aa", font_size="0.8em", letter_spacing="0.05em", text_transform="uppercase", _hover={"color": "#c0c8d8"}, transition="color 0.2s"),
                rx.box(
                    rx.hstack(
                        rx.text("ES", font_size="0.75em", color="#c0c8d8", font_weight="600", letter_spacing="0.05em"),
                        rx.box(width="1px", height="12px", background="#4a7fa5"),
                        rx.text("EN", font_size="0.75em", color="#8896aa", font_weight="400", letter_spacing="0.05em"),
                        spacing="2", align="center",
                    ),
                    border="1px solid #2a2a3a", border_radius="4px", padding="0.3em 0.75em",
                    cursor="pointer", _hover={"border_color": "#4a7fa5"}, transition="border-color 0.2s",
                ),
                spacing="6", align="center",
            ),
            justify="between", align="center", width="100%", max_width="1200px", margin="0 auto", padding="0 2em",
        ),
        position="sticky", top="0", z_index="100",
        background="rgba(10,10,13,0.92)", backdrop_filter="blur(20px)",
        border_bottom="1px solid #1e2030", height="64px",
        display="flex", align_items="center", width="100%",
    )


def post_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.link(
                    "← Volver al blog",
                    href="/",
                    color="#4a7fa5",
                    font_size="0.8em",
                    letter_spacing="0.05em",
                    text_transform="uppercase",
                    font_weight="500",
                    _hover={"color": "#c0c8d8"},
                    transition="color 0.2s",
                ),
                rx.box(height="1px", background="linear-gradient(90deg, #4a7fa5, transparent)", width="100%", margin_y="2em"),
                rx.cond(
                    PostState.found,
                    rx.vstack(
                        rx.hstack(
                            rx.text(PostState.category, font_size="0.7em", color="#4a7fa5", font_weight="600", letter_spacing="0.15em", text_transform="uppercase"),
                            rx.text("·", color="#1e2030"),
                            rx.text(PostState.date, font_size="0.7em", color="#4a7fa5", opacity="0.7"),
                            spacing="2", align="center",
                        ),
                        rx.heading(
                            PostState.title,
                            font_size="clamp(1.6rem, 3.5vw, 2.5rem)",
                            font_weight="700",
                            line_height="1.2",
                            color="#e8eaf0",
                            font_family="Georgia, serif",
                            letter_spacing="-0.02em",
                            margin_y="0.75em",
                        ),
                        rx.hstack(
                            rx.box(width="24px", height="24px", border_radius="50%", background="#0f1219", border="1px solid #4a7fa5"),
                            rx.text(PostState.author, font_size="0.875em", font_weight="500", color="#8896aa"),
                            spacing="2", align="center",
                            margin_bottom="2em",
                        ),
                        rx.box(height="1px", background="#1e2030", width="100%", margin_bottom="2.5em"),
                        rx.markdown(
                            PostState.content,
                            width="100%",
                            color="#c0c8d8",
                            component_map={
                                "h1": lambda text: rx.heading(text, size="7", color="#e8eaf0", font_family="Georgia, serif", margin_y="1em"),
                                "h2": lambda text: rx.heading(text, size="6", color="#e8eaf0", font_family="Georgia, serif", margin_y="0.85em"),
                                "h3": lambda text: rx.heading(text, size="5", color="#c0c8d8", font_family="Georgia, serif", margin_y="0.75em"),
                                "p": lambda text: rx.text(text, color="#8896aa", line_height="1.85", margin_bottom="1.25em", font_size="1em"),
                            },
                        ),
                        align_items="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.heading("Post no encontrado", size="7", color="#e8eaf0", font_family="Georgia, serif"),
                        rx.link("← Volver al blog", href="/", color="#4a7fa5"),
                        align_items="start",
                        spacing="4",
                    ),
                ),
                align_items="start",
                width="100%",
                max_width="740px",
                margin="0 auto",
                padding="3em 2em 6em",
            ),
        ),
        rx.box(
            rx.hstack(
                rx.text("© 2025 El Club de los Marginalistas", font_size="0.75em", color="#4a5568"),
                rx.text("elclubdelosmarginalistas.com", font_size="0.75em", color="#4a7fa5"),
                justify="between",
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding="0 2em",
            ),
            border_top="1px solid #1e2030",
            padding="2.5em 0",
            background="#0a0a0d",
        ),
        min_height="100vh",
        background="#0a0a0d",
        color="#e8eaf0",
        on_mount=PostState.load_post,
    )