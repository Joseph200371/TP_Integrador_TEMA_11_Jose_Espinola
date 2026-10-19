# ====================================================================
# MÓDULO: PERSISTENCIA.PY
# Propósito: Gestionar el almacenamiento y recuperación de los datos
# del calendario en archivos locales (JSON y CSV) para que la 
# información persista aunque se cierre la aplicación.
# ====================================================================
import json
import csv
import os

from utils.utilidades import pausa, mostrar_encabezado
from validaciones import verificar_registros_existentes

# Obtenemos la ruta absoluta de la carpeta 'src' donde está este archivo
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel para llegar a 'proyecto_integrador' y entramos a 'data'
CARPETA_DATOS = os.path.join(os.path.dirname(DIRECTORIO_ACTUAL), "data")

# Verificamos y creamos la carpeta 'data' si no existe físicamente
if not os.path.exists(CARPETA_DATOS):
    os.makedirs(CARPETA_DATOS)

# Rutas absolutas y seguras para los archivos
ARCHIVO_JSON = os.path.join(CARPETA_DATOS, "calendario_eventos.json")
ARCHIVO_CSV = os.path.join(CARPETA_DATOS, "calendario_eventos.csv")

# ==============================================================
# --- CARGA Y GUARDADO GENERAL (INICIO Y FIN APP) ---
# ==============================================================
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
    except (json.JSONDecodeError, Exception) as e:
        # Si el archivo está corrupto o malformado, evitamos que la app rompa retornando lista vacía
        print(f"[❌ ERROR]: No se pudieron cargar los datos iniciales: {e}")
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
    
    # --- 1. Guardado en formato JSON ---
    try:
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            # json.dump escribe la lista 'registros' en el archivo destino
            # indent=4: Ordena visualmente el archivo con 4 espacios de sangría
            # ensure_ascii=False: Permite guardar caracteres especiales como ñ y tildes correctamente
            json.dump(registros, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[❌ ERROR]: No se pudo guardar el archivo JSON: {e}")
    
    # --- 2. Guardado en formato CSV ---
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

# ==============================================================
# --- OPERACIONES MANUALES PARA EL SUBMENÚ (OPCIÓN 2) ---
# ==============================================================
# --- 1. GUARDAR JSON MANUAL (Opción 1 del submenú) ---
def guardar_json_manual(registros):
    """Opción 1 del submenú: Guardar manualmente solo en JSON."""
    mostrar_encabezado("--- GUARDAR DATOS EN FORMATO JSON ---", limpiar=True)
    # Verificamos si hay registros antes de intentar guardar
    if not verificar_registros_existentes(registros):
        return True

    try:
        # Abrimos el archivo en modo escritura ('w') con soporte UTF-8 para tildes y eñes
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            # json.dump serializa la lista de diccionarios con indentación de 4 espacios
            json.dump(registros, archivo, indent=4, ensure_ascii=False)
        print(f"[✅ ÉXITO]: Datos guardados manualmente en '{ARCHIVO_JSON}'.")       
    except Exception as e:
        # Capturamos cualquier imprevisto técnico al intentar escribir el archivo
        print(f"[❌ ERROR]: No se pudo guardar el archivo JSON: {e}")

    pausa()
    return True

# ==============================================================
# --- 2. CARGAR JSON MANUAL (Opción 2 del submenú) ---
def cargar_json_manual(registros):
    """Opción 2 del submenú: Cargar manualmente desde JSON."""
    mostrar_encabezado("--- CARGAR DATOS DESDE JSON ---", limpiar=True)
    # Validamos primero que el archivo físico realmente exista en el disco
    if not os.path.exists(ARCHIVO_JSON):
        print(f"[❌ ERROR]: No se encontró el archivo '{ARCHIVO_JSON}' para cargar datos.")
        return True

    try:
        # Abrimos el archivo JSON en modo lectura ('r')
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)        
            
            registros.clear()  # Limpiamos la lista actual en memoria antes de inyectar los nuevos datos
            registros.extend(datos) # Extendemos la lista con los elementos recuperados del archivo

        print(f"[✅ ÉXITO]: Datos cargados manualmente desde '{ARCHIVO_JSON}'. (Total: {len(registros)} registros).")
        
    except (json.JSONDecodeError, Exception) as e:
        # Capturamos errores si el archivo JSON está corrupto, vacío o malformado
        print(f"[❌ ERROR]: No se pudo cargar el archivo JSON: {e}")

    pausa()
    return True

