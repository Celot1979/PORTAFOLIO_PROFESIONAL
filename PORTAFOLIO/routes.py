import reflex as rx
from .pages.subida_repositorios import subida_repositorios
from .pages.proyectos import proyectos

# Crear la aplicación
app = rx.App()

# Agregar las rutas
app.add_page(proyectos, route="/proyectos")
app.add_page(subida_repositorios, route="/admin/repositorios", protected=True) 