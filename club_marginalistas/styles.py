import reflex as rx

# ============================================
# ESTILOS GLOBALES — El Club de los Marginalistas
# ============================================

# --- PALETA DE COLORES ---
colors = {
    "bg":       "#0a0a0d",
    "surface":  "#0f1219",
    "surface2": "#111827",
    "border":   "#1e2030",
    "accent":   "#4a7fa5",
    "accent2":  "#5a8fb5",
    "text":     "#e8eaf0",
    "muted":    "#8896aa",
    "silver":   "#c0c8d8",
    "dim":      "#4a5568",
    "dim2":     "#6b7a8d",
    "danger":   "#ef4444",
}

# --- TIPOGRAFÍA ---
fonts = {
    "serif": "Georgia, serif",
    "sans":  "system-ui, sans-serif",
}

# --- GRADIENTES ---
gradients = {
    "accent_h":  f"linear-gradient(90deg, {colors['accent']}, transparent)",
    "center_h":  f"linear-gradient(90deg, transparent, {colors['accent']}, transparent)",
    "border_h":  f"linear-gradient(90deg, transparent, {colors['border']}, transparent)",
    "card_top":  f"linear-gradient(90deg, {colors['accent']}, transparent)",
}

# --- ESPACIADO ---
spacing = {
    "page_x":   "2em",
    "page_max":  "1200px",
    "post_max":  "740px",
    "admin_max": "960px",
}

# ============================================
# ESTILOS DICCIONARIO
# ============================================

input_style = {
    "background":    colors["bg"],
    "border":        f"1px solid {colors['border']}",
    "color":         colors["text"],
    "border_radius": "4px",
    "width":         "100%",
    "_focus":        {"border_color": colors["accent"]},
    "_placeholder":  {"color": colors["dim"]},
}

textarea_style = {
    **input_style,
    "min_height":    "280px",
    "_placeholder":  {"color": colors["dim"]},
}

