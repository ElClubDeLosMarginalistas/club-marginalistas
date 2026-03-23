import reflex as rx
from club_marginalistas.styles import (
    page_wrapper, navbar, footer,
    page_content, panel, section_header,
    accent_divider, back_link, C, fonts, S, G,
)


def page_404() -> rx.Component:
    return page_wrapper(
        navbar(),
        rx.box(
            rx.box(height="1px", background=G["center_h"]),
            rx.box(
                rx.vstack(
                    rx.text("404", font_size="6rem", font_weight="700", color=C["accent"],
                            font_family=fonts["serif"], line_height="1", opacity="0.4"),
                    rx.text("PÁGINA NO ENCONTRADA", font_size="0.7em", color=C["accent"],
                            letter_spacing="0.35em", font_weight="600"),
                    rx.box(width="40px", height="2px", background=C["accent"],
                           border_radius="2px", margin_y="1.5em"),
                    rx.text(
                        "La página que buscás no existe o fue movida.",
                        color=C["muted"], font_size="1em", line_height="1.8",
                        text_align="center",
                    ),
                    rx.box(height="1.5em"),
                    back_link(),
                    align_items="center", spacing="0",
                ),
                display="flex", align_items="center", justify_content="center",
                min_height="70vh",
                max_width=S["page_max"], margin="0 auto", padding="4em 2em",
            ),
            rx.box(height="1px", background=G["border_h"]),
        ),
        footer(),
    )