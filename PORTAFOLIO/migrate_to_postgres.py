import os
import sys
from peewee import SqliteDatabase, PostgresqlDatabase
from dotenv import load_dotenv

# Añadir el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.blog import BlogPost
from models.repositorio import Repositorio

# Cargar variables de entorno
load_dotenv()

def migrate_data():
    # Conectar a la base de datos SQLite
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sqlite_db_path = os.path.join(os.path.dirname(current_dir), 'reflex.db')
    sqlite_db = SqliteDatabase(sqlite_db_path)
    
    # Obtener la URL de PostgreSQL del archivo .env
    db_url = os.getenv("DATABASE_URL")
    if not db_url or not db_url.startswith("postgresql://"):
        raise ValueError("DATABASE_URL no está configurada correctamente en el archivo .env")
    
    # Parsear la URL de PostgreSQL
    from urllib.parse import urlparse
    url = urlparse(db_url)
    
    # Extraer los componentes de la URL
    db_name = url.path[1:]  # Eliminar el slash inicial
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port or 5432
    
    # Conectar a PostgreSQL
    pg_db = PostgresqlDatabase(
        db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    try:
        # Conectar a ambas bases de datos
        sqlite_db.connect()
        pg_db.connect()
        
        # Crear las tablas en PostgreSQL
        pg_db.create_tables([BlogPost, Repositorio])
        
        # Migrar datos de BlogPost
        print("Migrando datos de BlogPost...")
        for post in BlogPost.select():
            BlogPost.create(
                title=post.title,
                content=post.content,
                image_url=post.image_url,
                created_at=post.created_at,
                updated_at=post.updated_at,
                meta_title=post.meta_title,
                meta_description=post.meta_description,
                meta_keywords=post.meta_keywords,
                slug=post.slug,
                canonical_url=post.canonical_url,
                og_title=post.og_title,
                og_description=post.og_description,
                og_image=post.og_image,
                twitter_title=post.twitter_title,
                twitter_description=post.twitter_description,
                twitter_image=post.twitter_image
            )
        
        # Migrar datos de Repositorio
        print("Migrando datos de Repositorio...")
        for repo in Repositorio.select():
            Repositorio.create(
                titulo=repo.titulo,
                enlace=repo.enlace,
                imagen=repo.imagen
            )
        
        print("Migración completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")
        raise e
    finally:
        # Cerrar las conexiones
        if not sqlite_db.is_closed():
            sqlite_db.close()
        if not pg_db.is_closed():
            pg_db.close()

if __name__ == "__main__":
    migrate_data() 