import reflex as rx
from ..state import GlobalState

def login():
    return rx.vstack(
        rx.heading("Iniciar Sesión", size="2"),
        rx.vstack(
            rx.input(
                placeholder="Usuario",
                value=GlobalState.username,
                on_change=GlobalState.set_username,
                required=True,
            ),
            rx.input(
                placeholder="Contraseña",
                type="password",
                value=GlobalState.password,
                on_change=GlobalState.set_password,
                required=True,
            ),
            rx.button(
                "Iniciar Sesión",
                on_click=GlobalState.login,
                width="100%",
            ),
            rx.link(
                rx.button(
                    "Volver a Inicio",
                    color_scheme="green",
                    _hover={"background_color": "#45a049"},
                    width="100%",
                ),
                href="/",
            ),
            rx.cond(
                GlobalState.error,
                rx.text(GlobalState.error, color="red"),
            ),
            rx.divider(margin_y="1em"),
            rx.text("¿Necesitas ayuda? Contáctame:", color="gray"),
            rx.hstack(
                rx.link(
                    "Telegram: @Celot1979",
                    href="https://t.me/Celot1979",
                    color="white",
                    _hover={"color": "#4CAF50"},
                ),
                rx.text("|", color="gray"),
                rx.link(
                    "Email: dgarciamartinez53@gmail.com",
                    href="mailto:dgarciamartinez53@gmail.com",
                    color="white",
                    _hover={"color": "#4CAF50"},
                ),
                spacing="1",
            ),
            spacing="1",
            width="100%",
            max_width="400px",
        ),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
        align_items="center",
        justify="center",
    )