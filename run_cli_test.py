# ActiBot/run_cli_test.py
import os
from app.core import chatbot_logic
from app.db import database_operations
from app.config import settings # Para asegurar que la config se carga

def main_cli_loop():
    print(f"--- Bienvenido a {settings.PROJECT_NAME} (CLI Test Mode) ---")
    print(f"Usando base de datos: {settings.DATABASE_URL.split('sqlite:///./')[1]}")
    print("Inicializando base de datos...")
    # Opcional: forzar recreación para pruebas limpias cada vez
    # database_operations.init_db(force_recreate=True)
    database_operations.init_db() # Normalmente no se fuerza la recreación
    print("------------------------------------------------------")
    print("Escriba su número de proyecto para comenzar o 'salir' para terminar.")

    user_id_cli = "terminal_user_main" # Un ID fijo para la sesión de terminal

    while True:
        try:
            user_input = input("Usted: ").strip()
            if user_input.lower() == 'salir':
                print("Saliendo del chatbot. ¡Hasta luego!")
                break

            if not user_input: # Si el usuario solo presiona Enter
                continue

            bot_response = chatbot_logic.process_user_message(user_id_cli, user_input)
            print(f"ActiBot: {bot_response}")
            print("------------------------------------------------------")

        except KeyboardInterrupt:
            print("\nSaliendo del chatbot (Ctrl+C detectado). ¡Hasta luego!")
            break
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            # Podrías querer romper el bucle aquí o continuar
            # break

if __name__ == "__main__":
    # Crear directorio 'docs' si no existe (para PDFs de ejemplo)
    if not os.path.exists('docs'):
        try:
            os.makedirs('docs')
            print("Directorio 'docs' creado para los archivos PDF simulados.")
            # Podrías incluso crear archivos PDF de ejemplo aquí si quieres
        except OSError as e:
            print(f"Error al crear directorio 'docs': {e}")

    main_cli_loop()