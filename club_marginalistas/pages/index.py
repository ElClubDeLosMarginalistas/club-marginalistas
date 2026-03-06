import reflex as rx
from club_marginalistas.utils import get_all_posts


def post_card(post) -> rx.Component:
    return rx.link(
        rx.box(
            rx.box(
                rx.text(
                    post.category,
                    font_size="0.7em",
                    color="green",
                    font_weight="600",
                    letter_spacing="0.1em",
                    text_transform="uppercase",
                    margin_bottom="0.5em",
                ),
                rx.heading(
                    post.title,
                    size="4",
                    margin_bottom="0.5em",
                    line_height="1.3",
                ),
                rx.text(
                    post.description,
                    color="gray",
                    font_size="0.875em",
                    line_height="1.6",
                    margin_bottom="1em",
                ),
                rx.hstack(
                    rx.text(post.author, font_size="0.8em", font_weight="500"),
                    rx.text("·", color="gray"),
                    rx.text(post.date, font_size="0.8em", color="gray"),
                ),
                padding="1.25em",
            ),
            border="1px solid #2a2a3a",
            border_radius="12px",
            overflow="hidden",
            background="#13131a",
            _hover={
                "border_color": "#86efac",
                "transform": "translateY(-3px)",
                "transition": "all 0.2s",
            },
            transition="all 0.2s",
        ),
        href=f"/blog/{post.slug}",
    )


def index_page() -> rx.Component:
    posts = get_all_posts()
    return rx.box(
        rx.vstack(
            rx.heading(
                "El Club de los Marginalistas",
                size="9",
                font_weight="700",
                margin_bottom="0.25em",
            ),
            rx.text(
                "Teoría y análisis económico",
                color="gray",
                font_size="1.1em",
                margin_bottom="2em",
            ),
            rx.grid(
                *[post_card(p) for p in posts],
                columns="3",
                spacing="4",
                width="100%",
            ) if posts else rx.text(
                "No hay entradas aún.",
                color="gray",
            ),
            align_items="start",
            width="100%",
            max_width="1100px",
            margin="0 auto",
            padding="3em 2em",
        ),
        min_height="100vh",
        background="#0c0c0f",
        color="white",
    )