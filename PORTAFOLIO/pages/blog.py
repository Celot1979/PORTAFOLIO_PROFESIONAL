import reflex as rx
from ..models.blog import BlogPost
from ..database import get_db, Base, engine
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Crear las tablas si no existen
Base.metadata.create_all(engine)

class BlogState(rx.State):
    title: str = ""
    content: str = ""
    image_url: str = ""
    posts: List[Dict[str, Any]] = []
    show_editor: bool = False

    def load_posts(self):
        """Loads blog posts from the database."""
        db: Session = next(get_db())  # Obtiene una sesión de la base de datos
        db_posts = db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()
        self.posts = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "image_url": post.image_url,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for post in db_posts
        ]

    def toggle_editor(self):
        """Toggles the visibility of the blog post editor."""
        self.show_editor = not self.show_editor

    def create_post(self):
        """Creates a new blog post and saves it to the database."""
        if self.title and self.content:
            db: Session = next(get_db())  # Obtiene una sesión de la base de datos
            post = BlogPost(
                title=self.title,
                content=self.content,
                image_url=self.image_url,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            post.save(db)  # Pasa la sesión al método save
            self.title = ""
            self.content = ""
            self.image_url = ""
            self.show_editor = False
            self.load_posts()

def blog():
    """Defines the UI for the blog page."""
    return rx.vstack(
        rx.heading("Blog", size="lg", margin_bottom="1em"),
        rx.button(
            "Nueva Entrada",
            on_click=BlogState.toggle_editor,
            margin_bottom="2em",
            background_color="#4CAF50",
            color="white",
            _hover={"background_color": "#45a049"},
        ),
        rx.cond(
            BlogState.show_editor,
            rx.vstack(
                rx.input(
                    placeholder="Título",
                    value=BlogState.title,
                    on_change=BlogState.set_title,
                    margin_bottom="1em",
                ),
                rx.text_area(
                    placeholder="Contenido",
                    value=BlogState.content,
                    on_change=BlogState.set_content,
                    height="200px",
                    margin_bottom="1em",
                ),
                rx.input(
                    placeholder="URL de la imagen",
                    value=BlogState.image_url,
                    on_change=BlogState.set_image_url,
                    margin_bottom="1em",
                ),
                rx.button(
                    "Publicar",
                    on_click=BlogState.create_post,
                    background_color="#4CAF50",
                    color="white",
                    _hover={"background_color": "#45a049"},
                ),
                padding="2em",
                background_color="#2d2d2d",
                border_radius="10px",
                margin_bottom="2em",
            ),
        ),
        rx.foreach(
            BlogState.posts,
            lambda post: rx.vstack(
                rx.heading(post["title"], size="md"),
                rx.cond(
                    post["image_url"],
                    rx.image(
                        src=post["image_url"],
                        width="100%",
                        max_width="600px",
                        margin_bottom="1em",
                    ),
                ),
                rx.markdown(post["content"]),
                rx.text(
                    f"Publicado el {post['created_at']}",
                    font_size="0.8em",
                    color="#888888",
                ),
                padding="2em",
                background_color="#2d2d2d",
                border_radius="10px",
                margin_bottom="2em",
                width="100%",
                max_width="800px",
            ),
        ),
        on_mount=BlogState.load_posts,
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    )