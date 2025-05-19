# ActiBot/app/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
# Busca el .env en el directorio padre (raíz del proyecto)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Advertencia: archivo .env no encontrado. Usando valores por defecto o variables de entorno del sistema.")

class Settings:
    PROJECT_NAME: str = "ActiBot"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./actibot_default.db")

    # Placeholder para futuras configuraciones de API
    META_VERIFY_TOKEN: str | None = os.getenv("META_VERIFY_TOKEN")
    META_ACCESS_TOKEN: str | None = os.getenv("META_ACCESS_TOKEN")
    # ... más configuraciones según sea necesario

settings = Settings()

# Para pruebas rápidas, puedes imprimir las configuraciones cargadas
if __name__ == "__main__":
    print(f"Nombre del Proyecto: {settings.PROJECT_NAME}")
    print(f"URL de la Base de Datos: {settings.DATABASE_URL}")
    print(f"Token de Verificación de Meta (ejemplo): {settings.META_VERIFY_TOKEN}")