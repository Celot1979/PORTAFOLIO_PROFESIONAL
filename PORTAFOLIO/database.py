import sys
import os
from dotenv import load_dotenv
from peewee import PostgresqlDatabase, SqliteDatabase

# Cargar variables de entorno
load_dotenv()

def get_database():
    """Obtiene la instancia de la base de datos según el entorno."""
    db_url = os.getenv("DATABASE_URL")
    
    if db_url and db_url.startswith("postgresql://"):
        # Parsear la URL de PostgreSQL
        from urllib.parse import urlparse
        url = urlparse(db_url)
        
        # Extraer los componentes de la URL
        db_name = url.path[1:]  # Eliminar el slash inicial
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
    else:
        # Fallback a SQLite para desarrollo local
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(os.path.dirname(current_dir), 'reflex.db')
        return SqliteDatabase(db_path)

# Crear la instancia de la base de datos
db = get_database()

def init_db():
    """Inicializa la base de datos."""
    try:
        # Conectar a la base de datos
        db.connect()
        
        # Importar los modelos aquí para evitar importaciones circulares
        from .models.blog import BlogPost
        from .models.repositorio import Repositorio
        
        # Crear las tablas si no existen
        db.create_tables([Repositorio, BlogPost], safe=True)
        
        print("Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        raise e
    finally:
        # Cerrar la conexión
        if not db.is_closed():
            db.close()