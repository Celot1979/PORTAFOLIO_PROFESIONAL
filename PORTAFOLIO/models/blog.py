from peewee import *
from datetime import datetime
from ..database import db
import re

def generate_unique_slug(title: str) -> str:
    """Genera un slug único a partir del título."""
    # Convertir a minúsculas y reemplazar espacios con guiones
    slug = title.lower()
    # Eliminar caracteres especiales
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Reemplazar espacios con guiones
    slug = re.sub(r'\s+', '-', slug)
    # Eliminar guiones múltiples
    slug = re.sub(r'-+', '-', slug)
    # Eliminar guiones al inicio y final
    slug = slug.strip('-')
    
    # Verificar si el slug ya existe
    base_slug = slug
    counter = 1
    while BlogPost.select().where(BlogPost.slug == slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug

# Define el modelo BlogPost
class BlogPost(Model):
    title = CharField()
    content = TextField()
    image_url = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    # Campos SEO
    meta_title = CharField(null=True)
    meta_description = TextField(null=True)
    meta_keywords = CharField(null=True)
    slug = CharField(unique=True)
    canonical_url = CharField(null=True)
    og_title = CharField(null=True)
    og_description = TextField(null=True)
    og_image = CharField(null=True)
    twitter_title = CharField(null=True)
    twitter_description = TextField(null=True)
    twitter_image = CharField(null=True)

    class Meta:
        database = db

    def __repr__(self):
        return f"<BlogPost(title='{self.title}')>"

    def save(self):
        """Guarda el post y genera un slug único si no existe."""
        if not self.slug:
            self.slug = generate_unique_slug(self.title)
        self.updated_at = datetime.now()
        return super().save()