import reflex as rx
from ..models.blog import BlogPost
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..components.navbar import navbar
from typing_extensions import TypedDict
from ..state import GlobalState
from ..database import db

class BlogPostDict(TypedDict):
    id: str
    title: str
    content: str
    image_url: str
    created_at: str
    updated_at: str
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

class BlogState(rx.State):
    """Estado para el blog."""
    posts: List[Dict[str, str]] = []
    selected_post_title: str = ""
    selected_post_content: str = ""
    selected_post_image_url: str = ""
    selected_post_created_at: str = ""
    selected_post_meta_title: str = ""
    selected_post_meta_description: str = ""
    selected_post_og_title: str = ""
    selected_post_og_description: str = ""
    selected_post_og_image: str = ""
    selected_post_twitter_title: str = ""
    selected_post_twitter_description: str = ""
    selected_post_twitter_image: str = ""
    current_slug: Optional[str] = None

    def load_posts(self):
        """Carga los posts desde la base de datos."""
        with db.atomic():
            db_posts = BlogPost.select().order_by(BlogPost.created_at.desc())
            self.posts = [
                {
                    "id": str(post.id),
                    "title": str(post.title) if post.title else "",
                    "content": str(post.content) if post.content else "",
                    "image_url": str(post.image_url) if post.image_url else "",
                    "created_at": post.created_at.strftime('%d/%m/%Y') if post.created_at else "",
                    "meta_title": str(post.meta_title) if post.meta_title else "",
                    "meta_description": str(post.meta_description) if post.meta_description else "",
                    "meta_keywords": str(post.meta_keywords) if post.meta_keywords else "",
                    "slug": str(post.slug) if post.slug else "",
                    "canonical_url": str(post.canonical_url) if post.canonical_url else "",
                    "og_title": str(post.og_title) if post.og_title else "",
                    "og_description": str(post.og_description) if post.og_description else "",
                    "og_image": str(post.og_image) if post.og_image else "",
                    "twitter_title": str(post.twitter_title) if post.twitter_title else "",
                    "twitter_description": str(post.twitter_description) if post.twitter_description else "",
                    "twitter_image": str(post.twitter_image) if post.twitter_image else "",
                }
                for post in db_posts
            ]

    def select_post(self, post_id: str):
        """Selecciona un post para ver sus detalles."""
        post = next((p for p in self.posts if p["id"] == post_id), None)
        if post:
            self.selected_post_title = post["title"]
            self.selected_post_content = post["content"]
            self.selected_post_image_url = post["image_url"]
            self.selected_post_created_at = post["created_at"]
            self.selected_post_meta_title = post["meta_title"] or post["title"]
            self.selected_post_meta_description = post["meta_description"] or post["content"][:160]
            self.selected_post_og_title = post["og_title"] or post["title"]
            self.selected_post_og_description = post["og_description"] or post["content"][:160]
            self.selected_post_og_image = post["og_image"] or post["image_url"]
            self.selected_post_twitter_title = post["twitter_title"] or post["title"]
            self.selected_post_twitter_description = post["twitter_description"] or post["content"][:160]
            self.selected_post_twitter_image = post["twitter_image"] or post["image_url"]
            self.current_slug = post["slug"]
            # Actualizar la URL sin recargar la página
            rx.window.history.push_state({}, f"/blog/{post['slug']}")

    def clear_selection(self):
        """Limpia la selección actual y vuelve a la lista de posts."""
        self.selected_post_title = ""
        self.selected_post_content = ""
        self.selected_post_image_url = ""
        self.selected_post_created_at = ""
        self.selected_post_meta_title = ""
        self.selected_post_meta_description = ""
        self.selected_post_og_title = ""
        self.selected_post_og_description = ""
        self.selected_post_og_image = ""
        self.selected_post_twitter_title = ""
        self.selected_post_twitter_description = ""
        self.selected_post_twitter_image = ""
        self.current_slug = None
        # Actualizar la URL sin recargar la página
        rx.window.history.push_state({}, "/blog")

    def load_post_by_slug(self, slug: str):
        """Carga un post específico por su slug."""
        with db.atomic():
            post = BlogPost.get_or_none(BlogPost.slug == slug)
            if post:
                self.selected_post_title = post.title
                self.selected_post_content = post.content
                self.selected_post_image_url = post.image_url
                self.selected_post_created_at = post.created_at.strftime('%d/%m/%Y')
                self.selected_post_meta_title = post.meta_title or post.title
                self.selected_post_meta_description = post.meta_description or post.content[:160]
                self.selected_post_og_title = post.og_title or post.title
                self.selected_post_og_description = post.og_description or post.content[:160]
                self.selected_post_og_image = post.og_image or post.image_url
                self.selected_post_twitter_title = post.twitter_title or post.title
                self.selected_post_twitter_description = post.twitter_description or post.content[:160]
                self.selected_post_twitter_image = post.twitter_image or post.image_url
                self.current_slug = slug

