# =========================================================
# MÓDULO: MAIN.PY
# Punto de entrada y orquestador del menú principal
# =========================================================

from utils.utilidades import limpiar_pantalla, pausa, mostrar_encabezado, imprimir_info, ANCHO

# Importaremos las funciones reales de los otros módulos
# from logica_negocio import crear_registro, actualizar_registro, ver_listado, buscar_registro, eliminar_registro
# from persistencia import guardar_json, cargar_json, guardar_csv, cargar_csv, generar_dataset
# from graficos import grafico_histograma, grafico_barras, grafico_boxplot, grafico_torta, panel_subplots

# =========================================================
# FUNCIONES ENRUTADORAS (Conectan el menú con la lógica)
# =========================================================
def fn_opcion_1():
    """Menú de gestión del sistema (Opciones 1 al 5 originales)"""
    mostrar_encabezado("Gestión del Sistema")
    imprimir_info("[INFO]: Aquí desplegaremos el submenú de Creación, Actualización, Listado, Búsqueda y Eliminación.")
    pausa()
    return fn_sub_gestion_sistema()

def fn_opcion_2():
    """Gestión de Datos y Dataset (Opciones 6 al 10 originales)"""
    mostrar_encabezado("Gestión de Datos y Dataset")
    imprimir_info("[INFO]: Aquí desplegaremos el submenú de JSON, CSV y Dataset automático.")
    pausa()
    return True

def fn_opcion_3():
    """Visualizaciones Gráficas (Opciones 11 al 15 originales)"""
    mostrar_encabezado("Visualizaciones Gráficas")
    imprimir_info("[INFO]: Aquí desplegaremos el submenú de gráficos de Matplotlib y Panel 2x2.")
    pausa()
    return True

def fn_opcion_4():
    """Salir del sistema"""
    mostrar_encabezado("Saliendo del Sistema")
    print("¡Gracias por utilizar el Calendario de Eventos! Programa finalizado correctamente.\n")
    return False  # Este False rompe el bucle while principal

def fn_opcion_invalida():
    """Manejo de opción fuera de rango"""
    mostrar_encabezado("Opción Inválida")
    print("[❌ ERROR]: La opción ingresada no es válida. Por favor, seleccione un número entre 1 y 4.")
    pausa()
    return True


# ==========================
# DICCIONARIO DE ACCIONES 
# ==========================
MENU_ACCIONES = {
    1: fn_opcion_1,
    2: fn_opcion_2,
    3: fn_opcion_3,
    4: fn_opcion_4
}

def imprimir_menu_principal():
    """Mostrar el menú principal por pantalla."""
    mostrar_encabezado("--- MENU PROYECTO: CALENDARIO DE EVENTOS ---", limpiar=True)
    print("1. Gestión del Sistema (Crear, Actualizar, Listar, Buscar, Eliminar)")
    print("2. Gestión de Datos y Dataset (JSON, CSV y Dataset automático)")
    print("3. Visualizaciones Gráficas (Histograma, Barras, Boxplot, Torta, Panel 2x2)")
    print("-" * ANCHO)
    print("4. Salir del Sistema")
    print("=" * ANCHO + "\n")

# =========================================================
# FUNCIONES ENRUTADORAS (Sub_menu conectado al menú)
# =========================================================
def fn_sub_gestion_sistema():
    """Submenú de Gestión del Sistema (Opciones CRUD)"""
    sub_ejecutando = True

    while sub_ejecutando:# (o sub_ejecutando)
        # Usamos limpiar=True solo una vez aquí al inicio del ciclo
        mostrar_encabezado("--- SUBMENÚ: GESTIÓN DEL SISTEMA ---", limpiar=True)
        print(" 1. Crear Registro")
        print(" 2. Actualizar Registro")
        print(" 3. Ver Listado de Registros")
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

        # Diccionario interno para el submenú (¡Cero if/elif!)
        acciones_sub = {
            1: fn_sub_crear,
            2: fn_sub_actualizar,
            3: fn_sub_listar,
            4: fn_sub_buscar,
            5: fn_sub_eliminar,
            6: lambda: False  # Rompe el bucle del submenú y vuelve al principal
        }
        
        accion = acciones_sub.get(opcion_sub, fn_opcion_invalida_sub)
        sub_ejecutando = accion()
        
    return True # Mantiene vivo el menú principal

def fn_sub_crear():
    mostrar_encabezado("Crear Nuevo Registro")
    # Aquí llamaremos a: crear_registro(registros_en_memoria)
    imprimir_info("[INFO]: Aquí ejecutaremos la lógica para pedir los datos del evento.")
    pausa()
    return True

def fn_sub_actualizar():
    mostrar_encabezado("Actualizar Registro")
    # Aquí llamaremos a: actualizar_registro(registros_en_memoria)
    imprimir_info("[INFO]: Aquí ejecutaremos la lógica para actualizar los datos del evento.")
    pausa()
    return True 

def fn_sub_buscar():
    mostrar_encabezado("Buscar Registro")
    # Aquí llamaremos a: buscar_registro(registros_en_memoria)
    imprimir_info("[INFO]: Aquí ejecutaremos la lógica para buscar los datos del evento.")
    pausa()
    return True

def fn_sub_eliminar():
    mostrar_encabezado("Eliminar Registro")
    # Aquí llamaremos a: eliminar_registro(registros_en_memoria)
    imprimir_info("[INFO]: Aquí ejecutaremos la lógica para eliminar los datos del evento.")
    pausa()
    return True

def fn_sub_listar():
    mostrar_encabezado("Listado de Registros")
    # Aquí llamaremos a: ver_listado(registros_en_memoria)
    imprimir_info("[INFO]: Aquí mostraremos todos los registros guardados.")
    pausa()
    return True

def fn_opcion_invalida_sub():
    mostrar_encabezado("Opción Inválida")
    print("[❌ ERROR]: Opción fuera de rango en el submenú.")
    pausa()
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

if __name__ == "__main__":
    ejecutar_opcion() # Variable de control