import sqlite3
import os

db_path = "/Users/danielgil/Documents/REFLEX/RUN/blog.db"

print(f"Intentando conectar a: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    print("Conexión exitosa a la base de datos.")
    conn.close()
except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos: {e}")

# Prueba de creación de carpeta y archivo si no existen
db_folder = os.path.dirname(db_path)
if not os.path.exists(db_folder):
    print(f"La carpeta '{db_folder}' no existe. Intentando crearla...")
    try:
        os.makedirs(db_folder, exist_ok=True)
        print(f"Carpeta '{db_folder}' creada exitosamente.")
    except OSError as e:
        print(f"Error al crear la carpeta '{db_folder}': {e}")

if not os.path.exists(db_path):
    print(f"El archivo de base de datos '{db_path}' no existe. Intentando crearlo...")
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"Archivo de base de datos '{db_path}' creado exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear el archivo de base de datos '{db_path}': {e}")
else:
    print(f"El archivo de base de datos '{db_path}' ya existe.")

# Intento de conexión después de la creación/verificación
try:
    conn = sqlite3.connect(db_path)
    print("Segunda conexión exitosa a la base de datos.")
    conn.close()
except sqlite3.Error as e:
    print(f"Segundo error al conectar a la base de datos: {e}")