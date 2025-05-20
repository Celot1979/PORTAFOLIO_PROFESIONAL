from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al directorio BBDD
db_dir = os.path.join(current_dir, "BBDD")
# Asegurarse de que el directorio existe
os.makedirs(db_dir, exist_ok=True)
# Construir la ruta completa a la base de datos
db_path = os.path.join(db_dir, "blog.db")

# Configura la conexión a la base de datos SQLite
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=True)

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 