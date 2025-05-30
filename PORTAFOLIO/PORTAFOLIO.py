import reflex as rx
from rxconfig import config
from .models.blog import BlogPost
from .database import init_db

# Importar las páginas
from .pages.quien_soy import quien_soy
from .pages.proyectos import proyectos
from .pages.blog import blog, blog_post
from .pages.contacto import contacto
from .pages.subida_repositorios import subida_repositorios
from .pages.subida_blog import subida_blog
from .pages.admin import admin
from .pages.login import login
from .pages.sitemap import sitemap
from .pages.robots import robots

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
            rx.link(
                rx.button(
                    "Ver Proyectos",
                    color_scheme="green",
                    _hover={"background_color": "#45a049"},
                    margin_top="2em",
                    size="lg",
                ),
                href="/proyectos",
            ),
            spacing="2em",
            width="100%",
            max_width="1200px",
            padding="2em",
        ),
        style=style,
        align_items="center",
        justify="center",
    )

# Crear la aplicación
app = rx.App()

# Inicializar la base de datos
init_db()

# Agregar las rutas
app.add_page(index)
app.add_page(quien_soy, route="/quien-soy")
app.add_page(proyectos, route="/proyectos")
app.add_page(blog, route="/blog")
app.add_page(blog_post, route="/blog/[slug]")
app.add_page(contacto, route="/contacto")
app.add_page(admin, route="/admin")
app.add_page(subida_repositorios, route="/admin/repositorios")
app.add_page(subida_blog, route="/admin/blog")
app.add_page(login, route="/login")
app.add_page(sitemap, route="/sitemap.xml")
app.add_page(robots, route="/robots.txt")
