import reflex as rx

def blog():
    return rx.vstack(
        rx.heading("Blog", size="lg", margin_bottom="1em"),
        rx.text(
            "Bienvenido a mi blog. Aquí comparto mis pensamientos, experiencias "
            "y conocimientos sobre tecnología, desarrollo y más.",
            margin_bottom="2em",
        ),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 