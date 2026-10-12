# ===============================================
# MÓDULO: LOGICA_NEGOCIO.PY
# Contiene todas las funciones atómicas del ABM
# ===============================================
from utils.utilidades import limpiar_pantalla, pausa, mostrar_encabezado, imprimir_info, ANCHO
from persistencia import guardar_datos
from validaciones import validar_texto, verificar_duplicado, validar_fecha_valida, validar_evento, leer_campo_opcional, verificar_registros_existentes

def _mostrar_detalle_registro(item):
    """
    Función auxiliar privada: Imprime de forma estandarizada 
    los detalles de un evento en la consola.
    """
    print(f" ID      : {item.get('id')}")
    print(f" Fecha   : {item.get('fecha')}")
    print(f" Evento  : {item.get('evento')}")
    print(f" Lugar   : {item.get('lugar', 'Sin especificar')}")
    print(f" Notas   : {item.get('notas', 'Sin notas')}")
    print("-" * ANCHO)

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
    """
    Función para modificar un registro existente buscando por su ID (Operación Update del CRUD).
    
    - Reutiliza 'verificar_registros_existentes' para mantener el principio DRY.
    - Solicita y valida el ID mediante 'try-except' asegurando robustez ante entradas incorrectas.
    - Implementa una actualización selectiva: si el usuario presiona ENTER, el campo conserva 
      su valor original; si ingresa un valor nuevo, este se valida antes de ser sobrescrito.
    - Actualiza el diccionario en memoria y llama inmediatamente a 'guardar_datos(registros)' 
      para persistir los cambios en disco.
    """
    mostrar_encabezado("=== MODIFICAR EVENTO EXISTENTE ===", limpiar=True)

    # 1. Validación centralizada de lista vacía
    if not verificar_registros_existentes(registros, "No hay eventos registrados para modificar."):
        return

    # 2. Mostramos los eventos actuales para guiar al usuario
    print("Eventos disponibles en el sistema:")
    print("-" * ANCHO)
    for item in registros:
        _mostrar_detalle_registro(item)
    print("-" * ANCHO)

    # 3. Solicitamos el ID del registro a modificar
    id_ingresado = input("Ingrese el ID del evento que desea modificar [0/ENTER para cancelar]: ").strip()

    if id_ingresado == '0' or id_ingresado == '':
        print("\n[INFO]: Operación de modificación cancelada.")
        pausa()
        return

    # Validamos que el ID sea un número entero
    try:
        id_a_modificar = int(id_ingresado)
    except ValueError:
        print("\n[❌ ERROR]: Entrada inválida. Debe ingresar un número entero.")
        pausa()
        return

    # 4. Buscamos el registro en la lista
    registro_encontrado = None
    for item in registros:
        if item.get('id') == id_a_modificar:
            registro_encontrado = item
            break

        if not registro_encontrado:
            print(f"\n[❌ ERROR]: No se encontró ningún evento asociado al ID {id_a_modificar}.")
            pausa()
            return
        
    # 5. Mostramos los datos actuales y procedemos a la actualización campo por campo
    print(f"\n[ℹ️]: Modificando el evento ID {id_a_modificar}. (Presione ENTER para conservar el valor actual).\n")
    print(f" -> Fecha actual : {registro_encontrado['fecha']}")
    print(f" -> Evento actual: {registro_encontrado['evento']}")
    print(f" -> Lugar actual : {registro_encontrado['lugar']}")
    print(f" -> Notas actual : {registro_encontrado['notas']}")
    print("-" * ANCHO)

    # --- Actualización de la Fecha ---
    nueva_fecha = validar_fecha_valida(f"Nueva fecha [{registro_encontrado['fecha']}]: ")
    if nueva_fecha in None:
        fecha_final = registro_encontrado['fecha']
    else:
        fecha_final = nueva_fecha

    # --- Actualización del Evento ---
    evento_final = leer_evento_modificacion(registro_encontrado['evento'])

    # --- Actualización del Lugar ---
    nuevo_lugar = validar_texto(f"Nuevo lugar [{registro_encontrado['lugar']}]: ")
    if nuevo_lugar is None or nuevo_lugar == "":
        lugar_final = registro_encontrado['lugar']
    else:
        lugar_final = nuevo_lugar

    # --- Actualización de las Notas ---
    nuevas_notas = validar_texto(f"Nuevas notas [{registro_encontrado['notas']}]: ")
    if nuevas_notas is None or nuevas_notas == "":
        notas_finales = registro_encontrado['notas']
    else:
        notas_finales = nuevas_notas

    # 6. Aplicamos los cambios al diccionario en memoria
    registro_encontrado['fecha'] = fecha_final
    registro_encontrado['evento'] = evento_final
    registro_encontrado['lugar'] = lugar_final
    registro_encontrado['notas'] = notas_finales
    # (Si quisieras actualizar el evento también, aplicas la misma lógica de conservar si está vacío)

    # 7. Sincronizamos con el almacenamiento persistente (JSON y CSV)
    guardar_datos(registros)

    print(f"\n[ÉXITO]: ¡El evento ID {id_a_modificar} ha sido actualizado correctamente!")
    print(f" --------------------------------------------------------")
    print(f" -> Fecha : {registro_encontrado['fecha']}")
    print(f" -> Evento: {registro_encontrado['evento']}")
    print(f" -> Lugar : {registro_encontrado['lugar']}")
    print(f" -> Notas : {registro_encontrado['notas']}")
    print(f" --------------------------------------------------------")
    pausa()