card_style = {
    "border":        f"1px solid {colors['border']}",
    "border_radius": "6px",
    "background":    colors["surface"],
    "height":        "100%",
    "overflow":      "hidden",
    "transition":    "all 0.25s ease",
    "_hover": {
        "border_color": colors["accent"],
        "background":   colors["surface2"],
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
    "border_bottom":   f"1px solid {colors['border']}",
    "height":          "64px",
    "display":         "flex",
    "align_items":     "center",
    "width":           "100%",
}

# ============================================
# COMPONENTES REUTILIZABLES
# ============================================

def page_wrapper(*children, **props) -> rx.Component:
    return rx.box(
        *children,
        min_height="100vh",
        background=colors["bg"],
        color=colors["text"],
        **props,
    )


def page_content(*children, max_w: str = spacing["page_max"], pad: str = "0 2em 5em", **props) -> rx.Component:
    """Contenedor de contenido centrado."""
    return rx.box(
        *children,
        max_width=max_w,
        margin="0 auto",
        padding=pad,
        **props,
    )


def logo() -> rx.Component:
    """Logo M + nombre del blog."""
    return rx.link(
        rx.hstack(
            rx.box(
                rx.text("M", font_family=fonts["serif"], font_size="1.1em", font_weight="bold", color=colors["silver"]),
                width="28px", height="28px", background=colors["bg"],
                border=f"1px solid {colors['accent']}", border_radius="5px",
                display="flex", align_items="center", justify_content="center",
            ),
            rx.text("El Club de los Marginalistas", font_size="0.9em", color=colors["silver"], font_weight="600", letter_spacing="0.02em", font_family=fonts["serif"]),
            spacing="2", align="center",
        ),
        href="/", text_decoration="none",
    )


def nav_link(text: str, href: str) -> rx.Component:
    """Link de navegación."""
    return rx.link(
        text, href=href,
        color=colors["muted"], font_size="0.8em",
        letter_spacing="0.05em", text_transform="uppercase",
        _hover={"color": colors["silver"]}, transition="color 0.2s",
    )


def lang_toggle() -> rx.Component:
    """Botón ES/EN."""
    return rx.box(
        rx.hstack(
            rx.text("ES", font_size="0.75em", color=colors["silver"], font_weight="600", letter_spacing="0.05em"),
            rx.box(width="1px", height="12px", background=colors["accent"]),
            rx.text("EN", font_size="0.75em", color=colors["muted"], font_weight="400", letter_spacing="0.05em"),
            spacing="2", align="center",
        ),
        border=f"1px solid {colors['border']}", border_radius="4px",
        padding="0.3em 0.75em", cursor="pointer",
        _hover={"border_color": colors["accent"]}, transition="border-color 0.2s",
    )


def navbar_inner(*right_items) -> rx.Component:
    """Interior del navbar reutilizable."""
    return rx.hstack(
        logo(),
        rx.hstack(*right_items, spacing="6", align="center"),
        justify="between", align="center",
        width="100%", max_width=spacing["page_max"],
        margin="0 auto", padding=f"0 {spacing['page_x']}",
    )


def navbar() -> rx.Component:
    """Navbar principal."""
    return rx.box(
        navbar_inner(
            nav_link("Inicio", "/"),
            nav_link("Acerca", "/acerca"),
            nav_link("Colaboradores", "/colaboradores"),
            nav_link("Trading", "/trading"),
            lang_toggle(),
        ),
        **navbar_box_style,
    )


def admin_navbar() -> rx.Component:
    """Navbar del panel admin."""
    return rx.box(
        rx.hstack(
            logo(),
            rx.hstack(
                rx.text("PANEL ADMIN", font_size="0.75em", color=colors["accent"], letter_spacing="0.15em", font_weight="600"),
                nav_link("← Ver blog", "/"),
                spacing="4", align="center",
            ),
            justify="between", align="center",
            width="100%", max_width=spacing["page_max"],
            margin="0 auto", padding=f"0 {spacing['page_x']}",
        ),
        **navbar_box_style,
    )


def footer() -> rx.Component:
    """Footer global."""
    links = ["Inicio", "Acerca", "Colaboradores", "Trading"]
    hrefs = ["/", "/acerca", "/colaboradores", "/trading"]
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("El Club de los Marginalistas", font_size="0.85em", color=colors["silver"], font_weight="600", font_family=fonts["serif"]),
                rx.text("Pensamiento económico independiente.", font_size="0.75em", color=colors["dim"]),
                rx.text("elclubdelosmarginalistas.com", font_size="0.75em", color=colors["accent"]),
                align_items="start", spacing="1",
            ),
            rx.hstack(
                *[rx.link(t, href=h, font_size="0.75em", color=colors["dim2"], _hover={"color": colors["silver"]}) for t, h in zip(links, hrefs)],
                spacing="5",
            ),
            rx.text("© 2025 El Club de los Marginalistas", font_size="0.75em", color=colors["dim"]),
            justify="between", align="center", width="100%",
            max_width=spacing["page_max"], margin="0 auto", padding=f"0 {spacing['page_x']}",
        ),
        border_top=f"1px solid {colors['border']}",
        padding="2.5em 0",
        background=colors["bg"],
    )


def newsletter() -> rx.Component:
    """Sección newsletter."""
    return rx.box(
        rx.box(
            rx.hstack(
                rx.vstack(
                    section_header("NEWSLETTER"),
                    rx.heading("Análisis directo a tu correo", size="5", color=colors["text"], font_family=fonts["serif"]),
                    rx.text("Sin ruido. Solo economía.", color=colors["dim2"], font_size="0.875em"),
                    align_items="start", spacing="2",
                ),
                rx.hstack(
                    rx.input(placeholder="tu@correo.com", **{**input_style, "width": "260px"}),
                    btn_primary("Suscribirse"),
                    spacing="3",
                ),
                justify="between", align="center", width="100%",
            ),
            max_width=spacing["page_max"], margin="0 auto", padding="3em 2em",
        ),
        border_top=f"1px solid {colors['border']}",
        border_bottom=f"1px solid {colors['border']}",
        background=colors["bg"],
    )


def section_header(text: str) -> rx.Component:
    """Encabezado de sección con barra azul."""
    return rx.hstack(
        rx.box(width="3px", height="16px", background=colors["accent"], border_radius="2px"),
        rx.text(text, font_size="0.7em", color=colors["muted"], letter_spacing="0.15em", font_weight="600"),
        spacing="3", align="center",
    )


def accent_divider() -> rx.Component:
    """Línea decorativa con gradiente."""
    return rx.box(height="1px", background=gradients["accent_h"], width="100%")


