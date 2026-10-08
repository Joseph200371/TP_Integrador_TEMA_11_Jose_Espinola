# ====================================================================
# MÓDULO: PERSISTENCIA.PY
# Propósito: Gestionar el almacenamiento y recuperación de los datos
# del calendario en archivos locales (JSON y CSV) para que la 
# información persista aunque se cierre la aplicación.
# ====================================================================

import json
import csv
import os

# Definimos los nombres de los archivos que actúan como nuestra base de datos local
ARCHIVO_JSON = "calendario.evento.json"
ARCHIVO_CSV = "calendario.evento.csv"

def cargar_datos():
    """
    Función para cargar los registros almacenados al iniciar el programa:

    - Utiliza 'os.path.exists' para verificar si el archivo JSON ya existe en el disco.
    - Si no existe (primera vez que corre la app), retorna una lista vacía para evitar errores.
    - Si existe, abre el archivo en modo lectura ('r') con codificación UTF-8 
      y usa 'json.load()' para transformar el texto JSON directamente en una 
      estructura nativa de Python (una lista de diccionarios).
    - Cuenta con manejo de excepciones ('try-except') por si el archivo llega a estar vacío o corrupto.
    """
    # Verificamos si el archivo de respaldo existe físicamente
    if not os.path.exists(ARCHIVO_JSON):
        return [] # Si no existe, empezamos con una lista en memoria vacía

    try:
        # Abrimos el archivo en modo lectura ('r') con codificación UTF-8 para soportar tildes
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            # json.load() deserializa el contenido del archivo transformándolo en objetos de Python
            return json.load(archivo)
    except (json.JSONDecodeError, Exception):
        # Si el archivo está corrupto o malformado, evitamos que la app rompa retornando lista vacía
        return []

def guardar_datos(registros):
    """
    Función para guardar y sincronizar los registros actuales en el disco duro.
    Se ejecuta automáticamente cada vez que se crea, modifica o elimina un evento.
    
    
    1. Persistencia en JSON: Emplea 'json.dump()' para volcar la lista completa 
       de diccionarios al archivo, aplicando indentación de 4 espacios para legibilidad 
       humana y desactivando ASCII estricto ('ensure_ascii=False') para respetar acentos.
    2. Exportación a CSV: Emplea 'csv.DictWriter' para mapear la lista de diccionarios 
       en formato tabular (filas y columnas), escribiendo primero las cabeceras 
       y luego iterando cada registro como una fila.
    """
    # --- 1. Guardado en formato JSON (Estructura jerárquica principal) ---
    try:
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            # json.dump escribe la lista 'registros' en el archivo destino
            # indent=4: Ordena visualmente el archivo con 4 espacios de sangría
            # ensure_ascii=False: Permite guardar caracteres especiales como ñ y tildes correctamente
            json.dump(registros, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[❌ ERROR]: No se pudo guardar el archivo JSON: {e}")
    
    # --- 2. Guardado en formato CSV (Formato tabular compatible con Excel) ---
    try:
        # Definimos estrictamente las columnas que conformarán la tabla del CSV
        campos = ["id", "fecha", "evento", "lugar", "notas"]
        
        # Abrimos el archivo CSV en modo escritura ('w')
        # newline="" evita que se generen líneas en blanco adicionales entre filas en Windows
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            # DictWriter facilita escribir diccionarios de Python directamente como filas tabulares
            writer = csv.DictWriter(archivo, fieldnames=campos)
            
            # Escribe la primera línea del archivo con los nombres de las columnas (cabeceras)
            writer.writeheader()
            
            # Recorre cada diccionario de la lista y vuelca su contenido como una fila en el CSV
            for reg in registros:
                writer.writerow(reg)
    except Exception as e:
        print(f"[❌ ERROR]: No se pudo guardar el archivo CSV: {e}")