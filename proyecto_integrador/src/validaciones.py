# =================================================================
# MÓDULO: VALIDACIONES.PY
# Control de entradas y unicidad (Clave única oculta al usuario)
# =================================================================

import  re # Permite usar expresiones regulares para validar formatos de texto (ej: email, teléfono, etc.)

from datetime import datetime # Permite trabajar con fechas y horas

def validar_texto(mensaje):
    """Valida que el campo no esté vacío y permite cancelar con '0' o ENTER."""
    while True:
        dato = input(mensaje).strip() # Elimina espacios al inicio y al final
        if dato == '0' or dato == '':
            return None # Permite cancelar la operación con '0' o ENTER
        
        if len(dato) > 0: # Valida que el campo no esté vacío
            return dato
        
        print("¨[❌ERROR]: Este campo no puede estar vacío. Ingrese '0' o ENTER para cancelar.")

def verificar_duplicado(registros, fecha, evento):
    """Verifica internamente si ya existe una combinación de fecha y evento (Clave única)."""
    for r in registros:
        if r['fecha'] == fecha and r['evento'].lower() == evento.lower():
            return True  # Retorna True si se encuentra un duplicado
    
    return False  # Retorna False si no se encuentra duplicado

from datetime import datetime
import re

def validar_fecha_valida(mensaje):
    """
    Función unificada: Valida en un solo paso que la fecha tenga 
    el formato correcto (DD/MM/AAAA) y que sea un día real del calendario.
    Permite cancelar ingresando '0' o presionando ENTER.
    """
    patron = r'^\d{2}/\d{2}/\d{4}$'  # Expresión regular para el formato
    
    while True:
        fecha_str = input(mensaje).strip()
        
        # Opción de salida / cancelación
        if fecha_str == '0' or fecha_str == '':
            return None 

        # PASO 1: Validar el formato visual con la expresión regular
        if not re.match(patron, fecha_str):
            print("[❌ ERROR]: Formato inválido. Use estrictamente DD/MM/AAAA (o '0'/ENTER para cancelar).")
            continue  # Vuelve a pedir el ingreso

        # PASO 2: Validar que sea una fecha real en el calendario (ej: evita el 31/02/2026)
        try:
            datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha_str  # Si pasó ambas pruebas, retornamos la fecha lista para usar
        except ValueError:
            print("[❌ ERROR]: La fecha ingresada no existe en el calendario. Ingrese una fecha real.")

def validar_evento(evento):
    """
    Valida que el texto del evento cumpla con los requisitos mínimos:
    - No puede estar vacío ni contener solo espacios.
    - Longitud máxima de 50 caracteres (para evitar desbordes en consola).
    - Debe contener al menos una letra (evita cadenas formadas solo por números o símbolos).
    
    Retorna:
        str: El texto limpio y 'strippeado' si es válido.
        False: Si no cumple con las reglas de validación.
    """
    if not evento or not isinstance(evento, str):
        return False
    
    # .strip() elimina espacios sobrantes al inicio y final
    evento_limpio = evento.strip()  # Elimina espacios al inicio y al final

    # Validar capos vacíos o exceso de caracteres
    if not evento_limpio or len(evento_limpio) > 50:
        return False

    # """Validar que el evento contenga solo letras, números y espacios"""
    #   if not re.match(r'^[A-Za-z0-9 ]+$', evento):
    #        return False

    # Asegurar mediante .isalpha() que exista al menos un carácter alfabético
    if not any(caracter.isalpha() for caracter in evento_limpio):  # Asegura que haya al menos una letra
        return False
    
    return evento_limpio # Devuelve el texto ya 'strippeado' listo para ser almacenado

def leer_campo_opcional(mensaje, valor_por_defecto="Sin especificar"):
    """
    Solicita un campo de texto opcional al usuario.
    - Si ingresa '0', retorna None (señal de cancelación).
    - Si presiona ENTER (vacío), retorna el valor por defecto.
    - Si ingresa texto válido, lo retorna.
    """
    texto = validar_texto(mensaje)
    
    if texto == '0':
        return None  # Indicador de cancelación
        
    # Si dio ENTER devuelve el valor por defecto, sino el texto ingresado
    return texto if texto else valor_por_defecto