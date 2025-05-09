import reflex as rx
from datetime import datetime

class BlogPost(rx.Model, table=True):
    title: str
    content: str
    image_url: str = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    author: str = "Admin"
    tags: str = "" 