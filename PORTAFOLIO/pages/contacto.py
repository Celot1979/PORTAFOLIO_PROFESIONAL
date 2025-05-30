import reflex as rx

def contacto():
    return rx.vstack(
        rx.heading("Contacto", size="lg"),
        rx.vstack(
            rx.text("¿Quieres contactar conmigo? Aquí tienes mis datos:", color="gray"),
            rx.hstack(
                rx.link(
                    "Telegram: @Celot1979",
                    href="https://t.me/Celot1979",
                    color="white",
                    _hover={"color": "#4CAF50"},
                    font_size="1.2em",
                ),
                rx.text("|", color="gray"),
                rx.link(
                    "Email: dgarciamartinez53@gmail.com",
                    href="mailto:dgarciamartinez53@gmail.com",
                    color="white",
                    _hover={"color": "#4CAF50"},
                    font_size="1.2em",
                ),
                spacing="1em",
            ),
            rx.link(
                rx.button(
                    "Página Principal",
                    color_scheme="green",
                    _hover={"background_color": "#45a049"},
                    width="100%",
                    margin_top="2em",
                ),
                href="/",
            ),
            spacing="2em",
            width="100%",
            max_width="800px",
            padding="2em",
            background_color="#2d2d2d",
            border_radius="lg",
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