# ==============================================================
# --- 3. GUARDAR CSV MANUAL (Opción 3 del submenú) ---
def guardar_csv_manual(registros):
    """Opción 3 del submenú: Guardar manualmente solo en CSV."""
    mostrar_encabezado("--- EXPORTAR DATOS A CSV ---", limpiar=True)
    if not verificar_registros_existentes(registros):
        return True

    try:
        campos = ["id", "fecha", "evento", "lugar", "notas"]
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=campos)     # DictWriter permite escribir diccionarios como filas en el CSV            writer.writeheader() # Escribe la primera línea con los nombres de las columnas
            for reg in registros:
                writer.writerow(reg) # Writerow escribe cada diccionario como una fila en el CSV
        print(f"[✅ ÉXITO]: Datos guardados manualmente en '{ARCHIVO_CSV}'.")
    except Exception as e:
        print(f"[❌ ERROR]: No se pudo guardar el archivo CSV: {e}")

    pausa()
    return True

# ==============================================================
# --- 4. CARGAR CSV MANUAL (Opción 4 del submenú) ---
def cargar_csv_manual(registros):
    """Opción 4 del submenú: Cargar manualmente desde CSV."""
    mostrar_encabezado("--- IMPORTAR DATOS DESDE CSV ---", limpiar=True)
    if not os.path.exists(ARCHIVO_CSV):
        print(f"[❌ ERROR]: No se encontró el archivo '{ARCHIVO_CSV}' para cargar datos.")
        return True

    try:
        with open(ARCHIVO_CSV, "r", newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)  # DictReader permite leer cada fila como un diccionario
            registros.clear()  # Limpiamos la lista actual antes de cargar nuevos datos
            for row in reader:
                # Convertimos los valores del CSV a los tipos de datos correctos
                registro = {
                    "id": int(row["id"]),
                    "fecha": row["fecha"],
                    "evento": row["evento"],
                    "lugar": row["lugar"],
                    "notas": row["notas"]
                }
                registros.append(registro)
        print(f"[✅ ÉXITO]: Datos cargados manualmente desde '{ARCHIVO_CSV}'.")
    except Exception as e:
        print(f"[❌ ERROR]: No se pudo cargar el archivo CSV: {e}")

    pausa()
    return True

# ==============================================================
# --- 5. GENERAR DATASET DE PRUEBA (opción 5 del submenú) ---
def generar_dataset(registros):
    """Genera automáticamente un conjunto de registros de prueba (10 elementos)."""
    mostrar_encabezado("--- GENERACIÓN AUTOMÁTICA DE DATASET ---", limpiar=True)

    # Verificamos si ya hay datos cargados para pedir confirmación
    if registros:
        print("[⚠️ ADVERTENCIA]: Ya existen registros cargados en el sistema.")
        confirmacion = input("¿Estás seguro de que deseas sobrescribirlos? 's' (sí) o 'n' (no): ").strip().lower()
        
        if confirmacion not in ('s','si'):
            print("[INFO]: Operación cancelada. Se conservan los datos anteriores.")
            pausa()
            return True
    
    dataset_prueba = [
        {"id": 1, "fecha": "10/11/2026", "evento": "Reunión de Equipo", "lugar": "Sala A", "notas": "Revisión de avances"},
        {"id": 2, "fecha": "12/11/2026", "evento": "Entrega de Proyecto", "lugar": "Facultad", "notas": "Defensa final"},
        {"id": 3, "fecha": "15/11/2026", "evento": "Examen de Redes", "lugar": "Aula Magna", "notas": "Estudiar capa de red"},
        {"id": 4, "fecha": "18/11/2026", "evento": "Consulta Médica", "lugar": "Clinica Central", "notas": "Control anual"},
        {"id": 5, "fecha": "20/11/2026", "evento": "Clase de Inglés", "lugar": "Virtual", "notas": "Practicar speaking"},
        {"id": 6, "fecha": "22/11/2026", "evento": "Mantenimiento PC", "lugar": "Casa", "notas": "Limpieza y cambio de pasta térmica"},
        {"id": 7, "fecha": "25/11/2026", "evento": "Festejo de Cumpleaños", "lugar": "Restaurante", "notas": "Comprar regalo"},
        {"id": 8, "fecha": "28/11/2026", "evento": "Sincronización Git", "lugar": "GitHub", "notas": "Actualizar ramas feature"},
        {"id": 9, "fecha": "02/12/2026", "evento": "Práctica de Laboratorio", "lugar": "Lab 2", "notas": "Montaje con transistores"},
        {"id": 10, "fecha": "05/12/2026", "evento": "Cierre de Actas", "lugar": "Secretaría", "notas": "Verificar calificaciones"}
    ]

    registros.clear()
    registros.extend(dataset_prueba)
    # Intentamos sincronizar en disco
    try:
        guardar_datos(registros)
        print("[✅ ÉXITO]: Se ha generado y cargado un dataset de prueba con 10 registros exitosamente.")
    except Exception as e:
        print(f"[❌ ERROR]: No se pudo guardar el dataset en el disco: {e}")

    pausa()
    return True