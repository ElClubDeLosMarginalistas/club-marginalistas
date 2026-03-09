import reflex as rx
from club_marginalistas.utils import get_all_posts


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


def post_card(post) -> rx.Component:
    return rx.link(
        rx.box(
            rx.box(
                rx.text(
                    post.category,
                    font_size="0.65em",
                    color="#86efac",
                    font_weight="600",
                    letter_spacing="0.12em",
                    text_transform="uppercase",
                    margin_bottom="0.75em",
                ),
                rx.heading(
                    post.title,
                    size="4",
                    margin_bottom="0.6em",
                    line_height="1.3",
                    color="white",
                    font_weight="600",
                ),
                rx.text(
                    post.description,
                    color="#9ca3af",
                    font_size="0.85em",
                    line_height="1.65",
                    margin_bottom="1.25em",
                ),
                rx.hstack(
                    rx.text(post.author, font_size="0.78em", font_weight="500", color="#e5e7eb"),
                    rx.text("·", color="#6b7280"),
                    rx.text(post.date, font_size="0.78em", color="#6b7280"),
                    spacing="2",
                ),
                rx.text(
                    "Leer entrada →",
                    font_size="0.78em",
                    color="#86efac",
                    margin_top="1em",
                    font_weight="500",
                ),
                padding="1.4em",
            ),
            border="1px solid #2a2a3a",
            border_radius="12px",
            overflow="hidden",
            background="#13131a",
            height="100%",
            _hover={
                "border_color": "#86efac",
                "background": "#1a1a24",
                "transform": "translateY(-3px)",
                "box_shadow": "0 8px 30px rgba(134,239,172,0.08)",
            },
            transition="all 0.25s ease",
        ),
        href=f"/blog/{post.slug}",
        text_decoration="none",
        _hover={"text_decoration": "none"},
    )


def hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "— Teoría & Análisis Económico",
                font_size="0.75em",
                color="#86efac",
                letter_spacing="0.15em",
                text_transform="uppercase",
                font_weight="500",
            ),
            rx.heading(
                "Ideas que mueven mercados y economías",
                size="8",
                font_weight="700",
                line_height="1.15",
                color="white",
                max_width="600px",
            ),
            rx.text(
                "Análisis profundo, teoría económica accesible y perspectivas sobre la economía contemporánea.",
                color="#9ca3af",
                font_size="1.05em",
                line_height="1.7",
                max_width="500px",
            ),
            align_items="start",
            spacing="4",
            padding="4em 2em 3em",
            max_width="1100px",
            margin="0 auto",
            width="100%",
        ),
    )


def index_page() -> rx.Component:
    posts = get_all_posts()
    return rx.box(
        navbar(),
        hero(),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "ENTRADAS RECIENTES",
                        font_size="0.7em",
                        color="#6b7280",
                        letter_spacing="0.12em",
                        font_weight="500",
                    ),
                    width="100%",
                    border_bottom="1px solid #2a2a3a",
                    padding_bottom="1em",
                    margin_bottom="1.5em",
                ),
                rx.grid(
                    *[post_card(p) for p in posts],
                    columns="3",
                    spacing="4",
                    width="100%",
                ) if posts else rx.text(
                    "No hay entradas aún.",
                    color="#6b7280",
                ),
                align_items="start",
                width="100%",
            ),
            max_width="1100px",
            margin="0 auto",
            padding="0 2em 5em",
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
    )