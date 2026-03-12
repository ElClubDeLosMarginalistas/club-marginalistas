import reflex as rx
from club_marginalistas.models import Post
from club_marginalistas.utils import get_all_posts
from club_marginalistas.styles import (
    colors, spacing, page_wrapper, page_content,
    navbar, footer, newsletter, section_header,
    hero, post_card, page_wrapper
)

CATEGORIES = ["Todas", "Teoría", "Macro", "Micro", "General"]


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


def filter_btn(cat: str) -> rx.Component:
    return rx.button(
        cat,
        on_click=lambda: IndexState.set_filter(cat),
        background=rx.cond(IndexState.active_filter == cat, colors["accent"], "transparent"),
        color=rx.cond(IndexState.active_filter == cat, colors["text"], colors["dim2"]),
        border=rx.cond(IndexState.active_filter == cat, f"1px solid {colors['accent']}", f"1px solid {colors['border']}"),
        border_radius="3px", font_size="0.72em", letter_spacing="0.05em",
        padding="0.3em 0.85em", cursor="pointer",
        _hover={"border_color": colors["accent"], "color": colors["silver"]},
        transition="all 0.2s",
    )


def filters_bar() -> rx.Component:
    return rx.hstack(
        section_header("ENTRADAS RECIENTES"),
        rx.hstack(rx.foreach(CATEGORIES, filter_btn), spacing="2"),
        justify="between", align="center", width="100%",
        border_bottom=f"1px solid {colors['border']}",
        padding_bottom="1.25em", margin_bottom="2em",
    )


def posts_grid() -> rx.Component:
    return rx.cond(
        IndexState.filtered_posts.length() > 0,
        rx.grid(rx.foreach(IndexState.filtered_posts, post_card), columns="3", spacing="4", width="100%"),
        rx.box(rx.text("No hay entradas en esta categoría.", color=colors["accent"], font_size="0.9em"), padding="3em 0"),
    )


def index_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        hero(),
        page_content(
            rx.vstack(filters_bar(), posts_grid(), align_items="start", width="100%"),
        ),
        newsletter(),
        footer(),
        on_mount=IndexState.load_posts,
    )