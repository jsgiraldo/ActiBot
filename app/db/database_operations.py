# app/db/database.py
# ActiBot/app/db/database_operations.py
import sqlite3
from typing import Dict, Optional, List, Any
from app.config import settings # Importar settings para la URL de la BD
import os


DATABASE_URL = settings.DATABASE_URL.split("sqlite:///./")[1] # Extraer solo el nombre del archivo

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_recreate: bool = False):
    if os.path.exists(DATABASE_URL) and force_recreate:
        print(f"Forzando recreación de la base de datos: {DATABASE_URL}")
        os.remove(DATABASE_URL)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proyectos (
                numero_proyecto TEXT PRIMARY KEY,
                nombre_cliente TEXT,
                etapa_actual TEXT NOT NULL CHECK(etapa_actual IN ('Diseño', 'Factibilidad', 'Recibo de obra')),
                pdf_path TEXT NOT NULL
            )
        ''')
        conn.commit()
        print(f"Tabla 'proyectos' en '{DATABASE_URL}' verificada/creada.")

        # Añadir datos de ejemplo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM proyectos")
        if cursor.fetchone()[0] == 0:
            print("Tabla vacía, añadiendo datos de ejemplo...")
            sample_data = [
                ('PROY001', 'Constructora A', 'Diseño', 'docs/PROY001_diseno.pdf'),
                ('PROY002', 'Constructora B', 'Factibilidad', 'docs/PROY002_factibilidad.pdf'),
                ('PROY003', 'Constructora C', 'Recibo de obra', 'docs/PROY003_recibo.pdf'),
            ]
            cursor.executemany(
                'INSERT INTO proyectos (numero_proyecto, nombre_cliente, etapa_actual, pdf_path) VALUES (?, ?, ?, ?)',
                sample_data
            )
            conn.commit()
            print(f"{len(sample_data)} proyectos de ejemplo añadidos.")
    except sqlite3.Error as e:
        print(f"Error de SQLite durante init_db: {e}")
    finally:
        conn.close()

def get_project_by_number(project_number: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proyectos WHERE numero_proyecto = ?', (project_number,))
    project_row = cursor.fetchone()
    conn.close()
    if project_row:
        return dict(project_row)
    return None

# Para probar directamente este módulo:
if __name__ == "__main__":
    print(f"Usando base de datos: {DATABASE_URL}")
    init_db(force_recreate=True) # Cambia a False después de la primera ejecución si no quieres recrear
    print("\nProyectos existentes:")
    conn_test = get_db_connection()
    for row in conn_test.execute("SELECT * FROM proyectos"):
        print(dict(row))
    conn_test.close()

    print(f"\nBuscando PROY001: {get_project_by_number('PROY001')}")
    print(f"Buscando PROY999: {get_project_by_number('PROY999')}")