def blog():
    """Página principal del blog."""
    def render_post(post: Dict[str, str]):
        return rx.box(
            rx.vstack(
                rx.heading(post["title"], size="3"),
                rx.text(f"Publicado el {post['created_at']}", color="gray"),
                rx.image(post["image_url"], width="100%", height="200px", object_fit="cover"),
                rx.text(post["content"][:200] + "...", color="gray"),
                rx.button("Leer más", on_click=lambda: BlogState.select_post(post["id"])),
                padding="1em",
                background_color="#2d2d2d",
                border_radius="lg",
                width="300px",
                _hover={"transform": "translateY(-5px)", "transition": "all 0.3s ease"},
            ),
            margin="1em",
        )

    return rx.vstack(
        navbar(),
        rx.heading("Blog", size="2", margin_bottom="2em"),
        rx.cond(
            BlogState.current_slug,
            rx.vstack(
                rx.button("← Volver", on_click=BlogState.clear_selection, margin_bottom="1em"),
                rx.heading(BlogState.selected_post_title, size="1"),
                rx.text(f"Publicado el {BlogState.selected_post_created_at}", color="gray"),
                rx.image(BlogState.selected_post_image_url, width="100%", max_width="800px", margin_y="2em"),
                rx.markdown(BlogState.selected_post_content),
                # Meta tags para SEO
                rx.script("""
                    document.title = arguments[0];
                    document.querySelector('meta[name="description"]').setAttribute('content', arguments[1]);
                    document.querySelector('meta[property="og:title"]').setAttribute('content', arguments[2]);
                    document.querySelector('meta[property="og:description"]').setAttribute('content', arguments[3]);
                    document.querySelector('meta[property="og:image"]').setAttribute('content', arguments[4]);
                    document.querySelector('meta[name="twitter:title"]').setAttribute('content', arguments[5]);
                    document.querySelector('meta[name="twitter:description"]').setAttribute('content', arguments[6]);
                    document.querySelector('meta[name="twitter:image"]').setAttribute('content', arguments[7]);
                """, 
                BlogState.selected_post_meta_title,
                BlogState.selected_post_meta_description,
                BlogState.selected_post_og_title,
                BlogState.selected_post_og_description,
                BlogState.selected_post_og_image,
                BlogState.selected_post_twitter_title,
                BlogState.selected_post_twitter_description,
                BlogState.selected_post_twitter_image),
                width="100%",
                max_width="800px",
                padding="2em",
            ),
            rx.vstack(
                rx.foreach(
                    BlogState.posts,
                    render_post
                ),
                direction="row",
                wrap="wrap",
                justify="center",
                spacing="1",
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

def blog_post(slug: Optional[str] = None):
    """Página individual de un post del blog."""
    if not slug:
        return rx.vstack(
            navbar(),
            rx.heading("Blog", size="2", margin_bottom="2em"),
            rx.text("Post no encontrado"),
            style={
                "background_color": "#1a1a1a",
                "color": "#ffffff",
                "min_height": "100vh",
                "padding": "2em",
            },
        )
    return rx.vstack(
        navbar(),
        rx.heading("Blog", size="2", margin_bottom="2em"),
        rx.cond(
            BlogState.current_slug,
            rx.vstack(
                rx.button("← Volver", on_click=BlogState.clear_selection, margin_bottom="1em"),
                rx.heading(BlogState.selected_post_title, size="1"),
                rx.text(f"Publicado el {BlogState.selected_post_created_at}", color="gray"),
                rx.image(BlogState.selected_post_image_url, width="100%", max_width="800px", margin_y="2em"),
                rx.markdown(BlogState.selected_post_content),
                # Meta tags para SEO
                rx.script("""
                    document.title = arguments[0];
                    document.querySelector('meta[name=\"description\"]').setAttribute('content', arguments[1]);
                    document.querySelector('meta[property=\"og:title\"]').setAttribute('content', arguments[2]);
                    document.querySelector('meta[property=\"og:description\"]').setAttribute('content', arguments[3]);
                    document.querySelector('meta[property=\"og:image\"]').setAttribute('content', arguments[4]);
                    document.querySelector('meta[name=\"twitter:title\"]').setAttribute('content', arguments[5]);
                    document.querySelector('meta[name=\"twitter:description\"]').setAttribute('content', arguments[6]);
                    document.querySelector('meta[name=\"twitter:image\"]').setAttribute('content', arguments[7]);
                """,
                BlogState.selected_post_meta_title,
                BlogState.selected_post_meta_description,
                BlogState.selected_post_og_title,
                BlogState.selected_post_og_description,
                BlogState.selected_post_og_image,
                BlogState.selected_post_twitter_title,
                BlogState.selected_post_twitter_description,
                BlogState.selected_post_twitter_image),
                width="100%",
                max_width="800px",
                padding="2em",
            ),
            rx.text("Post no encontrado"),
        ),
        on_mount=lambda: BlogState.load_post_by_slug(slug),
        style={
            "background_color": "#1a1a1a",
            "color": "#ffffff",
            "min_height": "100vh",
            "padding": "2em",
        },
    ) 