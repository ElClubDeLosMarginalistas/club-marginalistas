import reflex as rx

# ============================================
# ESTILOS GLOBALES — El Club de los Marginalistas
# ============================================

# --- PALETA ---
C = {
    "bg":          "#0a0a0d",
    "surface":     "#0f1219",
    "surface2":    "#111827",
    "border":      "#1e2030",
    "accent":      "#4a7fa5",
    "accent2":     "#5a8fb5",
    "text":        "#e8eaf0",
    "muted":       "#8896aa",
    "silver":      "#c0c8d8",
    "dim":         "#4a5568",
    "dim2":        "#6b7a8d",
    "danger":      "#ef4444",
    "danger_bg":   "#2a1a1a",
    "danger_dim":  "#6b3a3a",
}

# mantener alias `colors` para compatibilidad con post.py / otros módulos
colors = C

# --- TIPOGRAFÍA ---
fonts = {
    "serif": "Georgia, serif",
    "sans":  "system-ui, sans-serif",
}

# --- GRADIENTES ---
G = {
    "accent_h": f"linear-gradient(90deg, {C['accent']}, transparent)",
    "center_h": f"linear-gradient(90deg, transparent, {C['accent']}, transparent)",
    "border_h": f"linear-gradient(90deg, transparent, {C['border']}, transparent)",
}

# --- ESPACIADO ---
S = {
    "page_x":    "2em",
    "page_max":  "1200px",
    "post_max":  "740px",
    "admin_max": "960px",
}

# --- CATEGORÍAS ---
CATEGORIES_FILTER = ["Todas", "Teoría", "Macro", "Micro", "General"]
CATEGORIES_FORM   = ["General", "Teoría", "Macro", "Micro"]

# ============================================
# ESTILOS BASE (dict reutilizables)
# ============================================

_input_base = {
    "background":   C["bg"],
    "border":       f"1px solid {C['border']}",
    "color":        C["text"],
    "border_radius": "4px",
    "width":        "100%",
    "_focus":       {"border_color": C["accent"]},
    "_placeholder": {"color": C["dim"]},
}

input_style    = _input_base
textarea_style = {**_input_base, "min_height": "280px"}
select_style   = {
    "background":    C["bg"],
    "border":        f"1px solid {C['border']}",
    "color":         C["text"],
    "border_radius": "4px",
    "width":         "100%",
}

card_style = {
    "border":        f"1px solid {C['border']}",
    "border_radius": "6px",
    "background":    C["surface"],
    "height":        "100%",
    "overflow":      "hidden",
    "transition":    "all 0.25s ease",
    "_hover": {
        "border_color": C["accent"],
        "background":   C["surface2"],
        "transform":    "translateY(-2px)",
        "box_shadow":   "0 8px 30px rgba(74,127,165,0.1)",
    },
}

navbar_box_style = {
    "position":        "sticky",
    "top":             "0",
    "z_index":         "100",
    "background":      "rgba(10,10,13,0.92)",
    "backdrop_filter": "blur(20px)",
    "border_bottom":   f"1px solid {C['border']}",
    "height":          "64px",
    "display":         "flex",
    "align_items":     "center",
    "width":           "100%",
}

# ============================================
# ÁTOMOS
# ============================================

def page_wrapper(*children, **props) -> rx.Component:
    return rx.box(*children, min_height="100vh", background=C["bg"], color=C["text"], **props)


def page_content(*children, max_w: str = S["page_max"], pad: str = "0 2em 5em", **props) -> rx.Component:
    return rx.box(*children, max_width=max_w, margin="0 auto", padding=pad, **props)


def accent_divider() -> rx.Component:
    return rx.box(height="1px", background=G["accent_h"], width="100%")


def category_tag(text) -> rx.Component:
    return rx.text(
        text,
        font_size="0.65em", color=C["accent"], font_weight="600",
        letter_spacing="0.15em", text_transform="uppercase",
    )


def author_avatar() -> rx.Component:
    return rx.box(
        width="24px", height="24px", border_radius="50%",
        background=C["surface"], border=f"1px solid {C['accent']}",
    )


def section_header(text: str) -> rx.Component:
    return rx.hstack(
        rx.box(width="3px", height="16px", background=C["accent"], border_radius="2px"),
        rx.text(text, font_size="0.7em", color=C["muted"], letter_spacing="0.15em", font_weight="600"),
        spacing="3", align="center",
    )


