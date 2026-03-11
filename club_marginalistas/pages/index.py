import reflex as rx
from club_marginalistas.utils import get_all_posts
from club_marginalistas.models import Post


class IndexState(rx.State):
    posts: list[Post] = []
    active_filter: str = "Todas"

    def load_posts(self):
        self.posts = get_all_posts()

    def set_filter(self, category: str):
        self.active_filter = category

    @rx.var
    def filtered_posts(self) -> list[Post]:
        if self.active_filter == "Todas":
            return self.posts
        return [p for p in self.posts if p.category.lower() == self.active_filter.lower()]


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


def hero() -> rx.Component:
    return rx.box(
        rx.box(
            # Decorative line top
            rx.box(height="1px", background="linear-gradient(90deg, transparent, #4a7fa5, transparent)", margin_bottom="3em"),
            rx.vstack(
                rx.hstack(
                    rx.box(width="2px", height="40px", background="#4a7fa5"),
                    rx.vstack(
                        rx.text(
                            "ANÁLISIS · TEORÍA · MERCADOS",
                            font_size="0.7em",
                            color="#4a7fa5",
                            letter_spacing="0.2em",
                            font_weight="500",
                        ),
                        rx.heading(
                            "El Club de los Marginalistas",
                            font_size="clamp(1.8rem, 4vw, 3rem)",
                            font_weight="700",
                            color="#e8eaf0",
                            font_family="Georgia, serif",
                            letter_spacing="-0.02em",
                            line_height="1.15",
                        ),
                        align_items="start",
                        spacing="2",
                    ),
                    spacing="4",
                    align="center",
                ),
                rx.text(
                    "Pensamiento económico riguroso. Análisis de mercados, teoría y política económica desde una perspectiva académica e independiente.",
                    color="#8896aa",
                    font_size="1em",
                    line_height="1.8",
                    max_width="580px",
                ),
                rx.hstack(
                    rx.box(
                        rx.text("Explorar entradas →", font_size="0.85em", color="#c0c8d8", font_weight="500", letter_spacing="0.05em"),
                        border="1px solid #4a7fa5",
                        border_radius="4px",
                        padding="0.6em 1.4em",
                        cursor="pointer",
                        _hover={"background": "#4a7fa5", "color": "white"},
                        transition="all 0.2s",
                    ),
                    spacing="4",
                ),
                align_items="start",
                spacing="5",
            ),
            rx.box(height="1px", background="linear-gradient(90deg, transparent, #1e2030, transparent)", margin_top="3em"),
            max_width="1200px",
            margin="0 auto",
            padding="4em 2em",
        ),
    )


def post_card(post: Post) -> rx.Component:
    return rx.link(
        rx.box(
            # Top accent line
            rx.box(height="2px", background="linear-gradient(90deg, #4a7fa5, transparent)"),
            rx.box(
                rx.hstack(
                    rx.text(
                        post.category,
                        font_size="0.65em",
                        color="#4a7fa5",
                        font_weight="600",
                        letter_spacing="0.15em",
                        text_transform="uppercase",
                    ),
                    rx.text(
                        post.date,
                        font_size="0.65em",
                        color="#4a7fa5",
                        font_family="Georgia, serif",
                        opacity="0.7",
                    ),
                    justify="between",
                    width="100%",
                    margin_bottom="0.85em",
                ),
                rx.heading(
                    post.title,
                    size="4",
                    margin_bottom="0.75em",
                    line_height="1.3",
                    color="#e8eaf0",
                    font_weight="600",
                    font_family="Georgia, serif",
                ),
                rx.text(
                    post.description,
                    color="#6b7a8d",
                    font_size="0.85em",
                    line_height="1.7",
                    margin_bottom="1.5em",
                ),
                rx.hstack(
                    rx.hstack(
                        rx.box(width="18px", height="18px", border_radius="50%", background="#1e2030", border="1px solid #4a7fa5"),
                        rx.text(post.author, font_size="0.78em", font_weight="500", color="#8896aa"),
                        spacing="2", align="center",
                    ),
                    rx.text(
                        "Leer →",
                        font_size="0.78em",
                        color="#4a7fa5",
                        font_weight="500",
                        letter_spacing="0.05em",
                    ),
                    justify="between",
                    width="100%",
                ),
                padding="1.4em",
            ),
            border="1px solid #1e2030",
            border_radius="6px",
            overflow="hidden",
            background="#0f1219",
            height="100%",
            _hover={
                "border_color": "#4a7fa5",
                "background": "#111827",
                "transform": "translateY(-2px)",
                "box_shadow": "0 8px 30px rgba(74,127,165,0.1)",
            },
            transition="all 0.25s ease",
        ),
        href=f"/blog/{post.slug}",
        text_decoration="none",
        _hover={"text_decoration": "none"},
    )


