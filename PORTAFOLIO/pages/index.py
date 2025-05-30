import reflex as rx
from ..components.navbar import navbar
# Está página es para darle una presentación más atractiva a la página principal
def index():
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading("Bienvenido a mi portafolio personal", size="lg"),
            rx.text(
                "Desarrollador Full Stack & Entusiasta de la Tecnología",
                font_size="1.2em",
                color="gray",
                margin_bottom="2em",
            ),
            rx.hstack(
                rx.vstack(
                    rx.icon("code", size=32, color="#4CAF50"),
                    rx.heading("Desarrollo", size="md"),
                    rx.text("Creando soluciones digitales innovadoras", color="gray"),
                    padding="2em",
                    background_color="#2d2d2d",
                    border_radius="lg",
                    width="250px",
                    align_items="center",
                    _hover={"transform": "translateY(-5px)", "transition": "all 0.3s ease"},
                ),
                rx.vstack(
                    rx.icon("database", size=32, color="#4CAF50"),
                    rx.heading("Backend", size="md"),
                    rx.text("Arquitectura robusta y escalable", color="gray"),
                    padding="2em",
                    background_color="#2d2d2d",
                    border_radius="lg",
                    width="250px",
                    align_items="center",
                    _hover={"transform": "translateY(-5px)", "transition": "all 0.3s ease"},
                ),
                rx.vstack(
                    rx.icon("palette", size=32, color="#4CAF50"),
                    rx.heading("Diseño", size="md"),
                    rx.text("Interfaces intuitivas y atractivas", color="gray"),
                    padding="2em",
                    background_color="#2d2d2d",
                    border_radius="lg",
                    width="250px",
                    align_items="center",
                    _hover={"transform": "translateY(-5px)", "transition": "all 0.3s ease"},
                ),
                spacing="2em",
                margin_bottom="3em",
            ),
            rx.text(
                "Explora mis proyectos y descubre cómo puedo ayudarte a materializar tus ideas",
                color="gray",
                text_align="center",
                max_width="600px",
            ),
            rx.button(
                "Ver Proyectos",
                color_scheme="green",
                _hover={"background_color": "#45a049"},
                margin_top="2em",
                size="lg",
            ),
            spacing="2em",
            width="100%",
            max_width="1200px",
            padding="2em",
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