# ActiBot/app/core/chatbot_logic.py
from typing import Dict, Optional, Tuple
from app.db import database_operations as db

# Estado simple en memoria para simular sesiones de usuario para CLI
# Clave: user_id (para CLI será un ID fijo), Valor: info del proyecto autenticado
cli_sessions: Dict[str, Dict] = {}

def process_user_message(user_id: str, message: str) -> str:
    """
    Procesa el mensaje del usuario y devuelve la respuesta del chatbot.
    """
    global cli_sessions
    authenticated_project_info = cli_sessions.get(user_id)
    response_message = ""

    message_lower = message.strip().lower()

    if not authenticated_project_info:
        # --- Estado: No Autenticado ---
        # Asumimos que el mensaje es el número de proyecto
        project_data = db.get_project_by_number(message.strip().upper()) # Asegurar mayúsculas para el ID
        if project_data:
            cli_sessions[user_id] = project_data
            response_message = (
                f"¡Autenticación exitosa para el proyecto {project_data['numero_proyecto']}!\n"
                f"Cliente: {project_data['nombre_cliente']}\n"
                f"Etapa actual: {project_data['etapa_actual']}.\n"
                "Puedes preguntar por: 'estado', 'documento', o 'cerrar sesion'."
            )
        else:
            response_message = "Número de proyecto inválido o no encontrado. Por favor, intente de nuevo."
    else:
        # --- Estado: Autenticado ---
        project_num = authenticated_project_info['numero_proyecto']
        project_stage = authenticated_project_info['etapa_actual']
        pdf_path = authenticated_project_info['pdf_path']

        if message_lower == 'estado' or message_lower == 'etapa':
            response_message = f"El proyecto {project_num} se encuentra en la etapa: {project_stage}."
        elif message_lower == 'documento' or message_lower == 'pdf':
            response_message = f"El documento para la etapa '{project_stage}' es: {pdf_path}\n(En una app real, aquí se enviaría el archivo/enlace)."
        elif message_lower == 'cerrar sesion':
            del cli_sessions[user_id]
            response_message = "Sesión cerrada. Ingrese un número de proyecto para continuar."
        else:
            response_message = (
                f"Comando no reconocido. Proyecto {project_num} (Etapa: {project_stage}).\n"
                "Comandos disponibles: 'estado', 'documento', 'cerrar sesion'."
            )
    return response_message

# Para pruebas directas del módulo de lógica (menos común)
if __name__ == "__main__":
    # Simulación
    test_user_id = "cli_tester"
    print("Prueba de lógica del chatbot:")
    print(f"Respuesta a PROY001: {process_user_message(test_user_id, 'PROY001')}")
    if test_user_id in cli_sessions:
        print(f"Respuesta a 'estado': {process_user_message(test_user_id, 'estado')}")
        print(f"Respuesta a 'documento': {process_user_message(test_user_id, 'documento')}")
        print(f"Respuesta a 'cerrar sesion': {process_user_message(test_user_id, 'cerrar sesion')}")
    print(f"Respuesta a PROY999: {process_user_message(test_user_id, 'PROY999')}")