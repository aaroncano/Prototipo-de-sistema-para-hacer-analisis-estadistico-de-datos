import os
import time
import django
from django.conf import settings

# Configuración de Django para utilizar las configuraciones de django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Después de 24 horas se eliminan los archivos temporales
FILE_AGE_THRESHOLD = 24 * 60 * 60  

def cleanup_old_files():
    now = time.time()
    temp_dir = settings.TEMP_FILES_DIR

    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        file_age = now - os.path.getmtime(file_path)

        if file_age > FILE_AGE_THRESHOLD:
            os.remove(file_path)
            print(f"Eliminado: {file_path}")

if __name__ == "__main__":
    cleanup_old_files()