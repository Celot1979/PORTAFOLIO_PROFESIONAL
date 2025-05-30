import os
import unittest
from ..models.repositorio import Repositorio
from ..database import db

class TestRepositorio(unittest.TestCase):
    def setUp(self):
        # Configurar la base de datos de prueba
        db.connect()
        db.create_tables([Repositorio])
        
        # Crear un archivo de imagen de prueba
        self.test_image_path = os.path.join(Repositorio.UPLOAD_FOLDER, "test_image.jpg")
        os.makedirs(Repositorio.UPLOAD_FOLDER, exist_ok=True)
        with open(self.test_image_path, "w") as f:
            f.write("test image content")

    def tearDown(self):
        # Limpiar después de las pruebas
        Repositorio.delete().execute()
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        db.close()

    def test_create_repositorio(self):
        # Crear un repositorio de prueba
        repo = Repositorio.create(
            titulo="Test Repo",
            enlace="https://github.com/test",
            imagen="/static/uploads/test_image.jpg"
        )
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(repo.id)
        self.assertEqual(repo.titulo, "Test Repo")
        self.assertEqual(repo.enlace, "https://github.com/test")
        self.assertEqual(repo.imagen, "/static/uploads/test_image.jpg")

    def test_delete_repositorio(self):
        # Crear un repositorio
        repo = Repositorio.create(
            titulo="Test Repo",
            enlace="https://github.com/test",
            imagen="/static/uploads/test_image.jpg"
        )
        
        # Eliminar el repositorio
        Repositorio.delete_by_id(repo.id)
        
        # Verificar que se eliminó
        self.assertIsNone(Repositorio.get_or_none(id=repo.id))
        
        # Verificar que la imagen se eliminó
        self.assertFalse(os.path.exists(self.test_image_path))

    def test_save_image(self):
        # Simular un archivo de imagen
        class MockFile:
            def __init__(self):
                self.filename = "test_image.jpg"
            
            def save(self, path):
                with open(path, "w") as f:
                    f.write("test image content")

        # Guardar la imagen
        image_path = Repositorio.save_image(MockFile())
        
        # Verificar que la imagen se guardó
        self.assertTrue(os.path.exists(os.path.join(Repositorio.UPLOAD_FOLDER, "test_image.jpg")))
        self.assertEqual(image_path, "/static/uploads/test_image.jpg")

if __name__ == '__main__':
    unittest.main() 