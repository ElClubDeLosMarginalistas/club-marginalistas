import reflex as rx
from club_marginalistas.styles import (
    page_wrapper, page_content, page_hero,
    navbar, footer,
    panel, section_header, accent_divider, back_link,
)


def trading_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        page_hero("MERCADOS & ANÁLISIS", "Trading"),
        page_content(
            rx.vstack(
                accent_divider(),
                rx.box(height="3em"),
                panel(
                    rx.vstack(
                        section_header("PRÓXIMAMENTE"),
                        rx.text(
                            "Estamos construyendo una sección dedicada al análisis técnico y fundamental "
                            "de mercados financieros. Ideas de trading, seguimiento de portafolios y "
                            "análisis de activos con fundamento económico.",
                            line_height="1.85", max_width="560px",
                        ),
                        rx.box(height="0.5em"),
                        rx.text(
                            "Renta Variable · Divisas · Commodities · Tasas · Portafolios",
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