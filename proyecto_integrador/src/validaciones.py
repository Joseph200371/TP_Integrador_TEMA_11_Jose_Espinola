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

def validar_format_fecha(mensaje):
    """Valida que la fecha ingresada tenga el formato correcto (DD/MM/AAAA)."""
    patron = r'^\d{2}/\d{2}/\d{4}$'  # Expresión regular para validar el formato de fecha (DD/MM/AAAA)
    while True:
        fecha = input(mensaje).strip()
        if fecha == '0' or fecha == '':
            return None # Permite cancelar la operación con '0' o ENTER
        
        # Comprobamos si cumple el patrón de fecha con 're'
        if re.match(patron, fecha):
            return fecha
        
        print("¨[❌ERROR]: Formato de fecha inválido. Ingrese '0' o ENTER para cancelar.")

def validar_fecha_valida(mensaje):
    """Valida que la fecha ingresada sea una fecha válida (ej: 31/02/2023 no es válida)."""
    patron = r'^\d{2}/\d{2}/\d{4}$'
    while True:
        fecha_str = input(mensaje).strip()
        if fecha_str == '0' or fecha_str == '':
            return None # Permite cancelar la operación con '0' o ENTER

        # 1. Validar formato con Expresión Regular
        if not re.match(patron, fecha_str):
            print("[❌ ERROR]: Formato inválido. Use DD/MM/AAAA (o '0'/ENTER para cancelar).")
            continue

        # 2. Validar que la fecha sea real (ej: que no sea 31 de febrero)
        try:
            # Intentamos convertir el texto a un objeto fecha real
            datetime.strftime(fecha_str, "%d/%m/%Y")
            return fecha_str  # Retorna la fecha válida en formato de texto
        except ValueError:
            print("[❌ ERROR]: Fecha inexistente en el calendario. Ingrese una fecha válida.")

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