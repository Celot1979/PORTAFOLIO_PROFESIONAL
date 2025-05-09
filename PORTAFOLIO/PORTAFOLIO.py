import reflex as rx
from rxconfig import config

# Importar las páginas
from .pages.quien_soy import quien_soy
from .pages.proyectos import proyectos
from .pages.blog import blog
from .pages.contacto import contacto

# Estilo común para el tema oscuro
style = {
    "background_color": "#1a1a1a",
    "color": "#ffffff",
    "min_height": "100vh",
}

def navbar():
    return rx.hstack(
        rx.link("Quién Soy", href="/quien-soy", color="white", _hover={"color": "#4CAF50"}),
        rx.link("Proyectos", href="/proyectos", color="white", _hover={"color": "#4CAF50"}),
        rx.link("Blog", href="/blog", color="white", _hover={"color": "#4CAF50"}),
        rx.link("Contacto", href="/contacto", color="white", _hover={"color": "#4CAF50"}),
        justify="center",
        padding="1em",
        background_color="#2d2d2d",
        width="100%",
        position="sticky",
        top="0",
        z_index="1000",
    )

def index():
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading("Mi Portafolio", size="lg", margin_bottom="1em"),
            rx.text("Bienvenido a mi portafolio personal", margin_bottom="2em"),
            width="100%",
            align="center",
            padding="2em",
        ),
        style=style,
    )

# Configuración de la aplicación
app = rx.App()
app.add_page(index)
app.add_page(quien_soy, route="/quien-soy")
app.add_page(proyectos, route="/proyectos")
app.add_page(blog, route="/blog")
app.add_page(contacto, route="/contacto")
