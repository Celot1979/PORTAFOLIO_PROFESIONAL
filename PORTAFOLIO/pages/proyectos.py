import reflex as rx

def proyectos():
    return rx.vstack(
        rx.heading("Mis Proyectos", size="lg", margin_bottom="1em"),
        rx.text(
            "Aquí encontrarás una colección de mis proyectos más destacados. "
            "Cada proyecto representa un desafío único y una oportunidad de aprendizaje.",
            margin_bottom="2em",
        ),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 