import sys
import os
from dotenv import load_dotenv
from peewee import PostgresqlDatabase

# Cargar variables de entorno
load_dotenv()

def get_database():
    """Obtiene la instancia de la base de datos PostgreSQL."""
    # Intentar obtener la URL de la base de datos de diferentes fuentes
    db_url = os.getenv("DATABASE_URL")  # Para Reflex Cloud
    local_db_url = os.getenv("LOCAL_DATABASE_URL")  # Para desarrollo local
    
    # Imprimir información de diagnóstico
    print("=== Información de la Base de Datos ===")
    
    # Determinar qué URL usar
    if db_url and not db_url.startswith("postgresql://tu_"):
        print("Usando DATABASE_URL (producción)")
        selected_url = db_url
    elif local_db_url:
        print("Usando LOCAL_DATABASE_URL (desarrollo local)")
        selected_url = local_db_url
    else:
        raise ValueError("No se encontró una URL de base de datos válida. Asegúrate de configurar LOCAL_DATABASE_URL en tu archivo .env")
    
    print(f"URL de la base de datos: {selected_url}")
    
    if not selected_url.startswith("postgresql://"):
        raise ValueError("La URL de la base de datos debe comenzar con 'postgresql://'")
    
    # Parsear la URL de PostgreSQL
    from urllib.parse import urlparse
    url = urlparse(selected_url)
    
    # Extraer los componentes de la URL
    db_name = url.path[1:]  # Eliminar el slash inicial
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port or 5432
    
    print(f"Base de datos: {db_name}")
    print(f"Usuario: {user}")
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    print("=====================================")
    
    # Crear la instancia de PostgreSQL
    db = PostgresqlDatabase(
        db_name,
        user=user,
        password=password,
        host=host,
        port=port,
        sslmode='require' if host != 'localhost' else None  # Usar SSL en producción
    )
    
    # Verificar la conexión
    try:
        db.connect()
        print("✓ Conexión exitosa a PostgreSQL")
        db.close()
    except Exception as e:
        print(f"✗ Error al conectar con PostgreSQL: {str(e)}")
        print("\nSugerencias para solucionar el error:")
        print("1. Verifica que PostgreSQL esté instalado y ejecutándose")
        print("2. Asegúrate de que la base de datos exista")
        print("3. Verifica que el usuario y contraseña sean correctos")
        print("4. Si estás en desarrollo local, asegúrate de que LOCAL_DATABASE_URL esté configurado correctamente")
        raise
    
    return db

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
        
        print("✓ Base de datos inicializada correctamente ll")
        
        # Verificar los datos
        from .database_utils import verify_data, export_data
        verify_data()
        
        # Exportar datos
        backup_file = export_data()
        print(f"Respaldo creado en: {backup_file}")
        
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {str(e)}")
        raise e
    finally:
        # Cerrar la conexión
        if not db.is_closed():
            db.close()