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


def post_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.link(
                "← Volver al blog",
                href="/",
                color="#86efac",
                font_size="0.875em",
                margin_bottom="2em",
            ),
            rx.cond(
                PostState.found,
                rx.vstack(
                    rx.text(
                        PostState.category,
                        font_size="0.7em",
                        color="green",
                        font_weight="600",
                        letter_spacing="0.1em",
                        text_transform="uppercase",
                        margin_bottom="0.75em",
                    ),
                    rx.heading(
                        PostState.title,
                        size="9",
                        font_weight="700",
                        line_height="1.15",
                        margin_bottom="0.75em",
                    ),
                    rx.hstack(
                        rx.text(PostState.author, font_size="0.9em", font_weight="500"),
                        rx.text("·", color="gray"),
                        rx.text(PostState.date, font_size="0.9em", color="gray"),
                        margin_bottom="2.5em",
                    ),
                    rx.divider(border_color="#2a2a3a", margin_bottom="2.5em"),
                    rx.markdown(PostState.content, width="100%"),
                    align_items="start",
                    width="100%",
                ),
                rx.heading("Post no encontrado", size="8"),
            ),
            align_items="start",
            width="100%",
            max_width="720px",
            margin="0 auto",
            padding="3em 2em",
        ),
        min_height="100vh",
        background="#0c0c0f",
        color="white",
        on_mount=PostState.load_post,
    )