def category_tag(text) -> rx.Component:
    """Etiqueta de categoría."""
    return rx.text(
        text,
        font_size="0.65em", color=colors["accent"],
        font_weight="600", letter_spacing="0.15em", text_transform="uppercase",
    )


def author_avatar() -> rx.Component:
    """Avatar circular del autor."""
    return rx.box(
        width="24px", height="24px", border_radius="50%",
        background=colors["surface"], border=f"1px solid {colors['accent']}",
    )


def back_link(text: str = "← Volver al blog", href: str = "/") -> rx.Component:
    """Link para volver."""
    return rx.link(
        text, href=href,
        color=colors["accent"], font_size="0.8em",
        letter_spacing="0.05em", text_transform="uppercase",
        font_weight="500", _hover={"color": colors["silver"]},
        transition="color 0.2s",
    )


def post_card(post) -> rx.Component:
    """Tarjeta de post para el grid."""
    return rx.link(
        rx.box(
            rx.box(height="2px", background=gradients["card_top"]),
            rx.box(
                rx.hstack(
                    category_tag(post.category),
                    rx.text(post.date, font_size="0.65em", color=colors["accent"], opacity="0.7"),
                    justify="between", width="100%", margin_bottom="0.85em",
                ),
                rx.heading(post.title, size="4", margin_bottom="0.75em", line_height="1.3", color=colors["text"], font_weight="600", font_family=fonts["serif"]),
                rx.text(post.description, color=colors["dim2"], font_size="0.85em", line_height="1.7", margin_bottom="1.5em"),
                rx.hstack(
                    rx.hstack(author_avatar(), rx.text(post.author, font_size="0.78em", font_weight="500", color=colors["muted"]), spacing="2", align="center"),
                    rx.text("Leer →", font_size="0.78em", color=colors["accent"], font_weight="500", letter_spacing="0.05em"),
                    justify="between", width="100%",
                ),
                padding="1.4em",
            ),
            **card_style,
        ),
        href=f"/blog/{post.slug}",
        text_decoration="none", _hover={"text_decoration": "none"},
    )


def hero() -> rx.Component:
    """Hero de la página principal."""
    return rx.box(
        rx.box(
            rx.box(height="1px", background=gradients["center_h"], margin_bottom="3em"),
            rx.vstack(
                rx.hstack(
                    rx.box(width="2px", height="40px", background=colors["accent"]),
                    rx.vstack(
                        rx.text("ANÁLISIS · TEORÍA · MERCADOS", font_size="0.7em", color=colors["accent"], letter_spacing="0.2em", font_weight="500"),
                        rx.heading("El Club de los Marginalistas", font_size="clamp(1.8rem, 4vw, 3rem)", font_weight="700", color=colors["text"], font_family=fonts["serif"], letter_spacing="-0.02em", line_height="1.15"),
                        align_items="start", spacing="2",
                    ),
                    spacing="4", align="center",
                ),
                rx.text("Pensamiento económico riguroso. Análisis de mercados, teoría y política económica desde una perspectiva académica e independiente.", color=colors["muted"], font_size="1em", line_height="1.8", max_width="580px"),
                btn_outline("Explorar entradas →"),
                align_items="start", spacing="5",
            ),
            rx.box(height="1px", background=gradients["border_h"], margin_top="3em"),
            max_width=spacing["page_max"], margin="0 auto", padding="4em 2em",
        ),
    )


def feedback_message(message) -> rx.Component:
    """Mensaje de feedback en formularios."""
    return rx.cond(
        message != "",
        rx.box(
            rx.text(message, font_size="0.875em", color=colors["accent"]),
            background=colors["bg"],
            border=f"1px solid {colors['accent']}",
            border_radius="4px",
            padding="0.75em 1.25em",
            width="100%",
            margin_bottom="1.5em",
        ),
    )


def panel(*children, **props) -> rx.Component:
    """Panel/caja de contenido."""
    return rx.box(
        *children,
        background=colors["surface"],
        border=f"1px solid {colors['border']}",
        border_radius="6px",
        padding="2em",
        width="100%",
        **props,
    )


def form_field(label: str, component) -> rx.Component:
    """Campo de formulario con etiqueta."""
    return rx.vstack(
        rx.text(label, font_size="0.7em", color=colors["accent"], font_weight="600", letter_spacing="0.1em", text_transform="uppercase"),
        component,
        align_items="start", width="100%", spacing="1",
    )