def page_section_title(label: str, title: str) -> rx.Component:
    return rx.hstack(
        rx.box(width="3px", height="20px", background=C["accent"], border_radius="2px"),
        rx.vstack(
            rx.text(label, font_size="0.7em", color=C["accent"], letter_spacing="0.15em", font_weight="600"),
            rx.heading(title, size="6", color=C["text"], font_family=fonts["serif"]),
            align_items="start", spacing="0",
        ),
        spacing="3", align="center",
    )


def back_link(text: str = "← Volver al blog", href: str = "/") -> rx.Component:
    return rx.link(
        text, href=href,
        color=C["accent"], font_size="0.8em", letter_spacing="0.05em",
        text_transform="uppercase", font_weight="500",
        _hover={"color": C["silver"]}, transition="color 0.2s",
    )


def panel(*children, **props) -> rx.Component:
    return rx.box(
        *children,
        background=C["surface"], border=f"1px solid {C['border']}",
        border_radius="6px", padding="2em", width="100%",
        **props,
    )


def form_field(label: str, component) -> rx.Component:
    return rx.vstack(
        rx.text(label, font_size="0.7em", color=C["accent"], font_weight="600",
                letter_spacing="0.1em", text_transform="uppercase"),
        component,
        align_items="start", width="100%", spacing="1",
    )


def feedback_message(message) -> rx.Component:
    return rx.cond(
        message != "",
        rx.box(
            rx.text(message, font_size="0.875em", color=C["accent"]),
            background=C["bg"], border=f"1px solid {C['accent']}",
            border_radius="4px", padding="0.75em 1.25em",
            width="100%", margin_bottom="1.5em",
        ),
    )


# ============================================
# BOTONES
# ============================================

def btn_primary(text: str, **props) -> rx.Component:
    return rx.button(
        text,
        background=C["accent"], color=C["text"],
        font_weight="600", font_size="0.875em", letter_spacing="0.05em",
        border_radius="4px", padding="0.65em 1.75em",
        cursor="pointer", border="none",
        _hover={"background": C["accent2"]},
        transition="background 0.2s",
        **props,
    )


def btn_outline(text: str, **props) -> rx.Component:
    # Cambiado a rx.button para accesibilidad y soporte correcto de on_click
    return rx.button(
        text,
        background="transparent",
        border=f"1px solid {C['accent']}",
        color=C["silver"],
        font_size="0.85em", font_weight="500", letter_spacing="0.05em",
        border_radius="4px", padding="0.6em 1.4em",
        cursor="pointer",
        _hover={"background": C["accent"], "color": C["text"]},
        transition="all 0.2s",
        **props,
    )


def btn_danger(text: str, **props) -> rx.Component:
    return rx.button(
        text,
        background="transparent",
        border=f"1px solid {C['danger_bg']}",
        color=C["danger_dim"],
        font_size="0.72em", letter_spacing="0.05em",
        border_radius="3px", padding="0.3em 0.75em",
        cursor="pointer",
        _hover={"background": C["danger_bg"], "color": C["danger"], "border_color": C["danger"]},
        transition="all 0.2s",
        **props,
    )


# ============================================
# NAVEGACIÓN
# ============================================

def logo() -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.box(
                rx.text("M", font_family=fonts["serif"], font_size="1.1em", font_weight="bold", color=C["silver"]),
                width="28px", height="28px", background=C["bg"],
                border=f"1px solid {C['accent']}", border_radius="5px",
                display="flex", align_items="center", justify_content="center",
            ),
            rx.text("El Club de los Marginalistas", font_size="0.9em", color=C["silver"],
                    font_weight="600", letter_spacing="0.02em", font_family=fonts["serif"]),
            spacing="2", align="center",
        ),
        href="/", text_decoration="none",
    )


def nav_link(text: str, href: str) -> rx.Component:
    return rx.link(
        text, href=href, color=C["muted"], font_size="0.8em",
        letter_spacing="0.05em", text_transform="uppercase",
        _hover={"color": C["silver"]}, transition="color 0.2s",
    )


def lang_toggle() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text("ES", font_size="0.75em", color=C["silver"], font_weight="600", letter_spacing="0.05em"),
            rx.box(width="1px", height="12px", background=C["accent"]),
            rx.text("EN", font_size="0.75em", color=C["muted"], font_weight="400", letter_spacing="0.05em"),
            spacing="2", align="center",
        ),
        border=f"1px solid {C['border']}", border_radius="4px",
        padding="0.3em 0.75em", cursor="pointer",
        _hover={"border_color": C["accent"]}, transition="border-color 0.2s",
    )