def index_page() -> rx.Component:
    return rx.box(
        navbar(),
        hero(),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        rx.box(width="3px", height="16px", background="#4a7fa5", border_radius="2px"),
                        rx.text("ENTRADAS RECIENTES", font_size="0.7em", color="#8896aa", letter_spacing="0.15em", font_weight="600"),
                        spacing="3", align="center",
                    ),
                    rx.hstack(
                        rx.foreach(
                            ["Todas", "Teoría", "Macro", "Micro", "General"],
                            lambda cat: rx.button(
                                cat,
                                on_click=lambda: IndexState.set_filter(cat),
                                background=rx.cond(IndexState.active_filter == cat, "#4a7fa5", "transparent"),
                                color=rx.cond(IndexState.active_filter == cat, "#e8eaf0", "#6b7a8d"),
                                border=rx.cond(IndexState.active_filter == cat, "1px solid #4a7fa5", "1px solid #1e2030"),
                                border_radius="3px",
                                font_size="0.72em",
                                letter_spacing="0.05em",
                                padding="0.3em 0.85em",
                                cursor="pointer",
                                _hover={"border_color": "#4a7fa5", "color": "#c0c8d8"},
                                transition="all 0.2s",
                            ),
                        ),
                        spacing="2",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    border_bottom="1px solid #1e2030",
                    padding_bottom="1.25em",
                    margin_bottom="2em",
                ),
                rx.cond(
                    IndexState.filtered_posts.length() > 0,
                    rx.grid(
                        rx.foreach(IndexState.filtered_posts, post_card),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    rx.box(
                        rx.text("No hay entradas en esta categoría.", color="#4a7fa5", font_size="0.9em"),
                        padding="3em 0",
                    ),
                ),
                align_items="start",
                width="100%",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="0 2em 5em",
        ),
        # NEWSLETTER
        rx.box(
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.hstack(
                            rx.box(width="3px", height="16px", background="#4a7fa5", border_radius="2px"),
                            rx.text("NEWSLETTER", font_size="0.7em", color="#4a7fa5", letter_spacing="0.15em", font_weight="600"),
                            spacing="3", align="center",
                        ),
                        rx.heading("Análisis directo a tu correo", size="5", color="#e8eaf0", font_family="Georgia, serif"),
                        rx.text("Sin ruido. Solo economía.", color="#6b7a8d", font_size="0.875em"),
                        align_items="start",
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="tu@correo.com",
                            background="#0a0a0d",
                            border="1px solid #1e2030",
                            color="#e8eaf0",
                            border_radius="4px",
                            padding="0.65em 1em",
                            width="260px",
                            _focus={"border_color": "#4a7fa5"},
                            _placeholder={"color": "#4a5568"},
                        ),
                        rx.button(
                            "Suscribirse",
                            background="#4a7fa5",
                            color="#e8eaf0",
                            font_weight="600",
                            font_size="0.875em",
                            border_radius="4px",
                            padding="0.65em 1.4em",
                            cursor="pointer",
                            border="none",
                            _hover={"background": "#5a8fb5"},
                            transition="background 0.2s",
                        ),
                        spacing="3",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                ),
                max_width="1200px",
                margin="0 auto",
                padding="3em 2em",
            ),
            border_top="1px solid #1e2030",
            border_bottom="1px solid #1e2030",
            background="#0a0a0d",
        ),
        # FOOTER
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("El Club de los Marginalistas", font_size="0.85em", color="#c0c8d8", font_weight="600", font_family="Georgia, serif"),
                    rx.text("Pensamiento económico independiente.", font_size="0.75em", color="#4a5568"),
                    rx.text("elclubdelosmarginalistas.com", font_size="0.75em", color="#4a7fa5"),
                    align_items="start",
                    spacing="1",
                ),
                rx.hstack(
                    rx.link("Inicio", href="/", font_size="0.75em", color="#6b7a8d", _hover={"color": "#c0c8d8"}),
                    rx.link("Acerca", href="/acerca", font_size="0.75em", color="#6b7a8d", _hover={"color": "#c0c8d8"}),
                    rx.link("Colaboradores", href="/colaboradores", font_size="0.75em", color="#6b7a8d", _hover={"color": "#c0c8d8"}),
                    rx.link("Trading", href="/trading", font_size="0.75em", color="#6b7a8d", _hover={"color": "#c0c8d8"}),
                    spacing="5",
                ),
                rx.text("© 2025 El Club de los Marginalistas", font_size="0.75em", color="#4a5568"),
                justify="between",
                align="center",
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
        on_mount=IndexState.load_posts,
    )