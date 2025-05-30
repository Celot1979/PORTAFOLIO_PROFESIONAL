from peewee import *
import os
from datetime import datetime
from PORTAFOLIO.database import db

class Repositorio(Model):
    titulo = CharField()
    enlace = CharField()
    imagen = CharField()
    
    # Directorio para almacenar las imágenes
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    
    class Meta:
        database = db

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs).save()

    @classmethod
    def delete_by_id(cls, id):
        # Eliminar la imagen asociada si existe
        repo = cls.get_by_id(id)
        if repo and repo.imagen:
            image_path = os.path.join(cls.UPLOAD_FOLDER, os.path.basename(repo.imagen))
            if os.path.exists(image_path):
                os.remove(image_path)
        cls.delete().where(cls.id == id).execute()

    @staticmethod
    def save_image(image_data):
        """Guarda la imagen en el servidor.
        
        Args:
            image_data: Los datos binarios de la imagen.
            
        Returns:
            str: La ruta relativa de la imagen guardada.
        """
        # Crear el directorio de uploads si no existe
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        try:
            print(f"Tipo de datos de imagen: {type(image_data)}")
            
            # Asegurarse de que tenemos bytes
            if isinstance(image_data, str):
                image_data = image_data.encode()
            elif isinstance(image_data, dict):
                if "content" in image_data:
                    image_data = image_data["content"]
                elif "body" in image_data:
                    image_data = image_data["body"]
                elif "file" in image_data:
                    image_data = image_data["file"]
                else:
                    raise ValueError("No se encontró el contenido en el diccionario")
            
            if not isinstance(image_data, bytes):
                print(f"Estructura de los datos: {image_data}")
                raise ValueError("Los datos de la imagen deben ser bytes o string")

            # Generar un nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_image.jpg"
            file_path = os.path.join(upload_folder, filename)

            # Guardar la imagen
            with open(file_path, "wb") as f:
                f.write(image_data)

            # Retornar la ruta relativa para almacenar en la base de datos
            return f"/static/uploads/{filename}"

        except Exception as e:
            print(f"Error al guardar la imagen: {str(e)}")
            raise ValueError(f"Error al guardar la imagen: {str(e)}")

    @staticmethod
    def delete_by_id(repo_id):
        try:
            repo = Repositorio.get_by_id(repo_id)
            # Eliminar la imagen si existe
            if repo.imagen:
                image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), repo.imagen.lstrip("/"))
                if os.path.exists(image_path):
                    os.remove(image_path)
            repo.delete_instance()
            return True
        except Repositorio.DoesNotExist:
            return False 