def _navbar_inner(right_content) -> rx.Component:
    """Base compartida entre navbar y admin_navbar."""
    return rx.hstack(
        logo(),
        right_content,
        justify="between", align="center",
        width="100%", max_width=S["page_max"],
        margin="0 auto", padding=f"0 {S['page_x']}",
    )


def navbar() -> rx.Component:
    return rx.box(
        _navbar_inner(
            rx.hstack(
                nav_link("Inicio", "/"),
                nav_link("Acerca", "/acerca"),
                nav_link("Colaboradores", "/colaboradores"),
                nav_link("Trading", "/trading"),
                lang_toggle(),
                spacing="6", align="center",
            )
        ),
        **navbar_box_style,
    )


def admin_navbar() -> rx.Component:
    return rx.box(
        _navbar_inner(
            rx.hstack(
                rx.text("PANEL ADMIN", font_size="0.75em", color=C["accent"], letter_spacing="0.15em", font_weight="600"),
                nav_link("← Ver blog", "/"),
                spacing="4", align="center",
            )
        ),
        **navbar_box_style,
    )


# ============================================
# CONTENIDO
# ============================================

def footer() -> rx.Component:
    nav_items = [("Inicio", "/"), ("Acerca", "/acerca"), ("Colaboradores", "/colaboradores"), ("Trading", "/trading")]
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("El Club de los Marginalistas", font_size="0.85em", color=C["silver"], font_weight="600", font_family=fonts["serif"]),
                rx.text("Pensamiento económico independiente.", font_size="0.75em", color=C["dim"]),
                rx.text("elclubdelosmarginalistas.com", font_size="0.75em", color=C["accent"]),
                align_items="start", spacing="1",
            ),
            rx.hstack(
                *[rx.link(t, href=h, font_size="0.75em", color=C["dim2"], _hover={"color": C["silver"]}) for t, h in nav_items],
                spacing="5",
            ),
            rx.text("© 2025 El Club de los Marginalistas", font_size="0.75em", color=C["dim"]),
            justify="between", align="center", width="100%",
            max_width=S["page_max"], margin="0 auto", padding=f"0 {S['page_x']}",
        ),
        border_top=f"1px solid {C['border']}", padding="2.5em 0", background=C["bg"],
    )


def newsletter() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                rx.vstack(
                    section_header("NEWSLETTER"),
                    rx.heading("Análisis directo a tu correo", size="5", color=C["text"], font_family=fonts["serif"]),
                    rx.text("Sin ruido. Solo economía.", color=C["dim2"], font_size="0.875em"),
                    align_items="start", spacing="2",
                ),
                rx.hstack(
                    rx.input(placeholder="tu@correo.com", **{**_input_base, "width": "260px"}),
                    btn_primary("Suscribirse"),
                    spacing="3",
                ),
                justify="between", align="center", width="100%",
            ),
            max_width=S["page_max"], margin="0 auto", padding="3em 2em",
        ),
        border_top=f"1px solid {C['border']}",
        border_bottom=f"1px solid {C['border']}",
        background=C["bg"],
    )


def hero() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(height="1px", background=G["center_h"], margin_bottom="3em"),
            rx.vstack(
                rx.hstack(
                    rx.box(width="2px", height="40px", background=C["accent"]),
                    rx.vstack(
                        rx.text("ANÁLISIS · TEORÍA · MERCADOS", font_size="0.7em", color=C["accent"], letter_spacing="0.2em", font_weight="500"),
                        rx.heading(
                            "El Club de los Marginalistas",
                            font_size="clamp(1.8rem, 4vw, 3rem)", font_weight="700",
                            color=C["text"], font_family=fonts["serif"],
                            letter_spacing="-0.02em", line_height="1.15",
                        ),
                        align_items="start", spacing="2",
                    ),
                    spacing="4", align="center",
                ),
                rx.text(
                    "Pensamiento económico riguroso. Análisis de mercados, teoría y política económica desde una perspectiva académica e independiente.",
                    color=C["muted"], font_size="1em", line_height="1.8", max_width="580px",
                ),
                btn_outline("Explorar entradas →"),
                align_items="start", spacing="5",
            ),
            rx.box(height="1px", background=G["border_h"], margin_top="3em"),
            max_width=S["page_max"], margin="0 auto", padding="4em 2em",
        ),
    )