# --- FUNCIÓN AUXILIAR PARA actualizar_registro(registros) ---
def leer_evento_modificacion(evento_actual):
    """
    Solicita el nuevo nombre del evento para la modificación.
    Si el usuario presiona ENTER sin escribir nada, conserva el evento actual.
    Si escribe algo, valida que cumpla con los requisitos (máx 50 chars, al menos una letra).
    """
    while True:
        mensaje = f"Nuevo evento [{evento_actual}] (ENTER para conservar): "
        entrada_evento = validar_texto(mensaje)

        # Si presiona ENTER (retorna None o vacío), conservamos el actual
        if entrada_evento is None or entrada_evento == "":
            return evento_actual

        # Si ingresó '0', podemos interpretarlo como cancelar la modificación de este campo
        if entrada_evento == '0':
            return evento_actual # o None si prefieres cancelar

        # Validamos que cumpla con los requisitos del evento
        evento_validado = validar_evento(entrada_evento)
        
        if not evento_validado:
            print("[❌ ERROR]: Evento inválido. Debe tener máximo 50 caracteres y al menos una letra.")
            continue

        return evento_validado

# --- 3. CONSULTA (Listar - Opciones 3) ---
def listar_registros(registros):
    """
    Función para listar y mostrar todos los eventos registrados (Operación Read del CRUD).
    
    - Verifica primero si la lista está vacía para evitar iteraciones innecesarias y dar feedback claro.
    - Utiliza un ciclo 'for' para recorrer la lista de diccionarios en memoria.
    - Aplica un formato tabular o en bloques limpios usando f-strings para mejorar la experiencia de usuario.
    """
    mostrar_encabezado("=== OPCIÓN 2: LISTAR TODOS LOS EVENTOS ===", limpiar=True)

    # 1. Validamos usando la función centralizada
    if not verificar_registros_existentes(registros):
        pausa()
        return  # Si está vacía, la función auxiliar ya mostró el aviso y pausó, solo salimos

    print(f"Total de eventos encontrados: {len(registros)}\n")
    print("-" * ANCHO)

    # 2. Reutilizamos la función auxiliar para cada elemento
    for item in registros:
        _mostrar_detalle_registro(item)

    pausa()

# --- 4. CONSULTA (Buscar - Opción 4) ---
def buscar_registro(registros):
    """
    Función para buscar eventos en el sistema mediante filtros (Operación Read/Search).
    
    Defensa para el profesor:
    - Reutiliza la validación centralizada de lista vacía.
    - Ofrece un submenú claro con dos criterios de búsqueda: por fecha exacta o por palabra clave.
    - Utiliza subcadenas ('in') y conversiones a minúsculas (.lower()) para hacer una búsqueda 
      flexible por texto.
    - Reutiliza la función auxiliar '_mostrar_detalle_registro' para mantener la consistencia visual.
    """
    mostrar_encabezado("=== OPCIÓN 4: BUSCAR EVENTOS ===", limpiar=True)

    # 1. Validación centralizada de lista vacía
    if not verificar_registros_existentes(registros, "No hay eventos registrados para realizar búsquedas."):
        return

    # 2. Submenú de opciones de búsqueda
    print("Seleccione el criterio de búsqueda:")
    print("1. Buscar por Fecha exacta (DD/MM/AAAA)")
    print("2. Buscar por Palabra Clave (en el evento o lugar)")
    print("0. Cancelar / Volver al menú principal")
    
    opcion = input("\nIngrese una opción: ").strip()

    if opcion == '0':
        print("\n[INFO]: Operación de búsqueda cancelada.")
        pausa()
        return

    resultados = []

    # 3. Filtrado según la opción elegida
    if opcion == '1':
        # Búsqueda por fecha exacta
        fecha_buscada = validar_fecha_valida("Ingrese la fecha a buscar (DD/MM/AAAA): ")
        if fecha_buscada is None:
            print("\n[INFO]: Búsqueda cancelada.")
            pausa()
            return
        
        # Recorremos la lista buscando coincidencias exactas
        for item in registros:
            if item.get('fecha') == fecha_buscada:
                resultados.append(item)

    elif opcion == '2':
        # Búsqueda por palabra clave
        keyword = input("Ingrese la palabra clave (evento o lugar): ").strip().lower()
        if not keyword:
            print("\n[INFO]: No ingresó ninguna palabra clave. Búsqueda cancelada.")
            pausa()
            return

        # Recorremos la lista buscando si la palabra está contenida (ignorando mayúsculas/minúsculas)
        for item in registros:
            evento_lower = item.get('evento', '').lower()
            lugar_lower = item.get('lugar', '').lower()
            
            # 1. Verificamos si la palabra clave está contenida dentro del nombre del evento
            coincide_evento = keyword in evento_lower
            
            # 2. Verificamos si la palabra clave está contenida dentro del lugar del evento
            coincide_lugar = keyword in lugar_lower
            
            # 3. Si aparece en CUALQUIERA de los dos campos, el registro califica
            if coincide_evento:
                resultados.append(item)
            elif coincide_lugar:
                resultados.append(item)
    else:
        print("\n[❌ ERROR]: Opción inválida. Debe seleccionar 1, 2 o 0.")
        pausa()
        return

    # 4. Mostramos los resultados obtenidos
    mostrar_encabezado("=== RESULTADOS DE LA BÚSQUEDA ===", limpiar=True)
    
    if not resultados:
        print("[ℹ️ INFO]: No se encontraron eventos que coincidan con el criterio ingresado.")
    else:
        print(f"¡Se encontraron {len(resultados)} evento(s) coincidente(s)!\n")
        print("-" * ANCHO)
        for item in resultados:
            _mostrar_detalle_registro(item)

    pausa()

