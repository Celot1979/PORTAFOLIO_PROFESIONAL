import reflex as rx

def quien_soy():
    return rx.vstack(
        rx.heading("Quién Soy", size="lg", margin_bottom="1em"),
        rx.hstack(
            # Contenedor de la imagen
            rx.box(
                rx.image(
                    src="/mi_foto.jpg",  # Coloca tu imagen en la carpeta assets
                    width="300px",
                    height="300px",
                    object_fit="cover",
                    border_radius="10px",
                ),
                margin_right="2em",
            ),
            # Contenedor de la descripción
            rx.box(
                rx.text(
                    "Aquí puedes escribir tu descripción personal. Cuéntanos sobre ti, tus intereses, "
                    "tu experiencia y tus objetivos profesionales. Esta sección es una oportunidad "
                    "para que los visitantes conozcan más sobre quién eres y qué te apasiona hhhh.",
                    font_size="1.1em",
                    line_height="1.6",
                ),
                max_width="600px",
            ),
            align="center",
            padding="2em",
            background_color="#2d2d2d",
            border_radius="10px",
            margin="2em",
        ),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 