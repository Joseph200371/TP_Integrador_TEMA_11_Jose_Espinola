# =========================================================
# MÓDULO: MAIN.PY
# Punto de entrada y orquestador del menú principal
# =========================================================

from utils.utilidades import pausa, mostrar_encabezado, imprimir_info, ANCHO
# Importamos las funciones del módulo de lógica de negocio
from logica_negocio import (
    crear_registro,
    actualizar_registro,
    listar_registros,
    buscar_registro,
    eliminar_registro)
# AQUÍ IMPORTAMOS LAS FUNCIONES DE PERSISTENCIA
from persistencia import (
    cargar_datos,
    guardar_json_manual,
    cargar_json_manual,
    guardar_csv_manual,
    cargar_csv_manual,
    generar_dataset
    )

# from graficos import grafico_histograma, grafico_barras, grafico_boxplot, grafico_torta, panel_subplots

def imprimir_menu_principal():
    """Mostrar el menú principal por pantalla."""
    mostrar_encabezado("--- MENU PROYECTO: CALENDARIO DE EVENTOS ---", limpiar=True)
    print("1. Gestión del Sistema (Crear, Actualizar, Listar, Buscar, Eliminar)")
    print("2. Gestión de Datos y Dataset (JSON, CSV y Dataset automático)")
    print("3. Visualizaciones Gráficas (Histograma, Barras, Boxplot, Torta, Panel 2x2)")
    print("-" * ANCHO)
    print("4. Salir del Sistema")
    print("=" * ANCHO + "\n")

# ===========================================================
# FUNCIONES ENRUTADORAS - CRUD (Sub_menu conectado al menú)
# ===========================================================
def fn_sub_gestion_sistema(registros):
    """Submenú de Gestión del Sistema (Opciones CRUD)"""
    sub_ejecutando = True

    while sub_ejecutando:
        # Usamos limpiar=True solo una vez aquí al inicio del ciclo
        mostrar_encabezado("--- SUBMENÚ: GESTIÓN DEL SISTEMA ---", limpiar=True)
        imprimir_info("[INFO]: Aquí desplegaremos el submenú de Crear, Actualizar, Listar, Buscar y Eliminar registros.")
        print(" 1. Crear Registro")
        print(" 2. Actualizar Registro")
        print(" 3. Listar Registros")
        print(" 4. Buscar un Registro")
        print(" 5. Eliminar un Registro")
        print(" 6. Volver al Menú Principal")
        print("=" * ANCHO + "\n")

        try:
            opcion_sub = int(input("Selecciones una opción (1-6): ").strip())
        except ValueError:
            print("[❌ ERROR]: Debe ingresar un número entero válido.")
            pausa()
            continue
        
        # Diccionario interno para el submenú usando lambdas para pasar 'registros'
        acciones_sub = {
            1: lambda: fn_sub_crear(registros),
            2: lambda: fn_sub_actualizar(registros),
            3: lambda: fn_sub_listar(registros),
            4: lambda: fn_sub_buscar(registros),
            5: lambda: fn_sub_eliminar(registros),
            6: lambda: False  # Rompe el bucle del submenú y vuelve al principal
        }
        
        accion = acciones_sub.get(opcion_sub, fn_opcion_invalida)
        sub_ejecutando = accion()
        
    return True # Mantiene vivo el menú principal

# Llamamos a las funciones reales que creamos en logica_negocio.py
def fn_sub_crear(registros):
    crear_registro(registros)
    return True

def fn_sub_actualizar(registros):
    actualizar_registro(registros)
    return True 

def fn_sub_buscar(registros):
    buscar_registro(registros)
    return True

def fn_sub_eliminar(registros):
    eliminar_registro(registros)
    return True

def fn_sub_listar(registros):
    listar_registros(registros)
    return True

