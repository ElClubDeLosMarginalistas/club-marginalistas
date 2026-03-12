import reflex as rx
from club_marginalistas.utils import get_all_posts
from club_marginalistas.models import Post
from club_marginalistas.styles import (
    colors, fonts, card_style, input_style,
    navbar, footer, newsletter, section_header,
    accent_divider, category_tag, btn_primary, btn_outline, page_wrapper
)


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


def post_card(post: Post) -> rx.Component:
    return rx.link(
        rx.box(
            rx.box(height="2px", background=f"linear-gradient(90deg, {colors['accent']}, transparent)"),
            rx.box(
                rx.hstack(
                    category_tag(post.category),
                    rx.text(post.date, font_size="0.65em", color=colors["accent"], opacity="0.7"),
                    justify="between", width="100%", margin_bottom="0.85em",
                ),
                rx.heading(post.title, size="4", margin_bottom="0.75em", line_height="1.3", color=colors["text"], font_weight="600", font_family=fonts["serif"]),
                rx.text(post.description, color=colors["dim2"], font_size="0.85em", line_height="1.7", margin_bottom="1.5em"),
                rx.hstack(
                    rx.hstack(
                        rx.box(width="24px", height="24px", border_radius="50%", background=colors["surface"], border=f"1px solid {colors['accent']}"),
                        rx.text(post.author, font_size="0.78em", font_weight="500", color=colors["muted"]),
                        spacing="2", align="center",
                    ),
                    rx.text("Leer →", font_size="0.78em", color=colors["accent"], font_weight="500", letter_spacing="0.05em"),
                    justify="between", width="100%",
                ),
                padding="1.4em",
            ),
            **card_style,
        ),
        href=f"/blog/{post.slug}",
        text_decoration="none",
        _hover={"text_decoration": "none"},
    )


def hero() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(height="1px", background=f"linear-gradient(90deg, transparent, {colors['accent']}, transparent)", margin_bottom="3em"),
            rx.vstack(
                rx.hstack(
                    rx.box(width="2px", height="40px", background=colors["accent"]),
                    rx.vstack(
                        rx.text("ANÁLISIS · TEORÍA · MERCADOS", font_size="0.7em", color=colors["accent"], letter_spacing="0.2em", font_weight="500"),
                        rx.heading("El Club de los Marginalistas", font_size="clamp(1.8rem, 4vw, 3rem)", font_weight="700", color=colors["text"], font_family=fonts["serif"], letter_spacing="-0.02em", line_height="1.15"),
                        align_items="start", spacing="2",
                    ),
                    spacing="4", align="center",
                ),
                rx.text("Pensamiento económico riguroso. Análisis de mercados, teoría y política económica desde una perspectiva académica e independiente.", color=colors["muted"], font_size="1em", line_height="1.8", max_width="580px"),
                btn_outline("Explorar entradas →"),
                align_items="start", spacing="5",
            ),
            rx.box(height="1px", background=f"linear-gradient(90deg, transparent, {colors['border']}, transparent)", margin_top="3em"),
            max_width="1200px", margin="0 auto", padding="4em 2em",
        ),
    )


def filters() -> rx.Component:
    return rx.hstack(
        section_header("ENTRADAS RECIENTES"),
        rx.hstack(
            rx.foreach(
                ["Todas", "Teoría", "Macro", "Micro", "General"],
                lambda cat: rx.button(
                    cat,
                    on_click=lambda: IndexState.set_filter(cat),
                    background=rx.cond(IndexState.active_filter == cat, colors["accent"], "transparent"),
                    color=rx.cond(IndexState.active_filter == cat, colors["text"], colors["dim2"]),
                    border=rx.cond(IndexState.active_filter == cat, f"1px solid {colors['accent']}", f"1px solid {colors['border']}"),
                    border_radius="3px", font_size="0.72em", letter_spacing="0.05em",
                    padding="0.3em 0.85em", cursor="pointer",
                    _hover={"border_color": colors["accent"], "color": colors["silver"]},
                    transition="all 0.2s",
                ),
            ),
            spacing="2",
        ),
        justify="between", align="center", width="100%",
        border_bottom=f"1px solid {colors['border']}",
        padding_bottom="1.25em", margin_bottom="2em",
    )


def index_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        hero(),
        rx.box(
            rx.vstack(
                filters(),
                rx.cond(
                    IndexState.filtered_posts.length() > 0,
                    rx.grid(rx.foreach(IndexState.filtered_posts, post_card), columns="3", spacing="4", width="100%"),
                    rx.box(rx.text("No hay entradas en esta categoría.", color=colors["accent"], font_size="0.9em"), padding="3em 0"),
                ),
                align_items="start", width="100%",
            ),
            max_width="1200px", margin="0 auto", padding="0 2em 5em",
        ),
        newsletter(),
        footer(),
        on_mount=IndexState.load_posts,
    )