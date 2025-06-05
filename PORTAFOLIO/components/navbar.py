import reflex as rx

def navbar():
    return rx.hstack(
        rx.hstack(
            rx.link("Inicio", href="/", color="white", _hover={"color": "#4CAF50"}),
            rx.link("Quién Soy", href="/quien-soy", color="white", _hover={"color": "#4CAF50"}),
            rx.link("Proyectos", href="/proyectos", color="white", _hover={"color": "#4CAF50"}),
            rx.link("Blog", href="/blog", color="white", _hover={"color": "#4CAF50"}),
            rx.link("Contacto", href="/contacto", color="white", _hover={"color": "#4CAF50"}),
            spacing="2",
        ),
        padding="1em",
        background_color="#2d2d2d",
        width="100%",
        position="sticky",
        top="0",
        z_index="1000",
    ) 