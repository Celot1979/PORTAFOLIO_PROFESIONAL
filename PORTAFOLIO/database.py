from peewee import SqliteDatabase
import os

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al directorio BBDD
db_dir = os.path.join(current_dir, "BBDD")
# Asegurarse de que el directorio existe
os.makedirs(db_dir, exist_ok=True)
# Construir la ruta completa a la base de datos
db_path = os.path.join(db_dir, "blog.db")

# Crear la instancia de la base de datos
db = SqliteDatabase(db_path)

# Función para inicializar la base de datos
def init_db():
    db.connect()
    # Importar aquí para evitar importación circular
    from .models.repositorio import Repositorio
    from .models.blog import BlogPost
    db.create_tables([Repositorio, BlogPost], safe=True)
    db.close()