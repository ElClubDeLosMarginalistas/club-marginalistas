import reflex as rx
from club_marginalistas.models import Colaborador, Post
from club_marginalistas.utils import get_all_colaboradores, get_colaborador_by_slug, get_posts_by_author
from club_marginalistas.newsletter_state import NewsletterState
from club_marginalistas.styles import (
    page_wrapper, page_content, page_hero,
    navbar, footer, newsletter,
    panel, section_header, accent_divider,
    empty_state, category_tag, back_link,
    C, fonts, G, S,
)


# ============================================
# ESTADOS
# ============================================

class ColaboradoresState(rx.State):
    colaboradores: list[Colaborador] = []

    def load(self):
        self.colaboradores = get_all_colaboradores()


class ColaboradorState(rx.State):
    colaborador: Colaborador = Colaborador()
    posts:       list[Post]  = []
    found:       bool        = False

    def load(self):
        slug = self.router.page.params.get("slug", "")
        c = get_colaborador_by_slug(slug)
        if c:
            self.colaborador = c
            self.posts       = get_posts_by_author(c.name)
            self.found       = True
        else:
            self.colaborador = Colaborador()
            self.posts       = []
            self.found       = False


# ============================================
# COMPONENTES
# ============================================

def social_link(label: str, url, icon: str) -> rx.Component:
    return rx.cond(
        url != "",
        rx.link(
            rx.hstack(
                rx.text(icon, font_size="0.9em"),
                rx.text(label, font_size="0.78em", color=C["accent"],
                        font_weight="500", letter_spacing="0.03em"),
                spacing="2", align="center",
            ),
            href=url, is_external=True,
            _hover={"opacity": "0.75"}, transition="opacity 0.2s",
        ),
    )


def skill_chip(skill: str) -> rx.Component:
    return rx.box(
        rx.text(skill, font_size="0.7em", color=C["accent"], font_weight="500"),
        border=f"1px solid {C['border']}",
        border_radius="3px", padding="0.2em 0.65em",
        background=C["bg"],
    )


def colaborador_card(c: Colaborador) -> rx.Component:
    return rx.link(
        rx.box(
            rx.box(height="2px", background=G["accent_h"]),
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.text(c.initials, font_size="1.2em", font_weight="700",
                                color=C["accent"], font_family=fonts["serif"]),
                        width="56px", height="56px", border_radius="50%",
                        background=C["bg"], border=f"2px solid {C['accent']}",
                        display="flex", align_items="center", justify_content="center",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(c.name, font_size="1em", font_weight="700",
                                color=C["text"], font_family=fonts["serif"]),
                        rx.text(c.role, font_size="0.78em", color=C["accent"],
                                letter_spacing="0.03em"),
                        align_items="start", spacing="1",
                    ),
                    spacing="4", align="center", width="100%",
                ),
                rx.text(c.bio, color=C["dim2"], font_size="0.82em",
                        line_height="1.65", margin_top="1em"),
                rx.text("Ver perfil →", font_size="0.78em", color=C["accent"],
                        font_weight="500", letter_spacing="0.05em", margin_top="1.25em"),
                padding="1.4em",
            ),
            border=f"1px solid {C['border']}",
            border_radius="6px", background=C["surface"],
            overflow="hidden", transition="all 0.25s ease",
            _hover={
                "border_color": C["accent"], "background": C["surface2"],
                "transform": "translateY(-2px)",
                "box_shadow": "0 8px 30px rgba(74,127,165,0.1)",
            },
        ),
        href=f"/colaboradores/{c.slug}",
        text_decoration="none", _hover={"text_decoration": "none"},
    )


def post_row(post: Post) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.vstack(
                rx.text(post.title, font_weight="500", font_size="0.9em", color=C["text"]),
                rx.hstack(
                    category_tag(post.category),
                    rx.text(post.date, font_size="0.65em", color=C["muted"]),
                    spacing="2", align="center",
                ),
                align_items="start", spacing="1",
            ),
            rx.text("Leer →", font_size="0.78em", color=C["accent"], font_weight="500"),
            justify="between", align="center", width="100%",
            padding="0.85em 0", border_bottom=f"1px solid {C['border']}",
        ),
        href=f"/blog/{post.slug}",
        text_decoration="none", _hover={"text_decoration": "none"},
    )


