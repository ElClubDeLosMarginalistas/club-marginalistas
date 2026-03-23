import reflex as rx
from club_marginalistas.utils import auth_login, auth_logout, get_usuario_by_email
from club_marginalistas.styles import (
    page_wrapper, login_navbar,
    panel, form_field, btn_primary, feedback_message,
    input_style, page_hero,
)


class AuthState(rx.State):
    user_email: str = ""
    user_role:  str = ""
    user_name:  str = ""
    logged_in:  bool = False
    message:    str = ""
    email:      str = ""
    password:   str = ""

    def set_email(self, v):    self.email = v
    def set_password(self, v): self.password = v

    def handle_key_down(self, key: str):
        if key == "Enter":
            return self.login()

    def init_login(self):
        self.message  = ""
        self.email    = ""
        self.password = ""

    def login(self):
        if not self.email or not self.password:
            self.message = "❌ Ingresá email y contraseña."
            return
        result = auth_login(self.email, self.password)
        if not result["ok"]:
            self.message = "❌ Credenciales incorrectas."
            return
        usuario = get_usuario_by_email(self.email)
        if not usuario:
            self.message = "❌ Tu cuenta no tiene acceso asignado. Contactá al admin."
            return
        self.user_email = usuario.email
        self.user_role  = usuario.role
        self.user_name  = usuario.name
        self.logged_in  = True
        self.message    = ""
        if usuario.role == "admin":
            return rx.redirect("/admin")
        return rx.redirect("/portal")

    def logout(self):
        auth_logout()
        self.user_email = ""
        self.user_role  = ""
        self.user_name  = ""
        self.logged_in  = False
        self.message    = ""
        self.email      = ""
        self.password   = ""
        return rx.redirect("/login")


def login_page() -> rx.Component:
    return page_wrapper(
        login_navbar(),
        page_hero("ACCESO", "Iniciar sesión"),
        rx.box(
            panel(
                rx.vstack(
                    feedback_message(AuthState.message),
                    form_field("Email", rx.input(
                        value=AuthState.email, on_change=AuthState.set_email,
                        on_key_down=AuthState.handle_key_down,
                        placeholder="tu@correo.com", type="email", **input_style,
                    )),
                    form_field("Contraseña", rx.input(
                        value=AuthState.password, on_change=AuthState.set_password,
                        on_key_down=AuthState.handle_key_down,
                        placeholder="••••••••", type="password", **input_style,
                    )),
                    btn_primary("Ingresar", on_click=AuthState.login, width="100%"),
                    align_items="start", width="100%", spacing="4",
                ),
            ),
            max_width="420px", margin="0 auto", padding="3em 2em 6em",
        ),
        on_mount=AuthState.init_login,
    )