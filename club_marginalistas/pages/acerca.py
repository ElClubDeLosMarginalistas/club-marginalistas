import reflex as rx
from club_marginalistas.newsletter_state import NewsletterState
from club_marginalistas.styles import (
    page_wrapper, page_content, page_hero,
    navbar, footer, newsletter,
    panel, section_header, info_card, accent_divider,
)


def acerca_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        page_hero("SOBRE NOSOTROS", "Acerca del Club"),
        page_content(
            rx.vstack(
                # Intro
                rx.vstack(
                    rx.text(
                        "El Club de los Marginalistas es un espacio de análisis económico independiente. "
                        "Publicamos ensayos, análisis de coyuntura y reflexiones teóricas sobre economía, "
                        "mercados financieros y política económica desde una perspectiva rigurosa y académica.",
                        line_height="1.85",
                    ),
                    rx.text(
                        "El nombre rinde homenaje a los economistas marginalistas del siglo XIX — Jevons, Menger, Walras — "
                        "quienes transformaron la disciplina al introducir el análisis marginal como herramienta central "
                        "del pensamiento económico. Ese mismo espíritu de rigor, independencia intelectual y disposición "
                        "a cuestionar el consenso guía cada publicación.",
                        line_height="1.85",
                    ),
                    align_items="start", spacing="5", width="100%",
                ),

                # Qué hacemos
                rx.box(height="2.5em"),
                section_header("QUÉ HACEMOS"),
                accent_divider(),
                rx.box(height="1em"),
                rx.grid(
                    info_card("Teoría Económica",    "Análisis de las grandes corrientes del pensamiento económico: escuela austriaca, keynesianismo, monetarismo y sus implicaciones actuales."),
                    info_card("Análisis de Mercados","Seguimiento de mercados financieros globales con enfoque en renta variable, divisas, commodities y tasas de interés."),
                    info_card("Macroeconomía",       "Política fiscal, monetaria y cambiaria. Coyuntura económica de Colombia y América Latina en perspectiva global."),
                    info_card("Microeconomía",       "Teoría del consumidor, organización industrial, competencia y regulación. Casos prácticos y aplicaciones reales."),
                    columns="2", spacing="4", width="100%",
                ),

                # Principios editoriales
                rx.box(height="2.5em"),
                section_header("PRINCIPIOS EDITORIALES"),
                accent_divider(),
                rx.box(height="1em"),
                panel(
                    rx.vstack(
                        info_card("Independencia", "Sin afiliaciones políticas ni intereses comerciales. El análisis sigue la evidencia, no las conveniencias."),
                        info_card("Rigor",         "Cada argumento se sustenta en evidencia empírica o fundamentos teóricos sólidos."),
                        info_card("Claridad",      "El conocimiento económico debe ser accesible. Escribimos para lectores inteligentes, no necesariamente especialistas."),
                        info_card("Largo plazo",   "Evitamos el ruido de corto plazo. Nos interesan las tendencias estructurales, los ciclos y los patrones que perduran."),
                        align_items="start", spacing="3", width="100%",
                    ),
                ),

                # Contacto
                rx.box(height="2.5em"),
                section_header("CONTACTO"),
                accent_divider(),
                rx.box(height="1em"),
                panel(
                    rx.hstack(
                        rx.text("Para colaboraciones, sugerencias o consultas:"),
                        rx.link("elclubdelosmarginalistas@gmail.com", href="mailto:elclubdelosmarginalistas@gmail.com"),
                        spacing="2", align="center", flex_wrap="wrap",
                    ),
                ),

                align_items="start", width="100%", spacing="0",
            ),
        ),
        newsletter(
            NewsletterState.email,
            NewsletterState.set_email,
            NewsletterState.subscribe,
            NewsletterState.message,
        ),
        footer(),
    )