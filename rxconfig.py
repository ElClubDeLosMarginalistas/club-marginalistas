import reflex as rx

config = rx.Config(
    app_name="club_marginalistas",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)