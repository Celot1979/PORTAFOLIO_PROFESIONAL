import sys
import os
from dotenv import load_dotenv
from peewee import SqliteDatabase

# Cargar variables de entorno
load_dotenv()

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al directorio BBDD
db_dir = os.path.join(current_dir, "BBDD")
# Asegurarse de que el directorio existe
os.makedirs(db_dir, exist_ok=True)
# Construir la ruta completa a la base de datos
db_path = os.path.join(db_dir, os.getenv("DB_PATH", "blog.db"))

# Crear la base de datos
db = SqliteDatabase(db_path)

# Función para inicializar la base de datos
def init_db():
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        # Importar aquí para evitar importación circular
        from PORTAFOLIO.models.repositorio import Repositorio
        from PORTAFOLIO.models.blog import BlogPost
        db.create_tables([Repositorio, BlogPost], safe=True)
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise e
    finally:
        if not db.is_closed():
            db.close()