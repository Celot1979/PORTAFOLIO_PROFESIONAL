import reflex as rx
from typing import List, Dict, Any
from typing_extensions import TypedDict
from ..models.repositorio import Repositorio

class RepositorioDict(TypedDict):
    id: int
    titulo: str
    enlace: str
    imagen: str

class ProyectosState(rx.State):
    repositorios: List[RepositorioDict] = []

    def load_repositorios(self):
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

def proyectos():
    return rx.vstack(
        rx.heading("Mis Proyectos", size="lg", margin_bottom="1em"),
        rx.text(
            "Aquí encontrarás una colección de mis proyectos más destacados. "
            "Cada proyecto representa un desafío único y una oportunidad de aprendizaje.",
            margin_bottom="2em",
        ),
        rx.flex(
            rx.foreach(
                ProyectosState.repositorios,
                lambda repo: rx.box(
                    rx.vstack(
                        rx.image(
                            src=repo["imagen"],
                            width="100%",
                            height="200px",
                            object_fit="cover",
                            border_radius="lg",
                        ),
                        rx.heading(repo["titulo"], size="md"),
                        rx.link(
                            "Ver en GitHub",
                            href=str(repo["enlace"]),
                            is_external=True,
                            color="blue.400",
                        ),
                        align_items="start",
                        spacing="1em",
                        padding="1em",
                        border="1px solid #2d3748",
                        border_radius="lg",
                        background="rgba(255, 255, 255, 0.05)",
                        _hover={
                            "transform": "translateY(-5px)",
                            "transition": "all 0.3s ease",
                        },
                    ),
                    width="300px",
                ),
            ),
            wrap="wrap",
            gap="2em",
            justify="center",
        ),
        on_mount=ProyectosState.load_repositorios,
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 