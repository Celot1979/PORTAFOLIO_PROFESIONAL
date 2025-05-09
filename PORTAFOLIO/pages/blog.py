import reflex as rx
from ..models.blog import BlogPost
from datetime import datetime

class BlogState(rx.State):
    title: str = ""
    content: str = ""
    image_url: str = ""
    posts: list[BlogPost] = []
    show_editor: bool = False

    def load_posts(self):
        self.posts = BlogPost.select().order_by(BlogPost.created_at.desc())

    def toggle_editor(self):
        self.show_editor = not self.show_editor

    def create_post(self):
        if self.title and self.content:
            post = BlogPost(
                title=self.title,
                content=self.content,
                image_url=self.image_url,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            post.save()
            self.title = ""
            self.content = ""
            self.image_url = ""
            self.show_editor = False
            self.load_posts()

def blog():
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
                rx.textarea(
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
                rx.heading(post.title, size="md"),
                rx.cond(
                    post.image_url,
                    rx.image(
                        src=post.image_url,
                        width="100%",
                        max_width="600px",
                        margin_bottom="1em",
                    ),
                ),
                rx.markdown(post.content),
                rx.text(
                    f"Publicado el {post.created_at.strftime('%d/%m/%Y %H:%M')}",
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