def perfil_completo() -> rx.Component:
    c = ColaboradorState.colaborador
    return rx.vstack(
        # Header
        rx.hstack(
            rx.box(
                rx.text(c.initials, font_size="2em", font_weight="700",
                        color=C["accent"], font_family=fonts["serif"]),
                width="88px", height="88px", border_radius="50%",
                background=C["surface"], border=f"2px solid {C['accent']}",
                display="flex", align_items="center", justify_content="center",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(c.name, font_size="clamp(1.4rem, 3vw, 2rem)",
                        font_weight="700", color=C["text"], font_family=fonts["serif"]),
                rx.text(c.role, font_size="0.88em", color=C["accent"], letter_spacing="0.04em"),
                align_items="start", spacing="1",
            ),
            spacing="5", align="center", width="100%",
        ),

        # Bio
        rx.cond(
            c.bio != "",
            rx.text(c.bio, color=C["muted"], font_size="0.95em", line_height="1.85"),
        ),

        accent_divider(),

        # Skills e idiomas
        rx.grid(
            rx.cond(
                c.skills != "",
                rx.vstack(
                    section_header("HABILIDADES TÉCNICAS"),
                    rx.hstack(
                        rx.foreach(
                            c.skills.split(","),
                            lambda s: skill_chip(s),
                        ),
                        flex_wrap="wrap", spacing="2",
                    ),
                    align_items="start", spacing="3",
                ),
            ),
            rx.cond(
                c.languages != "",
                rx.vstack(
                    section_header("IDIOMAS"),
                    rx.text(c.languages, font_size="0.85em", color=C["muted"]),
                    align_items="start", spacing="3",
                ),
            ),
            columns="2", spacing="6", width="100%",
        ),

        accent_divider(),

        # Redes sociales
        rx.vstack(
            section_header("CONTACTO Y REDES"),
            rx.hstack(
                social_link("LinkedIn",  c.linkedin,  "in"),
                social_link("GitHub",    c.github,    "gh"),
                social_link("X/Twitter", c.twitter,   "𝕏"),
                social_link("Instagram", c.instagram, "ig"),
                social_link("YouTube",   c.youtube,   "▶"),
                rx.cond(
                    c.email_public != "",
                    rx.link(
                        rx.hstack(
                            rx.text("✉", font_size="0.9em"),
                            rx.text(c.email_public, font_size="0.78em", color=C["accent"],
                                    font_weight="500"),
                            spacing="2", align="center",
                        ),
                        href=rx.Var.create(f"mailto:{c.email_public}"),
                        _hover={"opacity": "0.75"},
                    ),
                ),
                flex_wrap="wrap", spacing="5",
            ),
            align_items="start", spacing="3", width="100%",
        ),

        accent_divider(),

        # Posts publicados
        section_header("ENTRADAS PUBLICADAS"),
        rx.cond(
            ColaboradorState.posts.length() > 0,
            rx.vstack(
                rx.foreach(ColaboradorState.posts, post_row),
                width="100%", spacing="0",
            ),
            empty_state("Este colaborador aún no tiene entradas publicadas."),
        ),

        align_items="start", width="100%", spacing="5",
    )


# ============================================
# PÁGINAS
# ============================================

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
                rx.grid(
                    rx.foreach(ColaboradoresState.colaboradores, colaborador_card),
                    columns="2", spacing="4", width="100%",
                ),
                rx.box(height="2em"),
                panel(
                    rx.vstack(
                        section_header("¿QUERÉS COLABORAR?"),
                        rx.text(
                            "Si sos economista, analista o investigador y querés publicar en el Club, escribinos.",
                            font_size="0.88em", line_height="1.6",
                        ),
                        rx.link("elclubdelosmarginalistas@gmail.com",
                                href="mailto:elclubdelosmarginalistas@gmail.com"),
                        align_items="start", spacing="3",
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
        on_mount=ColaboradoresState.load,
    )


def colaborador_page() -> rx.Component:
    return page_wrapper(
        navbar(),
        rx.box(
            rx.vstack(
                back_link("← Ver colaboradores", "/colaboradores"),
                accent_divider(),
                rx.cond(
                    ColaboradorState.found,
                    perfil_completo(),
                    rx.vstack(
                        rx.heading("Colaborador no encontrado", size="6", color=C["text"]),
                        back_link("← Ver colaboradores", "/colaboradores"),
                        align_items="start", spacing="4",
                    ),
                ),
                align_items="start", width="100%",
                max_width="740px", margin="0 auto",
                padding="3em 2em 6em", spacing="4",
            ),
        ),
        footer(),
        on_mount=ColaboradorState.load,
    )