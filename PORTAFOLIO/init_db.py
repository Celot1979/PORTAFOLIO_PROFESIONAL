from database import Base, engine
from models.repositorio import Repositorio

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.") 