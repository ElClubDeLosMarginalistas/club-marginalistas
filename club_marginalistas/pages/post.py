import reflex as rx
from club_marginalistas.utils import get_all_posts
from club_marginalistas.styles import (
    colors, fonts, navbar, footer,
    accent_divider, category_tag, page_wrapper
)


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


def post_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        rx.box(
            rx.vstack(
                rx.link(
                    "← Volver al blog",
                    href="/",
                    color=colors["accent"],
                    font_size="0.8em",
                    letter_spacing="0.05em",
                    text_transform="uppercase",
                    font_weight="500",
                    _hover={"color": colors["silver"]},
                    transition="color 0.2s",
                ),
                accent_divider(),
                rx.cond(
                    PostState.found,
                    rx.vstack(
                        rx.hstack(
                            category_tag(PostState.category),
                            rx.text("·", color=colors["border"]),
                            rx.text(PostState.date, font_size="0.7em", color=colors["accent"], opacity="0.7"),
                            spacing="2", align="center",
                        ),
                        rx.heading(
                            PostState.title,
                            font_size="clamp(1.6rem, 3.5vw, 2.5rem)",
                            font_weight="700",
                            line_height="1.2",
                            color=colors["text"],
                            font_family=fonts["serif"],
                            letter_spacing="-0.02em",
                            margin_y="0.75em",
                        ),
                        rx.hstack(
                            rx.box(width="24px", height="24px", border_radius="50%", background=colors["surface"], border=f"1px solid {colors['accent']}"),
                            rx.text(PostState.author, font_size="0.875em", font_weight="500", color=colors["muted"]),
                            spacing="2", align="center",
                            margin_bottom="2em",
                        ),
                        rx.box(height="1px", background=colors["border"], width="100%", margin_bottom="2.5em"),
                        rx.markdown(
                            PostState.content,
                            width="100%",
                            color=colors["muted"],
                            component_map={
                                "h1": lambda text: rx.heading(text, size="7", color=colors["text"], font_family=fonts["serif"], margin_y="1em"),
                                "h2": lambda text: rx.heading(text, size="6", color=colors["text"], font_family=fonts["serif"], margin_y="0.85em"),
                                "h3": lambda text: rx.heading(text, size="5", color=colors["silver"], font_family=fonts["serif"], margin_y="0.75em"),
                                "p": lambda text: rx.text(text, color=colors["muted"], line_height="1.85", margin_bottom="1.25em"),
                            },
                        ),
                        align_items="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.heading("Post no encontrado", size="7", color=colors["text"], font_family=fonts["serif"]),
                        rx.link("← Volver al blog", href="/", color=colors["accent"]),
                        align_items="start", spacing="4",
                    ),
                ),
                align_items="start",
                width="100%",
                max_width="740px",
                margin="0 auto",
                padding="3em 2em 6em",
                spacing="4",
            ),
        ),
        footer(),
        on_mount=PostState.load_post,
    )