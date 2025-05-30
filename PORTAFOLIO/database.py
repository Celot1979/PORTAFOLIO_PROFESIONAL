import sys
import os
from dotenv import load_dotenv
from peewee import SqliteDatabase

# Cargar variables de entorno
load_dotenv()

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta a la base de datos
db_path = os.path.join(os.path.dirname(current_dir), 'reflex.db')

# Crear la base de datos SQLite
db = SqliteDatabase(db_path)

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