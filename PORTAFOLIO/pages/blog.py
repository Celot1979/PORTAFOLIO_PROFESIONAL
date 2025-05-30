import reflex as rx
from ..models.blog import BlogPost
from datetime import datetime
from typing import List, Dict, Any
from ..components.navbar import navbar

class BlogState(rx.State):
    posts: List[Dict[str, Any]] = []

    def load_posts(self):
        """Loads blog posts from the database."""
        db_posts = BlogPost.select().order_by(BlogPost.created_at.desc())
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

def blog():
    """Defines the UI for the blog page."""
    return rx.vstack(
        navbar(),
        rx.heading("Blog", size="lg", margin_bottom="1em"),
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