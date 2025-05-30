import os
import sys

# Añadir el directorio actual al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from database import db

def init_db():
    try:
        print("Conectando a la base de datos...")
        db.connect()
        
        print("Creando tablas...")
        from models.repositorio import Repositorio
        from models.blog import BlogPost
        
        db.create_tables([Repositorio, BlogPost], safe=True)
        print("Tablas creadas correctamente.")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise e
    finally:
        if not db.is_closed():
            db.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    try:
        print("Inicializando base de datos...")
        init_db()
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        sys.exit(1) 