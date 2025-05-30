import reflex as rx
from typing import List, Dict, Any
from typing_extensions import TypedDict
from ..models.blog import BlogPost
from ..state import GlobalState
from urllib.parse import urlparse

class BlogPostDict(TypedDict):
    id: int
    title: str
    content: str
    image_url: str
    created_at: str

class SubidaBlogState(rx.State):
    title: str = ""
    content: str = ""
    image_url: str = ""
    error_message: str = ""
    posts: List[BlogPostDict] = []

    def handle_image_url(self, url: str):
        """Maneja la URL de la imagen."""
        if url:
            try:
                # Validar que sea una URL válida
                parsed_url = urlparse(url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    raise ValueError("URL inválida")
                
                self.image_url = url
                self.error_message = ""
                
            except Exception as e:
                print(f"Error al validar la URL: {str(e)}")
                self.error_message = f"Error al validar la URL: {str(e)}"

    def handle_submit(self):
        """Maneja el envío del formulario."""
        if self.title and self.content and self.image_url:
            try:
                # Crear la entrada del blog
                post = BlogPost(
                    title=self.title,
                    content=self.content,
                    image_url=self.image_url
                )
                post.save()
                
                # Limpiar el formulario
                self.title = ""
                self.content = ""
                self.image_url = ""
                self.error_message = ""
                
                # Recargar la lista de posts
                self.load_posts()
            except Exception as e:
                self.error_message = f"Error al crear la entrada: {str(e)}"

    def load_posts(self):
        """Carga la lista de posts desde la base de datos."""
        db_posts = BlogPost.select().order_by(BlogPost.id.desc())
        self.posts = [
            {
                "id": int(post.id),
                "title": str(post.title),
                "content": str(post.content),
                "image_url": str(post.image_url),
                "created_at": str(post.created_at)
            }
            for post in db_posts
        ]

    def delete_post(self, post_id: int):
        """Elimina una entrada del blog."""
        BlogPost.delete_by_id(post_id)
        self.load_posts()

def subida_blog():
    return rx.cond(
        GlobalState.is_authenticated,
        rx.vstack(
            rx.hstack(
                rx.heading("Gestión del Blog", size="lg"),
                rx.spacer(),
                rx.button("Cerrar Sesión", on_click=GlobalState.logout, color_scheme="red"),
                width="100%",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.input(
                    placeholder="Título de la entrada",
                    value=SubidaBlogState.title,
                    on_change=SubidaBlogState.set_title,
                    required=True,
                ),
                rx.text_area(
                    placeholder="Contenido de la entrada",
                    value=SubidaBlogState.content,
                    on_change=SubidaBlogState.set_content,
                    required=True,
                    min_height="200px",
                    width="100%",
                    resize="vertical",
                    padding="1em",
                    border="1px solid #2d3748",
                    border_radius="md",
                    background="rgba(255, 255, 255, 0.05)",
                    color="white",
                    _focus={
                        "border_color": "#4CAF50",
                        "box_shadow": "0 0 0 1px #4CAF50",
                    },
                ),
                rx.input(
                    placeholder="URL de la imagen (ej: https://ejemplo.com/imagen.jpg)",
                    value=SubidaBlogState.image_url,
                    on_change=SubidaBlogState.handle_image_url,
                    required=True,
                ),
                rx.cond(
                    SubidaBlogState.image_url,
                    rx.image(src=SubidaBlogState.image_url, width="200px", height="200px"),
                ),
                rx.cond(
                    SubidaBlogState.error_message,
                    rx.text(SubidaBlogState.error_message, color="red"),
                ),
                rx.button(
                    "Publicar Entrada",
                    on_click=SubidaBlogState.handle_submit,
                ),
                spacing="1em",
            ),
            rx.divider(),
            rx.heading("Entradas Existentes", size="md", margin_top="2em"),
            rx.vstack(
                rx.foreach(
                    SubidaBlogState.posts,
                    lambda post: rx.box(
                        rx.vstack(
                            rx.image(src=post["image_url"], width="100px", height="100px"),
                            rx.heading(post["title"], size="md"),
                            rx.text(str(post["content"])[:200] + "...", color="gray.400"),
                            rx.text(f"Fecha: {post['created_at']}", color="gray.500"),
                            rx.button(
                                "Eliminar",
                                on_click=lambda: SubidaBlogState.delete_post(post["id"]),
                                color_scheme="red",
                            ),
                            align_items="start",
                            spacing="1em",
                        ),
                        width="100%",
                        padding="1em",
                        border="1px solid #ccc",
                        border_radius="md",
                    ),
                ),
                spacing="1em",
            ),
            on_mount=SubidaBlogState.load_posts,
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