import reflex as rx
from club_marginalistas.styles import (
    page_wrapper, page_content, page_hero,
    navbar, footer, newsletter,
    panel, section_header, author_card, accent_divider,
)


def colaboradores_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        page_hero("EL EQUIPO", "Colaboradores"),
        page_content(
            rx.vstack(
                rx.text(
                    "Las personas detrás del análisis. Economistas, analistas e investigadores "
                    "comprometidos con el pensamiento económico riguroso e independiente.",
                    line_height="1.8", max_width="600px",
                ),
                rx.box(height="2em"),

                # Tarjeta Diego
                panel(
                    rx.vstack(
                        author_card(
                            "DH",
                            "Diego Herrera Castañeda",
                            "Fundador · Economista · Analista de Datos",
                            "Economista e Ingeniero de Sistemas de la Universidad EAN, con International MBA "
                            "en curso en Westfield Business School. Especializado en análisis de datos para "
                            "la toma de decisiones estratégicas, con experiencia en los sectores financiero "
                            "y corporativo en entidades como Skandia y Colfondos.",
                        ),
                        accent_divider(),
                        rx.hstack(
                            rx.vstack(
                                section_header("HABILIDADES"),
                                rx.text("Python · SQL · Power BI · Excel · Tableau", font_size="0.82em"),
                                align_items="start", spacing="2",
                            ),
                            rx.vstack(
                                section_header("IDIOMAS"),
                                rx.text("Español (Nativo) · Inglés (C1)", font_size="0.82em"),
                                align_items="start", spacing="2",
                            ),
                            rx.link(
                                "LinkedIn →",
                                href="https://linkedin.com/in/diego-herrera-b5187456",
                                is_external=True,
                                font_size="0.82em",
                            ),
                            justify="between", align="end", width="100%",
                        ),
                        align_items="start", spacing="4", width="100%",
                    ),
                ),

                # CTA colaborar
                rx.box(height="2em"),
                panel(
                    rx.vstack(
                        section_header("¿QUERÉS COLABORAR?"),
                        rx.text(
                            "Si sos economista, analista o investigador y querés publicar en el Club, escribinos.",
                            font_size="0.88em", line_height="1.6",
                        ),
                        rx.link("elclubdelosmarginalistas@gmail.com", href="mailto:elclubdelosmarginalistas@gmail.com"),
                        align_items="start", spacing="3",
                    ),
                ),

                align_items="start", width="100%", spacing="0",
            ),
        ),
        newsletter(),
        footer(),
    )