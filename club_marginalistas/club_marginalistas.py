import reflex as rx
from club_marginalistas.pages.index import index_page
from club_marginalistas.pages.post import post_page
from club_marginalistas.pages.admin import admin_page


app = rx.App()
app.add_page(index_page, route="/")
app.add_page(post_page, route="/blog/[slug]")
app.add_page(admin_page, route="/admin")