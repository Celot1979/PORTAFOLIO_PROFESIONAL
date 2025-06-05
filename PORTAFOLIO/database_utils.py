import json
import os
from datetime import datetime
from .models.blog import BlogPost
from .models.repositorio import Repositorio
from .database import db

def export_data():
    """Exporta todos los datos a archivos JSON."""
    data = {
        'blog_posts': [],
        'repositorios': []
    }
    
    # Exportar posts del blog
    for post in BlogPost.select():
        data['blog_posts'].append({
            'title': post.title,
            'content': post.content,
            'image_url': post.image_url,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            'meta_title': post.meta_title,
            'meta_description': post.meta_description,
            'meta_keywords': post.meta_keywords,
            'slug': post.slug,
            'canonical_url': post.canonical_url,
            'og_title': post.og_title,
            'og_description': post.og_description,
            'og_image': post.og_image,
            'twitter_title': post.twitter_title,
            'twitter_description': post.twitter_description,
            'twitter_image': post.twitter_image
        })
    
    # Exportar repositorios
    for repo in Repositorio.select():
        data['repositorios'].append({
            'titulo': repo.titulo,
            'enlace': repo.enlace,
            'imagen': repo.imagen
        })
    
    # Crear directorio de backup si no existe
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Guardar datos en archivo JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return backup_file

def import_data(backup_file):
    """Importa datos desde un archivo JSON."""
    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Importar posts del blog
    for post_data in data['blog_posts']:
        BlogPost.create(**post_data)
    
    # Importar repositorios
    for repo_data in data['repositorios']:
        Repositorio.create(**repo_data)

def verify_data():
    """Verifica que los datos estén correctamente almacenados."""
    results = {
        'blog_posts': {
            'total': BlogPost.select().count(),
            'with_images': BlogPost.select().where(BlogPost.image_url.is_null(False)).count()
        },
        'repositorios': {
            'total': Repositorio.select().count(),
            'with_images': Repositorio.select().where(Repositorio.imagen.is_null(False)).count()
        }
    }
    
    print("\n=== Verificación de Datos ===")
    print(f"Posts del blog: {results['blog_posts']['total']} (con imágenes: {results['blog_posts']['with_images']})")
    print(f"Repositorios: {results['repositorios']['total']} (con imágenes: {results['repositorios']['with_images']})")
    print("===========================\n")
    
    return results 