def post_card(post) -> rx.Component:
    return rx.link(
        rx.box(
            rx.box(height="2px", background=G["accent_h"]),
            rx.box(
                rx.hstack(
                    category_tag(post.category),
                    rx.text(post.date, font_size="0.65em", color=C["accent"], opacity="0.7"),
                    justify="between", width="100%", margin_bottom="0.85em",
                ),
                rx.heading(post.title, size="4", margin_bottom="0.75em", line_height="1.3",
                           color=C["text"], font_weight="600", font_family=fonts["serif"]),
                rx.text(post.description, color=C["dim2"], font_size="0.85em", line_height="1.7", margin_bottom="1.5em"),
                rx.hstack(
                    rx.hstack(author_avatar(), rx.text(post.author, font_size="0.78em", font_weight="500", color=C["muted"]), spacing="2", align="center"),
                    rx.text("Leer →", font_size="0.78em", color=C["accent"], font_weight="500", letter_spacing="0.05em"),
                    justify="between", width="100%",
                ),
                padding="1.4em",
            ),
            **card_style,
        ),
        href=f"/blog/{post.slug}",
        text_decoration="none", _hover={"text_decoration": "none"},
    )


def post_meta_header(category, date, title, author) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            category_tag(category),
            rx.text("·", color=C["border"]),
            rx.text(date, font_size="0.7em", color=C["accent"], opacity="0.7"),
            spacing="2", align="center",
        ),
        rx.heading(
            title,
            font_size="clamp(1.6rem, 3.5vw, 2.5rem)", font_weight="700",
            line_height="1.2", color=C["text"], font_family=fonts["serif"],
            letter_spacing="-0.02em", margin_y="0.75em",
        ),
        rx.hstack(author_avatar(), rx.text(author, font_size="0.875em", font_weight="500", color=C["muted"]),
                  spacing="2", align="center", margin_bottom="2em"),
        rx.box(height="1px", background=C["border"], width="100%", margin_bottom="2.5em"),
        align_items="start", width="100%",
    )


def markdown_content(content) -> rx.Component:
    return rx.markdown(
        content, width="100%", color=C["muted"],
        component_map={
            "h1": lambda text: rx.heading(text, size="7", color=C["text"], font_family=fonts["serif"], margin_y="1em"),
            "h2": lambda text: rx.heading(text, size="6", color=C["text"], font_family=fonts["serif"], margin_y="0.85em"),
            "h3": lambda text: rx.heading(text, size="5", color=C["silver"], font_family=fonts["serif"], margin_y="0.75em"),
            "p":  lambda text: rx.text(text, color=C["muted"], line_height="1.85", margin_bottom="1.25em"),
        },
    )


def post_list_item(post, on_delete) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(post.title, font_weight="500", color=C["text"], font_size="0.9em", font_family=fonts["serif"]),
            rx.hstack(
                rx.text(post.slug, color=C["dim"], font_size="0.72em"),
                rx.text("·", color=C["border"]),
                rx.text(post.category, color=C["accent"], font_size="0.72em"),
                spacing="2",
            ),
            align_items="start", spacing="0",
        ),
        btn_danger("Eliminar", on_click=on_delete),
        justify="between", align="center", width="100%",
        padding="1em 0", border_bottom=f"1px solid {C['border']}",
    )


# ============================================
# WRAPPERS DE PÁGINA
# ============================================

def post_content_wrapper(*children) -> rx.Component:
    return rx.box(
        rx.vstack(*children, align_items="start", width="100%",
                  max_width=S["post_max"], margin="0 auto", padding="3em 2em 6em", spacing="4"),
    )


def admin_content_wrapper(*children) -> rx.Component:
    return rx.box(
        rx.vstack(*children, align_items="start", width="100%"),
        max_width=S["admin_max"], margin="0 auto", padding="3em 2em 6em",
    )


# ============================================
# COMPONENTES DE PÁGINAS ESPECÍFICAS
# ============================================

def info_card(label: str, description: str) -> rx.Component:
    return rx.box(
        rx.text(label, font_size="0.8em", color=C["accent"], font_weight="600",
                letter_spacing="0.1em", text_transform="uppercase", margin_bottom="0.5em"),
        rx.text(description, font_size="0.85em", color=C["muted"], line_height="1.6"),
        background=C["surface"], border=f"1px solid {C['border']}",
        border_radius="6px", padding="1.25em",
    )


def author_card(initials: str, name: str, role: str, bio: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(initials, font_size="1.2em", font_weight="700", color=C["accent"], font_family=fonts["serif"]),
            width="64px", height="64px", border_radius="50%",
            background=C["surface"], border=f"1px solid {C['accent']}",
            display="flex", align_items="center", justify_content="center", flex_shrink="0",
        ),
        rx.vstack(
            rx.text(name, font_size="1.1em", font_weight="600", color=C["text"], font_family=fonts["serif"]),
            rx.text(role, font_size="0.85em", color=C["accent"], letter_spacing="0.05em"),
            rx.text(bio, color=C["muted"], font_size="0.9em", line_height="1.7"),
            align_items="start", spacing="2",
        ),
        spacing="5", align="start", width="100%",
    )


