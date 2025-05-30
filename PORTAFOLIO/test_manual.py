import os
import sys

# Añadir el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PORTAFOLIO.models.repositorio import Repositorio
from PORTAFOLIO.database import db

# Conectar a la base de datos
db.connect()
db.create_tables([Repositorio])

# Crear un repositorio de prueba
print("1. Creando repositorio de prueba...")
repo_id = Repositorio.create(
    titulo="Proyecto de Prueba",
    enlace="https://github.com/test",
    imagen="/static/uploads/test_image.jpg"
)
repo = Repositorio.get_by_id(repo_id)
print(f"Repositorio creado con ID: {repo.id}")

# Verificar que se creó correctamente
print("\n2. Verificando datos del repositorio...")
repo_db = Repositorio.get_by_id(repo.id)
print(f"Título: {repo_db.titulo}")
print(f"Enlace: {repo_db.enlace}")
print(f"Imagen: {repo_db.imagen}")

# Probar la eliminación
print("\n3. Eliminando repositorio...")
Repositorio.delete_by_id(repo.id)
repo_deleted = Repositorio.get_or_none(id=repo.id)
print(f"¿Repositorio eliminado?: {repo_deleted is None}")

# Cerrar la conexión
db.close() 