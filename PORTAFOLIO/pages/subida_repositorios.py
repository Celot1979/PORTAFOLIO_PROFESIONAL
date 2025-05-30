import reflex as rx
from typing import List, Dict, Any
from typing_extensions import TypedDict
from ..models.repositorio import Repositorio
from ..state import GlobalState
from urllib.parse import urlparse

class RepositorioDict(TypedDict):
    id: int
    titulo: str
    enlace: str
    imagen: str

class SubidaRepositoriosState(rx.State):
    titulo: str = ""
    enlace: str = ""
    imagen_url: str = ""
    error_message: str = ""
    repositorios: List[RepositorioDict] = []

    def handle_image_url(self, url: str):
        """Maneja la URL de la imagen."""
        if url:
            try:
                # Validar que sea una URL válida
                parsed_url = urlparse(url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    raise ValueError("URL inválida")
                
                self.imagen_url = url
                self.error_message = ""
                
            except Exception as e:
                print(f"Error al validar la URL: {str(e)}")
                self.error_message = f"Error al validar la URL: {str(e)}"

    def handle_submit(self):
        """Maneja el envío del formulario."""
        if self.titulo and self.enlace and self.imagen_url:
            try:
                # Crear el repositorio
                Repositorio.create(
                    titulo=self.titulo,
                    enlace=self.enlace,
                    imagen=self.imagen_url
                )
                
                # Limpiar el formulario
                self.titulo = ""
                self.enlace = ""
                self.imagen_url = ""
                self.error_message = ""
                
                # Recargar la lista de repositorios
                self.load_repositorios()
            except Exception as e:
                self.error_message = f"Error al crear el repositorio: {str(e)}"

    def load_repositorios(self):
        """Carga la lista de repositorios desde la base de datos."""
        db_repos = Repositorio.select().order_by(Repositorio.id.desc())
        self.repositorios = [
            {
                "id": int(repo.id),
                "titulo": str(repo.titulo),
                "enlace": str(repo.enlace),
                "imagen": str(repo.imagen)
            }
            for repo in db_repos
        ]

    def delete_repo(self, repo_id: int):
        """Elimina un repositorio."""
        Repositorio.delete_by_id(repo_id)
        self.load_repositorios()

def subida_repositorios():
    return rx.cond(
        GlobalState.is_authenticated,
        rx.vstack(
            rx.hstack(
                rx.heading("Gestión de Repositorios", size="lg"),
                rx.spacer(),
                rx.button("Cerrar Sesión", on_click=GlobalState.logout, color_scheme="red"),
                width="100%",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.input(
                    placeholder="Título del Repositorio",
                    value=SubidaRepositoriosState.titulo,
                    on_change=SubidaRepositoriosState.set_titulo,
                    required=True,
                ),
                rx.input(
                    placeholder="Enlace al Repositorio",
                    value=SubidaRepositoriosState.enlace,
                    on_change=SubidaRepositoriosState.set_enlace,
                    required=True,
                ),
                rx.input(
                    placeholder="URL de la imagen (ej: https://ejemplo.com/imagen.jpg)",
                    value=SubidaRepositoriosState.imagen_url,
                    on_change=SubidaRepositoriosState.handle_image_url,
                    required=True,
                ),
                rx.cond(
                    SubidaRepositoriosState.imagen_url,
                    rx.image(src=SubidaRepositoriosState.imagen_url, width="200px", height="200px"),
                ),
                rx.cond(
                    SubidaRepositoriosState.error_message,
                    rx.text(SubidaRepositoriosState.error_message, color="red"),
                ),
                rx.button(
                    "Subir Repositorio",
                    on_click=SubidaRepositoriosState.handle_submit,
                ),
                spacing="1em",
            ),
            rx.divider(),
            rx.heading("Repositorios Existentes", size="md", margin_top="2em"),
            rx.vstack(
                rx.foreach(
                    SubidaRepositoriosState.repositorios,
                    lambda repo: rx.hstack(
                        rx.image(src=repo["imagen"], width="100px", height="100px"),
                        rx.vstack(
                            rx.text(repo["titulo"]),
                            rx.link(repo["enlace"], href=str(repo["enlace"]), is_external=True),
                            align_items="start",
                        ),
                        rx.button(
                            "Eliminar",
                            on_click=lambda: SubidaRepositoriosState.delete_repo(repo["id"]),
                            color_scheme="red",
                        ),
                        justify="space-between",
                        width="100%",
                        padding="1em",
                        border="1px solid #ccc",
                        border_radius="md",
                    ),
                ),
                spacing="1em",
            ),
            on_mount=SubidaRepositoriosState.load_repositorios,
            style={
                "background_color": "#1a1a1a",
                "color": "#ffffff",
                "min_height": "100vh",
                "padding": "2em",
            },
        ),
        rx.center(
            rx.vstack(
                rx.heading("Acceso Denegado", size="lg"),
                rx.text("Por favor, inicia sesión para acceder a esta página."),
                rx.button("Ir al Login", on_click=rx.redirect("/login")),
                spacing="1em",
            ),
            width="100%",
            height="100vh",
        ),
    )