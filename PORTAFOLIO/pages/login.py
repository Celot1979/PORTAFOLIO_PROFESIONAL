import reflex as rx
from ..state import GlobalState

def login():
    return rx.vstack(
        rx.heading("Iniciar Sesión", size="lg"),
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
            rx.cond(
                GlobalState.error,
                rx.text(GlobalState.error, color="red"),
            ),
            spacing="1em",
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