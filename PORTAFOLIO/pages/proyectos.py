import reflex as rx
from typing import List, Dict, Any
from typing_extensions import TypedDict
from ..models.repositorio import Repositorio
from ..components.navbar import navbar

class RepositorioDict(TypedDict):
    id: int
    titulo: str
    enlace: str
    imagen: str

class ProyectosState(rx.State):
    repositorios: List[RepositorioDict] = []
    error_message: str = ""
    is_empty: bool = True

    def load_repositorios(self):
        try:
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
            self.is_empty = len(self.repositorios) == 0
            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error al cargar los repositorios: {str(e)}"
            self.repositorios = []
            self.is_empty = True

def proyectos():
    return rx.vstack(
        navbar(),
        rx.heading("Mis Proyectos", size="lg", margin_bottom="1em"),
        rx.text(
            "Aquí encontrarás una colección de mis proyectos más destacados. "
            "Cada proyecto representa un desafío único y una oportunidad de aprendizaje.",
            margin_bottom="2em",
        ),
        rx.cond(
            ProyectosState.error_message,
            rx.text(ProyectosState.error_message, color="red"),
        ),
        rx.cond(
            ProyectosState.is_empty,
            rx.text("No hay proyectos disponibles en este momento.", color="gray.400"),
            rx.vstack(
                rx.foreach(
                    ProyectosState.repositorios,
                    lambda repo: rx.box(
                        rx.vstack(
                            rx.image(
                                src=repo["imagen"],
                                width="100%",
                                max_height="400px",
                                object_fit="contain",
                                border_radius="lg",
                                fallback="https://via.placeholder.com/800x400?text=Imagen+no+disponible",
                            ),
                            rx.heading(repo["titulo"], size="md", margin_top="1em"),
                            rx.link(
                                "Ver en GitHub",
                                href=str(repo["enlace"]),
                                is_external=True,
                                color="blue.400",
                                _hover={"text_decoration": "underline"},
                            ),
                            align_items="start",
                            spacing="1em",
                            padding="2em",
                            border="1px solid #2d3748",
                            border_radius="lg",
                            background="rgba(255, 255, 255, 0.05)",
                            _hover={
                                "transform": "translateY(-5px)",
                                "transition": "all 0.3s ease",
                                "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                            },
                        ),
                        width="100%",
                        max_width="800px",
                        margin_bottom="2em",
                    ),
                ),
                spacing="2em",
                align="center",
                width="100%",
            ),
        ),
        on_mount=ProyectosState.load_repositorios,
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 