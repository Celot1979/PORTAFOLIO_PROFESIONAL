import unittest
import sys
import os

# Añadir el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar las pruebas
from tests.test_repositorio import TestRepositorio

if __name__ == '__main__':
    # Crear el suite de pruebas
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestRepositorio)
    
    # Ejecutar las pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Salir con código de error si hay fallos
    sys.exit(not result.wasSuccessful()) 