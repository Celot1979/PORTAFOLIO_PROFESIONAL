import sqlite3
import os
from peewee import *
import sys

# Añadir el directorio padre al path para poder importar database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

def test_sqlite():
    """Prueba la conexión a SQLite."""
    db_path = "/Users/danielgil/Documents/REFLEX/RUN/blog.db"
    print("\n=== Probando conexión SQLite ===")
    print(f"Ruta de la base de datos SQLite: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        print("✓ Conexión exitosa a SQLite")
        conn.close()
    except sqlite3.Error as e:
        print(f"✗ Error al conectar a SQLite: {e}")

def test_postgresql():
    """Prueba la conexión a PostgreSQL."""
    print("\n=== Probando conexión PostgreSQL ===")
    try:
        # Intentar conectar a la base de datos
        db.connect()
        
        # Obtener información de la base de datos
        cursor = db.execute_sql('SELECT version();')
        version = cursor.fetchone()[0]
        
        print(f"✓ Versión de PostgreSQL: {version}")
        print(f"✓ Base de datos conectada: {db.database}")
        print(f"✓ Host: {db.connect_params.get('host', 'localhost')}")
        print(f"✓ Puerto: {db.connect_params.get('port', 5432)}")
        print(f"✓ Usuario: {db.connect_params.get('user', 'postgres')}")
        
        # Cerrar la conexión
        db.close()
        return True
    except Exception as e:
        print(f"✗ Error al conectar con PostgreSQL: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Iniciando pruebas de conexión a bases de datos ===")
    test_sqlite()
    test_postgresql()
    print("\n=== Fin de las pruebas ===")