import os
from dotenv import load_dotenv
from peewee import SqliteDatabase, PostgresqlDatabase
from urllib.parse import urlparse
from models.blog import BlogPost
from models.repositorio import Repositorio

# Cargar variables de entorno
load_dotenv()

def get_sqlite_db():
    """Obtiene la conexión a la base de datos SQLite."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(current_dir), 'reflex.db')
    return SqliteDatabase(db_path)

def get_postgres_db():
    """Obtiene la conexión a la base de datos PostgreSQL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL no está configurada")
    
    url = urlparse(db_url)
    db_name = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port or 5432
    
    return PostgresqlDatabase(
        db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )

def migrate_data():
    """Migra los datos de SQLite a PostgreSQL."""
    sqlite_db = get_sqlite_db()
    postgres_db = get_postgres_db()
    
    try:
        # Conectar a ambas bases de datos
        sqlite_db.connect()
        postgres_db.connect()
        
        # Crear tablas en PostgreSQL
        postgres_db.create_tables([BlogPost, Repositorio], safe=True)
        
        # Migrar datos de BlogPost
        for post in BlogPost.select():
            BlogPost.create(
                id=post.id,
                title=post.title,
                content=post.content,
                slug=post.slug,
                created_at=post.created_at,
                updated_at=post.updated_at
            )
        
        # Migrar datos de Repositorio
        for repo in Repositorio.select():
            Repositorio.create(
                id=repo.id,
                name=repo.name,
                description=repo.description,
                url=repo.url,
                created_at=repo.created_at,
                updated_at=repo.updated_at
            )
        
        print("Migración completada exitosamente")
        
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")
        raise e
    finally:
        if not sqlite_db.is_closed():
            sqlite_db.close()
        if not postgres_db.is_closed():
            postgres_db.close()

if __name__ == "__main__":
    migrate_data() 