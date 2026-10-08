# ========================================================
# MÓDULO: UTILIDADES.PY
# Funciones transversales de consola e interfaz visual
# ========================================================

import textwrap # Permite ajustar texto a un ancho específico

import os  # Permite usar comandos del sistema (ej: limpiar pantalla)

ANCHO = 75  # Controla el ancho de toda la salida (alineación)

# --- FUNCIÓN: LIMPIAR PANTALLA ---
def limpiar_pantalla():
    """Limpia la consola según el sistema operativo (Windows/Linux/Mac)."""
    os.system("cls" if os.name == "nt" else "clear")

# --- FUNCIÓN: PAUSA ---
def pausa():
    """Espera que el usuario presione Enter para continuar."""
    input("\n🔸 Presione Enter para continuar...\n")

# --- FUNCIÓN: ENCABEZADO PANTALLA ---
def mostrar_encabezado(texto, limpiar = True, ancho=75):
    """
    Muestra un título decorado. 
    Si limpiar = True, limpia la pantalla antes de mostrarlo (ideal para pantallas nuevas).
    """
    if limpiar:
        limpiar_pantalla()
        
    print("=" * ancho)
    print(f"{texto.upper():^{ancho}}")
    print("=" * ancho + "\n")

# FUNCIÓN: IMPRIMIR MENSAJE DE INFORMACIÓN
def imprimir_info(texto):
    """
    Imprime un mensaje de información con formato.
    Ajusta el texto al ancho definido y lo centra.
    """
    lineas = textwrap.wrap(texto, width=ANCHO)
    for linea in lineas:
        print(linea)
