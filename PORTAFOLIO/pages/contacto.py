import reflex as rx
from ..components.navbar import navbar

def contacto():
    return rx.vstack(
        navbar(),
        rx.heading("Contacto", size="lg", margin_bottom="1em"),
        rx.text(
            "¿Quieres ponerte en contacto conmigo? Estoy disponible para "
            "colaboraciones, consultas o simplemente para charlar sobre tecnología.",
            margin_bottom="2em",
        ),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 