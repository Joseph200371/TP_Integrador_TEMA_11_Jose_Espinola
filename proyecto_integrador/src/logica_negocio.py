# ===============================================
# MÓDULO: LOGICA_NEGOCIO.PY
# Contiene todas las funciones atómicas del ABM
# ===============================================

from utils.utilidades import limpiar_pantalla, pausa

# --- 1. ALTA (Crear Registro - Opción 1) ---
def crear_registro(registros):
    # Lógica de creación con cancelación limpia
    limpiar_pantalla()
    print("=== OPCIÓN 1: CREAR NUEVO EVENTO ===")
    print("NOTA: Puede cancelar la creación ingresando '0' o presionando ENTER.\n")

    pass

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