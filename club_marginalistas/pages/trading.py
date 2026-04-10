import reflex as rx
from club_marginalistas.styles import (
    page_wrapper, page_content, page_hero,
    navbar, footer,
    panel, section_header, accent_divider, back_link,
)


def trading_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        page_hero("MARKETS & ANALYSIS", "Trading"),
        page_content(
            rx.vstack(
                accent_divider(),
                rx.box(height="3em"),
                panel(
                    rx.vstack(
                        section_header("COMING SOON"),
                        rx.text(
                            "We are building a section dedicated to technical and fundamental analysis "
                            "of financial markets. Trading ideas, portfolio tracking and "
                            "asset analysis with economic grounding.",
                            line_height="1.85", max_width="560px",
                        ),
                        rx.box(height="0.5em"),
                        rx.text(
                            "Equities · FX · Commodities · Rates · Portfolios",
                            font_size="0.8em",
                        ),
                        rx.box(height="1em"),
                        back_link(),
                        align_items="start", spacing="4",
                    ),
                ),
                align_items="start", width="100%", spacing="0",
            ),
        ),
        footer(),
    )