def page_hero(eyebrow: str, title: str) -> rx.Component:
    return rx.box(
        rx.box(height="1px", background=G["center_h"], margin_bottom="3em"),
        rx.hstack(
            rx.box(width="2px", height="40px", background=C["accent"]),
            rx.vstack(
                rx.text(eyebrow, font_size="0.7em", color=C["accent"], letter_spacing="0.2em", font_weight="500"),
                rx.heading(title, font_size="clamp(1.8rem, 4vw, 2.8rem)", font_weight="700",
                           color=C["text"], font_family=fonts["serif"], letter_spacing="-0.02em", line_height="1.15"),
                align_items="start", spacing="2",
            ),
            spacing="4", align="center",
        ),
        max_width=S["page_max"], margin="0 auto", padding="4em 2em 2em",
    )


def filter_btn(active_filter, set_filter, cat: str) -> rx.Component:
    return rx.button(
        cat,
        on_click=lambda: set_filter(cat),
        background=rx.cond(active_filter == cat, C["accent"], "transparent"),
        color=rx.cond(active_filter == cat, C["text"], C["dim2"]),
        border=rx.cond(active_filter == cat, f"1px solid {C['accent']}", f"1px solid {C['border']}"),
        border_radius="3px", font_size="0.72em", letter_spacing="0.05em",
        padding="0.3em 0.85em", cursor="pointer",
        _hover={"border_color": C["accent"], "color": C["silver"]},
        transition="all 0.2s",
    )


def filters_bar(active_filter, set_filter) -> rx.Component:
    return rx.hstack(
        section_header("ENTRADAS RECIENTES"),
        rx.hstack(
            rx.foreach(CATEGORIES_FILTER, lambda cat: filter_btn(active_filter, set_filter, cat)),
            spacing="2",
        ),
        justify="between", align="center", width="100%",
        border_bottom=f"1px solid {C['border']}",
        padding_bottom="1.25em", margin_bottom="2em",
    )


def empty_state(message: str = "No hay entradas en esta categoría.") -> rx.Component:
    return rx.box(rx.text(message, color=C["accent"], font_size="0.9em"), padding="3em 0")


# ============================================
# NAVBARS PARA PORTALES (minimalistas)
# ============================================

def login_navbar() -> rx.Component:
    """Navbar minimalista para la página de login."""
    return rx.box(
        rx.hstack(
            logo(),
            justify="between", align="center",
            width="100%", max_width=S["page_max"],
            margin="0 auto", padding=f"0 {S['page_x']}",
        ),
        **navbar_box_style,
    )

def portal_navbar(label: str, on_logout) -> rx.Component:
    """Navbar minimalista para admin y portal colaborador."""
    return rx.box(
        rx.hstack(
            logo(),
            rx.hstack(
                rx.text(label, font_size="0.75em", color=C["accent"], letter_spacing="0.15em", font_weight="600"),
                rx.button(
                    "Cerrar sesión",
                    on_click=on_logout,
                    background="transparent",
                    border=f"1px solid {C['border']}",
                    color=C["muted"],
                    font_size="0.75em", letter_spacing="0.05em",
                    border_radius="4px", padding="0.3em 0.85em",
                    cursor="pointer",
                    _hover={"border_color": C["danger"], "color": C["danger"]},
                    transition="all 0.2s",
                ),
                spacing="4", align="center",
            ),
            justify="between", align="center",
            width="100%", max_width=S["page_max"],
            margin="0 auto", padding=f"0 {S['page_x']}",
        ),
        **navbar_box_style,
    )


def status_badge(status) -> rx.Component:
    """Badge de status para posts en el portal."""
    return rx.box(
        rx.text(status, font_size="0.65em", font_weight="600", letter_spacing="0.1em", text_transform="uppercase"),
        background=rx.cond(
            status == "published", "rgba(74,127,165,0.15)",
            rx.cond(status == "pending", "rgba(234,179,8,0.15)", "rgba(107,114,128,0.15)")
        ),
        color=rx.cond(
            status == "published", C["accent"],
            rx.cond(status == "pending", "#eab308", C["dim2"])
        ),
        border=rx.cond(
            status == "published", f"1px solid {C['accent']}",
            rx.cond(status == "pending", "1px solid #eab308", f"1px solid {C['dim']}")
        ),
        border_radius="3px", padding="0.2em 0.6em",
    )