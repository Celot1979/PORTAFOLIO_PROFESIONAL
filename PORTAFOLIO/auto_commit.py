import time
import subprocess
import os
from datetime import datetime

def git_commit():
    try:
        # Agregar todos los cambios
        subprocess.run(['git', 'add', '.'])
        
        # Crear commit con timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto commit: {timestamp}"
        subprocess.run(['git', 'commit', '-m', commit_message])
        
        # Push al repositorio remoto
        subprocess.run(['git', 'push'])
        
        print(f"Commit automático realizado: {timestamp}")
    except Exception as e:
        print(f"Error al realizar commit automático: {str(e)}")

def main():
    print("Iniciando monitoreo de cambios...")
    while True:
        # Verificar si hay cambios
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        
        if result.stdout.strip():
            print("Cambios detectados, realizando commit...")
            git_commit()
        
        # Esperar 5 minutos antes de la siguiente verificación
        time.sleep(300)

if __name__ == "__main__":
    main() 