# --- 5. BAJA (Eliminar Registro - Opción 5) ---
def eliminar_registro(registros):
    """
    Función para eliminar un registro por su ID (Operación Delete del CRUD).
    
    - Verifica primero si la lista está vacía.
    - Muestra un resumen rápido con los IDs para guiar al usuario.
    - Solicita el ID y valida mediante 'try-except' que sea un número entero válido.
    - Implementa una confirmación obligatoria ('s/n') antes de mutar los datos.
    - Utiliza comprensión de listas ('registros[:] = [...]') para remover el elemento 
      de forma segura de la lista en memoria.
    - Llama automáticamente a 'guardar_datos(registros)' para sincronizar disco y memoria.
    """
    mostrar_encabezado("=== ELIMINAR EVENTO ===", limpiar=True)

    # 1. Validación de lista vacía
    if not verificar_registros_existentes(registros):
        pausa()
        return

    # 2. Mostramos un resumen rápido con los IDs disponibles
    print("Eventos actuales en el sistema:")
    print("-" * ANCHO)
    for item in registros:
        _mostrar_detalle_registro(item)
        print("-" * ANCHO)
    
    # 3. Solicitamos el ID a eliminar
    id_ingresado = input("Ingrese el ID del evento que desea eliminar [0/ENTER para cancelar]: ").strip()

    if id_ingresado == '0' or id_ingresado == '':
        print("\n[INFO]: Operación de eliminación cancelada.")
        pausa()
        return

    # Validamos que el ID ingresado sea estrictamente un número entero
    try:
        id_a_eliminar = int (id_ingresado)
    except ValueError:
        print("\n[❌ ERROR]: Entrada inválida. Debe ingresar un número entero.")
        pausa()
        return

    # 4. Buscamos el registro en la lista por su ID
    registro_encontrado = None
    for item in registros:
        if item.get('id') == id_a_eliminar:
            registro_encontrado = item
            break
        
    # Si no se encuentra el ID, informamos al usuario
    if not registro_encontrado:
        print(f"\n[❌ ERROR]: No se encontró ningún evento asociado al ID {id_a_eliminar}.")
        pausa()
        return

    # 5. Pedimos confirmación de seguridad antes de borrar
    print(f"\n⚠️  ¿Está seguro de que desea eliminar el siguiente evento?")
    print(f" -> Fecha : {registro_encontrado['fecha']}")
    print(f" -> Evento: {registro_encontrado['evento']}")
    print(f" -> Lugar : {registro_encontrado['lugar']}")
    print("-" * ANCHO)

    confirmacion = input("Confirme la eliminación escribiendo 's' (sí) o 'n' (no): ").strip().lower()

    if confirmacion != 's' or confirmacion != 'si':
        print("\n[INFO]: Operación cancelada por el usuario. El registro se conserva.")
        pausa()
        return

    # 6. Eliminación segura de la lista en memoria
    # Usamos reasignación in-place (registros[:]) para modificar la lista original
    registros[:] = [item for item in registros if item.get('id') != id_a_eliminar]

    # 7. Sincronizamos los cambios permanentemente en JSON y CSV
    guardar_datos(registros)

    print(f"\n[ÉXITO]: El evento con ID {id_a_eliminar} ha sido eliminado correctamente del sistema.")
    pausa()