# ===========================================================
# FUNCIONES ENRUTADORAS - DATOS (Sub_menu conectado al menú)
# ===========================================================
def fn_sub_gestion_dato(registros):
    """Submenú de Gestión de Datos y Dataset (JSON, CSV y Dataset)"""
    sub_ejecutando = True

    while sub_ejecutando:
        # Usamos limpiar=True solo una vez aquí al inicio del ciclo
        mostrar_encabezado("--- SUBMENÚ: GESTIÓN DE DATOS Y DATASET ---", limpiar=True)
        imprimir_info("[INFO]: Aquí desplegaremos el submenú de JSON, CSV y Dataset automático.")
        print(" 1. Guardar Datos en JSON")
        print(" 2. Cargar Datos desde JSON")
        print(" 3. Guardar Datos en CSV")
        print(" 4. Cargar Datos desde CSV")
        print(" 5. Generación Automática de Dataset (Registros de prueba)")
        print(" 6. Volver al Menú Principal")
        print("=" * ANCHO + "\n")

        try:
            opcion_sub = int(input("Seleccione una opción (1-6): ").strip())
        except ValueError:
            print("[❌ ERROR]: Debe ingresar un número entero válido.")
            pausa()
            continue
        
        # Diccionario interno para el submenú usando lambdas para pasar 'registros'
        acciones_sub = {
            1: lambda: fn_guardar_json(registros),
            2: lambda: fn_cargar_json(registros),
            3: lambda: fn_guardar_csv(registros),
            4: lambda: fn_cargar_csv(registros),
            5: lambda: fn_generar_dataset(registros),
            6: lambda: False  # Rompe el bucle del submenú y vuelve al principal
        }
        
        accion = acciones_sub.get(opcion_sub, fn_opcion_invalida)
        sub_ejecutando = accion()
        
    return True # Mantiene vivo el menú principal

def fn_guardar_json(registros):
    guardar_json_manual(registros)
    return True

def fn_cargar_json(registros):
    cargar_json_manual(registros)
    return True

def fn_guardar_csv(registros):
    guardar_csv_manual(registros)
    return True

def fn_cargar_csv(registros):
    cargar_csv_manual(registros)
    return True

def fn_generar_dataset(registros):
    generar_dataset(registros)
    return True

# =========================================================
# FUNCIONES PARA LEER Y EJECUTAR LAS OPCIONES DEL MENÚ
# =========================================================
def leer_opcion_user():
    """"Lee la opción ingresada por el usuario y la devuelve como entero."""
    try:
        opcion = input("Ingrese el número de la opción deseada (1-4): ").strip()
        return int(opcion)
    except ValueError:
        print("[❌ ERROR]: La opción ingresada no es un número válido. Por favor, intente nuevamente.")
        pausa()
        return None  # Retorna None si la conversión falla

def ejecutar_opcion():
    """Ejecuta la opción seleccionada por el usuario en un bucle hasta que decida salir."""
    # 1. Cargamos los datos iniciales desde el disco (JSON/CSV) al arrancar el programa
    registros = cargar_datos()

    # 2. Definimos el diccionario de acciones conectando 'registros' a la opción 1
    # DICCIONARIO DE ACCIONES 
    MENU_ACCIONES = {
        1: lambda: fn_opcion_1(registros),  # Submenú CRUD (Gestión del Sistema)
        2: lambda: fn_opcion_2(registros),  # Submenú Datos (JSON, CSV, Dataset)
        3: lambda: fn_opcion_3(registros),  # Submenú Gráficos (Visualizaciones)
        4: lambda: fn_opcion_4()            # Salir del sistema
    }

    ejecutando = True
    while ejecutando:
        imprimir_menu_principal()
        opcion_elegida = leer_opcion_user()

        # Validar que no haya retornado None por error de tipeo
        if opcion_elegida is not None:
            accion_a_ejecutar = MENU_ACCIONES.get(opcion_elegida, fn_opcion_invalida)
            ejecutando = accion_a_ejecutar()
        else:
            ejecutando = True

# =========================================================
# FUNCIONES ENRUTADORAS (Conectan el menú con la lógica)
# =========================================================
def fn_opcion_1(registros):
    """Menú de gestión del sistema (Opciones 1 al 5 originales - Opciones CRUD)"""
    return fn_sub_gestion_sistema(registros)

def fn_opcion_2(registros):
    """Gestión de Datos y Dataset (Opciones 6 al 10 originales)"""
    return fn_sub_gestion_dato(registros)

def fn_opcion_3(res):
    """Visualizaciones Gráficas (Opciones 11 al 15 originales)"""
    mostrar_encabezado("Visualizaciones Gráficas")
    imprimir_info("[INFO]: Aquí desplegaremos el submenú de gráficos de Matplotlib y Panel 2x2.")
    pausa()
    return True

def fn_opcion_4():
    """Salir del sistema"""
    mostrar_encabezado("Saliendo del Sistema")
    imprimir_info("¡Gracias por utilizar el Calendario de Eventos! Programa finalizado correctamente.\n")
    pausa()
    return False  # Indica que se debe salir del bucle principal y terminar el programa

def fn_opcion_invalida():
    mostrar_encabezado("Opción Inválida")
    print("[❌ ERROR]: Opción fuera de rango.")
    pausa()
    return True

# =============================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =============================================
# Sirve como punto de entrada del programa y ejecuta el menú principal
if __name__ == "__main__":
    ejecutar_opcion() # Variable de control