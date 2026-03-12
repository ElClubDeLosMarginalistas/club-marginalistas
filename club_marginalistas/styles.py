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

# ============================================
# COMPONENTES REUTILIZABLES
# ============================================

def page_wrapper(*children, **props) -> rx.Component:
    """Contenedor principal de cualquier página."""
    return rx.box(
        *children,
        min_height="100vh",
        background=colors["bg"],
        color=colors["text"],
        **props,
    )


def navbar(active: str = "") -> rx.Component:
    """Navbar global del sitio."""
    def nav_link(text: str, href: str) -> rx.Component:
        return rx.link(
            text,
            href=href,
            color=colors["muted"],
            font_size="0.8em",
            letter_spacing="0.05em",
            text_transform="uppercase",
            _hover={"color": colors["silver"]},
            transition="color 0.2s",
        )

    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
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
            ),
            # Links
            rx.hstack(
                nav_link("Inicio", "/"),
                nav_link("Acerca", "/acerca"),
                nav_link("Colaboradores", "/colaboradores"),
                nav_link("Trading", "/trading"),
                # Botón ES/EN
                rx.box(
                    rx.hstack(
                        rx.text("ES", font_size="0.75em", color=colors["silver"], font_weight="600", letter_spacing="0.05em"),
                        rx.box(width="1px", height="12px", background=colors["accent"]),
                        rx.text("EN", font_size="0.75em", color=colors["muted"], font_weight="400", letter_spacing="0.05em"),
                        spacing="2", align="center",
                    ),
                    border=f"1px solid {colors['border']}", border_radius="4px",
                    padding="0.3em 0.75em", cursor="pointer",
                    _hover={"border_color": colors["accent"]}, transition="border-color 0.2s",
                ),
                spacing="6", align="center",
            ),
            justify="between", align="center",
            width="100%", max_width="1200px", margin="0 auto", padding="0 2em",
        ),
        position="sticky", top="0", z_index="100",
        background="rgba(10,10,13,0.92)", backdrop_filter="blur(20px)",
        border_bottom=f"1px solid {colors['border']}",
        height="64px", display="flex", align_items="center", width="100%",
    )


def admin_navbar() -> rx.Component:
    """Navbar para el panel admin."""
    return rx.box(
        rx.hstack(
            rx.link(
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
            ),
            rx.hstack(
                rx.text("PANEL ADMIN", font_size="0.75em", color=colors["accent"], letter_spacing="0.15em", font_weight="600"),
                rx.link("← Ver blog", href="/", color=colors["muted"], font_size="0.8em", _hover={"color": colors["silver"]}),
                spacing="4", align="center",
            ),
            justify="between", align="center",
            width="100%", max_width="1200px", margin="0 auto", padding="0 2em",
        ),
        position="sticky", top="0", z_index="100",
        background="rgba(10,10,13,0.92)", backdrop_filter="blur(20px)",
        border_bottom=f"1px solid {colors['border']}",
        height="64px", display="flex", align_items="center", width="100%",
    )


def footer() -> rx.Component:
    """Footer global del sitio."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("El Club de los Marginalistas", font_size="0.85em", color=colors["silver"], font_weight="600", font_family=fonts["serif"]),
                rx.text("Pensamiento económico independiente.", font_size="0.75em", color=colors["dim"]),
                rx.text("elclubdelosmarginalistas.com", font_size="0.75em", color=colors["accent"]),
                align_items="start", spacing="1",
            ),
            rx.hstack(
                rx.link("Inicio", href="/", font_size="0.75em", color=colors["dim2"], _hover={"color": colors["silver"]}),
                rx.link("Acerca", href="/acerca", font_size="0.75em", color=colors["dim2"], _hover={"color": colors["silver"]}),
                rx.link("Colaboradores", href="/colaboradores", font_size="0.75em", color=colors["dim2"], _hover={"color": colors["silver"]}),
                rx.link("Trading", href="/trading", font_size="0.75em", color=colors["dim2"], _hover={"color": colors["silver"]}),
                spacing="5",
            ),
            rx.text("© 2025 El Club de los Marginalistas", font_size="0.75em", color=colors["dim"]),
            justify="between", align="center", width="100%",
            max_width="1200px", margin="0 auto", padding="0 2em",
        ),
        border_top=f"1px solid {colors['border']}",
        padding="2.5em 0",
        background=colors["bg"],
    )


def newsletter() -> rx.Component:
    """Sección de newsletter reutilizable."""
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
                    rx.input(placeholder="tu@correo.com", background=colors["bg"], border=f"1px solid {colors['border']}", color=colors["text"], border_radius="4px", _focus={"border_color": colors["accent"]}, _placeholder={"color": colors["dim"]}, width="260px"),
                    btn_primary("Suscribirse"),
                    spacing="3",
                ),
                justify="between", align="center", width="100%",
            ),
            max_width="1200px", margin="0 auto", padding="3em 2em",
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
    return rx.box(
        height="1px",
        background=f"linear-gradient(90deg, {colors['accent']}, transparent)",
        width="100%",
    )


def category_tag(text) -> rx.Component:
    """Etiqueta de categoría."""
    return rx.text(
        text,
        font_size="0.65em",
        color=colors["accent"],
        font_weight="600",
        letter_spacing="0.15em",
        text_transform="uppercase",
    )


def btn_primary(text: str, **props) -> rx.Component:
    """Botón primario azul."""
    return rx.button(
        text,
        background=colors["accent"],
        color=colors["text"],
        font_weight="600",
        font_size="0.875em",
        letter_spacing="0.05em",
        border_radius="4px",
        padding="0.65em 1.75em",
        cursor="pointer",
        border="none",
        _hover={"background": colors["accent2"]},
        transition="background 0.2s",
        **props,
    )


def btn_outline(text: str, **props) -> rx.Component:
    """Botón outline plateado."""
    return rx.box(
        rx.text(text, font_size="0.85em", color=colors["silver"], font_weight="500", letter_spacing="0.05em"),
        border=f"1px solid {colors['accent']}",
        border_radius="4px",
        padding="0.6em 1.4em",
        cursor="pointer",
        _hover={"background": colors["accent"]},
        transition="all 0.2s",
        **props,
    )


def btn_danger(text: str, **props) -> rx.Component:
    """Botón de eliminar."""
    return rx.button(
        text,
        background="transparent",
        border="1px solid #2a1a1a",
        color="#6b3a3a",
        font_size="0.72em",
        letter_spacing="0.05em",
        border_radius="3px",
        padding="0.3em 0.75em",
        cursor="pointer",
        _hover={"background": "#2a1a1a", "color": colors["danger"], "border_color": colors["danger"]},
        transition="all 0.2s",
        **props,
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
        align_items="start",
        width="100%",
        spacing="1",
    )


# --- ESTILOS DE DICCIONARIO (para componentes que los aceptan) ---
input_style = {
    "background":   colors["bg"],
    "border":       f"1px solid {colors['border']}",
    "color":        colors["text"],
    "border_radius": "4px",
    "width":        "100%",
    "_focus":       {"border_color": colors["accent"]},
    "_placeholder": {"color": colors["dim"]},
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