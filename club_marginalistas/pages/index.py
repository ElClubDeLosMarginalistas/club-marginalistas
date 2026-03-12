import reflex as rx
from club_marginalistas.models import Post
from club_marginalistas.utils import get_all_posts
from club_marginalistas.styles import (
    page_wrapper, page_content, navbar, footer,
    newsletter, hero, post_card, filters_bar, empty_state,
    CATEGORIES_FILTER,
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


def posts_grid() -> rx.Component:
    return rx.cond(
        IndexState.filtered_posts.length() > 0,
        rx.grid(
            rx.foreach(IndexState.filtered_posts, post_card),
            columns="3", spacing="4", width="100%",
        ),
        empty_state(),
    )


def index_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        hero(),
        page_content(
            rx.vstack(
                filters_bar(IndexState.active_filter, IndexState.set_filter),
                posts_grid(),
                align_items="start", width="100%",
            ),
        ),
        newsletter(),
        footer(),
        on_mount=IndexState.load_posts,
    )