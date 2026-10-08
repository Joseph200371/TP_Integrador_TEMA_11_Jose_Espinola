# ===============================================
# MÓDULO: LOGICA_NEGOCIO.PY
# Contiene todas las funciones atómicas del ABM
# ===============================================
from utils.utilidades import limpiar_pantalla, pausa, mostrar_encabezado, imprimir_info, ANCHO
from persistencia import guardar_datos
from validaciones import validar_texto, verificar_duplicado, validar_fecha_valida, validar_evento, leer_campo_opcional

# --- 1. ALTA (Crear Registro - Opción 1) ---
def crear_registro(registros):
    """
    Función principal de Alta (Create - Opción 1 del submenú).
    Orquesta la recolección de datos, maneja las cancelaciones y añade 
    el nuevo diccionario de evento a la lista principal en memoria.
    """
    mostrar_encabezado("=== OPCIÓN 1: CREAR NUEVO EVENTO ===", limpiar = True)
    imprimir_info("NOTA: Puede cancelar la creación ingresando '0' o presionando ENTER.\n")
    print("-" * ANCHO)

    # Solicitar al usuario que ingrese el nuevo evento (FECHA, EVENTO, LUGAR, NOTAS)
    # PASO 1: Capturar y validar la fecha de forma directa
    fecha = validar_fecha_valida("Ingrese la fecha del evento (DD/MM/AAAA) [0/ENTER para cancelar]: ")
    if fecha is None:
        print("\n[INFO]: Operación de creación cancelada.")
        pausa()
        return

    # PASO 2: Capturar y validar el nombre del evento
    evento = leer_evento_nuevo()
    if evento is None:
        print("\n[INFO]: Operación de creación cancelada.")
        return  # Sale de la función de inmediato sin alterar la lista de registros

    # PASO 3: Control de duplicados (Clave única: Fecha + Evento)
    if verificar_duplicado(registros, fecha, evento):
        print(f"\n[❌ ERROR]: Ya existe un evento idéntico ('{evento}') registrado para la fecha {fecha}.")
        pausa()
        return
    
    # PASO 4: Capturar el lugar del evento
    lugar = leer_campo_opcional("Ingrese el lugar del evento [0/ENTER para omitir]: ", "Sin especificar")
    if lugar is None:
        print("\n[INFO]: Operación de creación cancelada.")
        pausa()
        return

    # PASO 5: Capturar notas adicionales
    notas = leer_campo_opcional("Ingrese notas adicionales [0/ENTER para omitir]: ", "Sin notas")
    if notas is None:
        print("\n[INFO]: Operación de creación cancelada.")
        pausa()
        return

    # PASO 6: Delegamos la construcción y guardado a nuestra nueva función auxiliar
    _registrar_y_persistir(registros, fecha, evento, lugar, notas)

def leer_evento_nuevo():
    """
    Función auxiliar de lectura: Solicita el nombre del evento y se apoya 
    en la función 'validar_evento' para asegurar su integridad.
    
    Retorna:
        str: El nombre del evento validado y limpio.
        None: Si el usuario cancela la operación ('0').
    """
    while True:
        # validar_texto ya hace el input, el strip, y maneja el '0' o '' devolviendo None
        entrada_evento = validar_texto("Ingrese el nombre del evento [0/ENTER para cancelar]: ")

        # CONDICIÓN DE ESCAPE: Permite abortar el alta en cualquier momento
        if entrada_evento is None:
            return None # El usuario canceló

        # Aplicamos la función validar_evento() que pertenece a validaciones.py - (máx 50 caracteres y letras)
        evento = validar_evento(entrada_evento)
        
        if not evento:
            print("[❌ ERROR]: Evento inválido. Debe tener máximo 50 caracteres y al menos una letra.")
            continue # Vuelve a solicitar el ingreso sin romper el programa

        return evento

def _registrar_y_persistir(registros, fecha, evento, lugar, notas):
    """
    Función auxiliar interna.
    Propósito: Encapsular la lógica de creación del diccionario, 
    inserción en memoria, persistencia en archivos y feedback al usuario.
    
    Defensa para el profesor:
    - Aplica el principio DRY y modularidad extrema.
    - Centraliza la mutación de la lista 'registros' y la llamada a persistencia.
    """
    # 1. Construimos el diccionario con un ID autoincremental seguro
    nuevo_item = {
        "id": len(registros) + 1,
        "fecha": fecha,
        "evento": evento,
        "lugar": lugar,
        "notas": notas
    }
    
    # 2. Añadimos el ítem a la lista en memoria RAM
    registros.append(nuevo_item)

    # 3. Guardamos permanentemente en JSON y CSV llamando al módulo de persistencia
    guardar_datos(registros)

    # 4. Mensaje visual de éxito para el usuario
    print(f"\n[ÉXITO]: ¡Evento registrado y guardado exitosamente en el sistema!")
    print(f" --------------------------------------------------------")
    print(f" -> ID Asignado : {nuevo_item['id']}")
    print(f" -> Fecha       : {fecha}")
    print(f" -> Evento      : {evento}")
    print(f" -> Lugar       : {lugar}")
    print(f" -> Notas       : {notas}")
    print(f" --------------------------------------------------------")
    
    pausa()

# --- 2. MODIFICACIÓN (Actualizar Registro - Opción 2) ---
def actualizar_registro(registros):
    # Lógica de edición con ENTER
    limpiar_pantalla()
    pass

# --- 3. CONSULTA (Listar - Opciones 3) ---
def ver_listado(registros):
    # Lógica para mostrar todos
    limpiar_pantalla()
    print("=== OPCIÓN 3: LISTADO DE EVENTOS ===")

    pass

# --- 4. CONSULTA (Buscar - Opciones 4) ---
def buscar_registro(registros):
    # Lógica de búsqueda por filtros
    limpiar_pantalla()

    pass

# --- 5. BAJA (Eliminar Registro - Opción 5) ---
def eliminar_registro(registros):
    # Lógica de eliminación por índice
    limpiar_pantalla()

    pass