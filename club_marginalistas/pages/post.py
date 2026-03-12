import reflex as rx
from club_marginalistas.utils import get_all_posts
from club_marginalistas.styles import (
    page_wrapper, navbar, footer,
    accent_divider, back_link, post_meta_header,
    markdown_content, post_content_wrapper, fonts, colors
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


def post_found() -> rx.Component:
    return rx.vstack(
        post_meta_header(PostState.category, PostState.date, PostState.title, PostState.author),
        markdown_content(PostState.content),
        align_items="start",
        width="100%",
    )


def post_not_found() -> rx.Component:
    return rx.vstack(
        rx.heading("Post no encontrado", size="7", color=colors["text"], font_family=fonts["serif"]),
        back_link(),
        align_items="start",
        spacing="4",
    )


def post_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        post_content_wrapper(
            back_link(),
            accent_divider(),
            rx.cond(PostState.found, post_found(), post_not_found()),
        ),
        footer(),
        on_mount=PostState.load_post,
    )