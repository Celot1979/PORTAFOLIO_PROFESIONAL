import reflex as rx
from typing import List, Dict, Any
from typing_extensions import TypedDict
from ..models.blog import BlogPost
from ..state import GlobalState
from urllib.parse import urlparse
import re

class BlogPostDict(TypedDict):
    id: int
    title: str
    content: str
    image_url: str
    created_at: str
    meta_title: str
    meta_description: str
    meta_keywords: str
    slug: str
    canonical_url: str
    og_title: str
    og_description: str
    og_image: str
    twitter_title: str
    twitter_description: str
    twitter_image: str

class SubidaBlogState(rx.State):
    title: str = ""
    content: str = ""
    image_url: str = ""
    error_message: str = ""
    posts: List[BlogPostDict] = []
    # Campos SEO
    meta_title: str = ""
    meta_description: str = ""
    meta_keywords: str = ""
    slug: str = ""
    canonical_url: str = ""
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""
    twitter_title: str = ""
    twitter_description: str = ""
    twitter_image: str = ""

    def generate_slug(self):
        """Genera un slug a partir del título."""
        if self.title:
            # Convertir a minúsculas y reemplazar espacios con guiones
            slug = self.title.lower()
            # Eliminar caracteres especiales
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            # Reemplazar espacios con guiones
            slug = re.sub(r'\s+', '-', slug)
            # Eliminar guiones múltiples
            slug = re.sub(r'-+', '-', slug)
            # Eliminar guiones al inicio y final
            slug = slug.strip('-')
            self.slug = slug

    def handle_title_change(self, value: str):
        """Maneja el cambio en el título y genera el slug."""
        self.title = value
        self.generate_slug()
        # Si no hay meta_title, usar el título
        if not self.meta_title:
            self.meta_title = value
        # Si no hay og_title, usar el título
        if not self.og_title:
            self.og_title = value
        # Si no hay twitter_title, usar el título
        if not self.twitter_title:
            self.twitter_title = value

    def handle_image_url(self, url: str):
        """Maneja la URL de la imagen."""
        if url:
            try:
                # Validar que sea una URL válida
                parsed_url = urlparse(url)
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    raise ValueError("URL inválida")
                
                self.image_url = url
                # Si no hay og_image, usar la misma imagen
                if not self.og_image:
                    self.og_image = url
                # Si no hay twitter_image, usar la misma imagen
                if not self.twitter_image:
                    self.twitter_image = url
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
                    image_url=self.image_url,
                    meta_title=self.meta_title,
                    meta_description=self.meta_description,
                    meta_keywords=self.meta_keywords,
                    slug=self.slug,
                    canonical_url=self.canonical_url,
                    og_title=self.og_title,
                    og_description=self.og_description,
                    og_image=self.og_image,
                    twitter_title=self.twitter_title,
                    twitter_description=self.twitter_description,
                    twitter_image=self.twitter_image
                )
                post.save()
                
                # Limpiar el formulario
                self.title = ""
                self.content = ""
                self.image_url = ""
                self.meta_title = ""
                self.meta_description = ""
                self.meta_keywords = ""
                self.slug = ""
                self.canonical_url = ""
                self.og_title = ""
                self.og_description = ""
                self.og_image = ""
                self.twitter_title = ""
                self.twitter_description = ""
                self.twitter_image = ""
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
                "created_at": str(post.created_at),
                "meta_title": str(post.meta_title) if post.meta_title else "",
                "meta_description": str(post.meta_description) if post.meta_description else "",
                "meta_keywords": str(post.meta_keywords) if post.meta_keywords else "",
                "slug": str(post.slug),
                "canonical_url": str(post.canonical_url) if post.canonical_url else "",
                "og_title": str(post.og_title) if post.og_title else "",
                "og_description": str(post.og_description) if post.og_description else "",
                "og_image": str(post.og_image) if post.og_image else "",
                "twitter_title": str(post.twitter_title) if post.twitter_title else "",
                "twitter_description": str(post.twitter_description) if post.twitter_description else "",
                "twitter_image": str(post.twitter_image) if post.twitter_image else ""
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
                # Campos básicos
                rx.heading("Información Básica", size="md"),
                rx.input(
                    placeholder="Título de la entrada",
                    value=SubidaBlogState.title,
                    on_change=SubidaBlogState.handle_title_change,
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
                
                # Campos SEO
                rx.heading("SEO", size="md", margin_top="2em"),
                rx.input(
                    placeholder="Meta Título",
                    value=SubidaBlogState.meta_title,
                    on_change=SubidaBlogState.set_meta_title,
                ),
                rx.text_area(
                    placeholder="Meta Descripción",
                    value=SubidaBlogState.meta_description,
                    on_change=SubidaBlogState.set_meta_description,
                    min_height="100px",
                ),
                rx.input(
                    placeholder="Meta Keywords (separadas por comas)",
                    value=SubidaBlogState.meta_keywords,
                    on_change=SubidaBlogState.set_meta_keywords,
                ),
                rx.input(
                    placeholder="Slug (URL amigable)",
                    value=SubidaBlogState.slug,
                    on_change=SubidaBlogState.set_slug,
                ),
                rx.input(
                    placeholder="URL Canónica",
                    value=SubidaBlogState.canonical_url,
                    on_change=SubidaBlogState.set_canonical_url,
                ),
                
                # Open Graph
                rx.heading("Open Graph", size="md", margin_top="2em"),
                rx.input(
                    placeholder="OG Título",
                    value=SubidaBlogState.og_title,
                    on_change=SubidaBlogState.set_og_title,
                ),
                rx.text_area(
                    placeholder="OG Descripción",
                    value=SubidaBlogState.og_description,
                    on_change=SubidaBlogState.set_og_description,
                    min_height="100px",
                ),
                rx.input(
                    placeholder="OG Imagen URL",
                    value=SubidaBlogState.og_image,
                    on_change=SubidaBlogState.set_og_image,
                ),
                
                # Twitter Cards
                rx.heading("Twitter Cards", size="md", margin_top="2em"),
                rx.input(
                    placeholder="Twitter Título",
                    value=SubidaBlogState.twitter_title,
                    on_change=SubidaBlogState.set_twitter_title,
                ),
                rx.text_area(
                    placeholder="Twitter Descripción",
                    value=SubidaBlogState.twitter_description,
                    on_change=SubidaBlogState.set_twitter_description,
                    min_height="100px",
                ),
                rx.input(
                    placeholder="Twitter Imagen URL",
                    value=SubidaBlogState.twitter_image,
                    on_change=SubidaBlogState.set_twitter_image,
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
                            rx.text(f"Slug: {post['slug']}", color="gray.500"),
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