def btn_primary(text: str, **props) -> rx.Component:
    """Botón primario azul."""
    return rx.button(
        text,
        background=colors["accent"], color=colors["text"],
        font_weight="600", font_size="0.875em", letter_spacing="0.05em",
        border_radius="4px", padding="0.65em 1.75em",
        cursor="pointer", border="none",
        _hover={"background": colors["accent2"]}, transition="background 0.2s",
        **props,
    )


def btn_outline(text: str, **props) -> rx.Component:
    """Botón outline plateado."""
    return rx.box(
        rx.text(text, font_size="0.85em", color=colors["silver"], font_weight="500", letter_spacing="0.05em"),
        border=f"1px solid {colors['accent']}", border_radius="4px",
        padding="0.6em 1.4em", cursor="pointer",
        _hover={"background": colors["accent"]}, transition="all 0.2s",
        **props,
    )


def btn_danger(text: str, **props) -> rx.Component:
    """Botón de eliminar."""
    return rx.button(
        text,
        background="transparent", border="1px solid #2a1a1a",
        color="#6b3a3a", font_size="0.72em", letter_spacing="0.05em",
        border_radius="3px", padding="0.3em 0.75em", cursor="pointer",
        _hover={"background": "#2a1a1a", "color": colors["danger"], "border_color": colors["danger"]},
        transition="all 0.2s",
        **props,
    )


def post_meta_header(category, date, title, author) -> rx.Component:
    """Encabezado completo de un post individual."""
    return rx.vstack(
        rx.hstack(
            category_tag(category),
            rx.text("·", color=colors["border"]),
            rx.text(date, font_size="0.7em", color=colors["accent"], opacity="0.7"),
            spacing="2", align="center",
        ),
        rx.heading(
            title,
            font_size="clamp(1.6rem, 3.5vw, 2.5rem)",
            font_weight="700", line_height="1.2",
            color=colors["text"], font_family=fonts["serif"],
            letter_spacing="-0.02em", margin_y="0.75em",
        ),
        rx.hstack(
            author_avatar(),
            rx.text(author, font_size="0.875em", font_weight="500", color=colors["muted"]),
            spacing="2", align="center", margin_bottom="2em",
        ),
        rx.box(height="1px", background=colors["border"], width="100%", margin_bottom="2.5em"),
        align_items="start", width="100%",
    )


def markdown_content(content) -> rx.Component:
    """Contenido markdown estilizado."""
    return rx.markdown(
        content,
        width="100%",
        color=colors["muted"],
        component_map={
            "h1": lambda text: rx.heading(text, size="7", color=colors["text"], font_family=fonts["serif"], margin_y="1em"),
            "h2": lambda text: rx.heading(text, size="6", color=colors["text"], font_family=fonts["serif"], margin_y="0.85em"),
            "h3": lambda text: rx.heading(text, size="5", color=colors["silver"], font_family=fonts["serif"], margin_y="0.75em"),
            "p": lambda text: rx.text(text, color=colors["muted"], line_height="1.85", margin_bottom="1.25em"),
        },
    )


def post_list_item(post, on_delete) -> rx.Component:
    """Fila de post en el panel admin."""
    return rx.hstack(
        rx.vstack(
            rx.text(post.title, font_weight="500", color=colors["text"], font_size="0.9em", font_family=fonts["serif"]),
            rx.hstack(
                rx.text(post.slug, color=colors["dim"], font_size="0.72em"),
                rx.text("·", color=colors["border"]),
                rx.text(post.category, color=colors["accent"], font_size="0.72em"),
                spacing="2",
            ),
            align_items="start", spacing="0",
        ),
        btn_danger("Eliminar", on_click=on_delete),
        justify="between", align="center", width="100%",
        padding="1em 0", border_bottom=f"1px solid {colors['border']}",
    )


def section_title(label: str, title: str) -> rx.Component:
    """Título de sección con etiqueta superior."""
    return rx.hstack(
        rx.box(width="3px", height="20px", background=colors["accent"], border_radius="2px"),
        rx.vstack(
            rx.text(label, font_size="0.7em", color=colors["accent"], letter_spacing="0.15em", font_weight="600"),
            rx.heading(title, size="6", color=colors["text"], font_family=fonts["serif"]),
            align_items="start", spacing="0",
        ),
        spacing="3", align="center",
    )