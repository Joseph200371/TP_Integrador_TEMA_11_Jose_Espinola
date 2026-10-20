import matplotlib.pyplot as plt  # Biblioteca para visualización de datos en Python (creación de gráficos)
from datetime import datetime
from utils.utilidades import pausa

def verificar_registros(registros):
    """Verifica si hay registros suficientes en el sistema antes de graficar."""
    if not registros:
        print("[⚠️ ADVERTENCIA]: No hay registros suficientes en el sistema para generar gráficos.")
        pausa()
        return False
    return True

# ============================================================================
# 1. HISTOGRAMA HORIZONTAL (Distribución de Longitud de Notas)
# ============================================================================
def grafico_histograma_notas_horizontal(registros):
    """Genera un histograma horizontal para analizar la distribución de la longitud de las notas."""
    # Validación previa: si no hay datos, cancela la ejecución del gráfico
    if not verificar_registros(registros): 
        return
    
    # --- PROCESAMIENTO DE DATOS ---
    longitudes = [len(r["notas"]) for r in registros]
    
    # --- CONFIGURACIÓN DE LA FIGURA ---
    plt.figure(figsize=(9, 5))
    
    # --- CREACIÓN DEL HISTOGRAMA HORIZONTAL ---
    # Usamos orientation='horizontal' para tumbar las barras
    n, bins, patches = plt.hist(
        longitudes, 
        bins=5,               # Divide los datos en 5 rangos o intervalos
        orientation='horizontal', # <-- CLAVE: Convierte el histograma en horizontal
        color='#e67e22',      # Color de relleno naranja moderno
        edgecolor='#2c3e50',  # Color del borde para mejor definición
        linewidth=1.2,        # Grosor del borde
        alpha=0.85            # Transparencia
    )
    
    # --- ETIQUETAS Y ESTÉTICA (Invertidas por el cambio de eje) ---
    plt.title("Histograma Horizontal: Longitud de las Notas", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Frecuencia (Cantidad de Eventos)", fontsize=11, fontweight='bold')  # Ahora la frecuencia va abajo
    plt.ylabel("Cantidad de Caracteres en las Notas", fontsize=11, fontweight='bold') # Los rangos van al costado
    
    # Cuadrícula vertical sutil (porque los valores numéricos ahora están en el eje X)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    
    # --- DISEÑO LIMPIO (CLEAN LOOK) ---
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# ==============================================================
# 2. GRÁFICO DE TORTA (Del ejemplo) - Proporción por Lugar
# ==============================================================
def grafico_torta_lugares(registros):
    """Genera un gráfico circular (torta) para mostrar la proporción porcentual de eventos por lugar."""
    # Validación previa: si no hay registros, cancela la ejecución
    if not verificar_registros(registros): 
        return
    
    # --- PROCESAMIENTO DE DATOS ---
    # Extraemos todos los lugares y contamos cuántas veces aparece cada uno
    lugares = [r["lugar"] for r in registros]
    conteo = {l: lugares.count(l) for l in set(lugares)}
    
    # --- CONFIGURACIÓN Y CREACIÓN DEL GRÁFICO ---
    # Definimos una figura cuadrada para que el gráfico de torta mantenga su forma circular perfecta
    plt.figure(figsize=(7, 7))
    
    plt.pie(
        conteo.values(),                                    # Valores numéricos de cada porción
        labels=conteo.keys(),                               # Etiquetas con los nombres de los lugares
        autopct='%1.1f%%',                                  # Muestra el porcentaje con un decimal en cada porción
        startangle=140,                                     # Rota el inicio del gráfico para mejorar la visibilidad
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'], # Paleta de colores variada
        textprops={'fontsize': 11, 'fontweight': 'bold'}    # Estilo y tamaño de fuente de las etiquetas
    )
    
    # Título principal del gráfico
    plt.title("Distribución Porcentual de Eventos por Lugar", fontsize=14, fontweight='bold', pad=15)
    
    # Ajusta los márgenes para que no se corte ningún texto
    plt.tight_layout()
    plt.show()

# ==============================================================
# 3. GRÁFICO DE LÍNEAS TEMPORAL (Investigado) - Evolución Cronológica
# ==============================================================
def grafico_lineas_tiempo(registros):
    """Genera un gráfico de líneas para analizar la evolución y tendencia de los eventos a lo largo del tiempo."""
    # Validación previa: si no hay registros, cancela la ejecución
    if not verificar_registros(registros): 
        return
    
    # --- PROCESAMIENTO Y CONVERSIÓN DE FECHAS ---
    # 1. Convertimos las fechas de texto ("DD/MM/YYYY") a objetos datetime reales de Python.
    # Esto es fundamental para que el sistema entienda el orden cronológico real y no ordene por texto alfabético.
    fechas_objs = [datetime.strptime(r["fecha"], "%d/%m/%Y") for r in registros]
    
    # Contamos cuántos eventos hay por cada objeto de fecha
    conteo_fechas = {}
    for f in fechas_objs:
        conteo_fechas[f] = conteo_fechas.get(f, 0) + 1
        
    # 2. Ordenamos las fechas de manera cronológica (de la más antigua a la más reciente)
    fechas_ordenadas = sorted(conteo_fechas.keys())
    cantidades = [conteo_fechas[f] for f in fechas_ordenadas]
    
    # 3. Volvemos a formatear las fechas ordenadas a texto ("DD/MM/YYYY") para mostrarlas claramente en el eje X
    fechas_str = [f.strftime("%d/%m/%Y") for f in fechas_ordenadas]

    # --- CONFIGURACIÓN DE LA FIGURA ---
    plt.figure(figsize=(9, 5))
    
    # Creamos el gráfico de líneas con marcadores en los puntos, color verde institucional y línea sólida
    plt.plot(
        fechas_str, 
        cantidades, 
        marker='o',          # Dibuja un círculo pequeño en cada coordenada de fecha
        color='#27ae60',
        linestyle='-',       # Línea continua
        linewidth=2,         # Grosor de la línea
        markersize=6         # Tamaño del marcador
    )
    
    # --- ETIQUETAS Y ESTÉTICA ---
    plt.title("Evolución Cronológica de Eventos", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Fecha", fontsize=11, fontweight='bold')
    plt.ylabel("Cantidad de Eventos", fontsize=11, fontweight='bold')
    
    # Rota las fechas en el eje X para evitar que se encimen y se lean perfecto
    plt.xticks(rotation=30, ha='right', fontsize=10)
    
    # Cuadrícula sutil para facilitar la lectura de los valores numéricos
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # --- DISEÑO LIMPIO (CLEAN LOOK) ---
    # Ocultamos los bordes superior y derecho para un acabado visual profesional
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# ==============================================================
# 4. GRÁFICO DE DÍAS DE LA SEMANA (Investigado) - Distribución semanal
# ==============================================================
def grafico_dias_semana(registros):
    """Genera un gráfico de barras para analizar qué días de la semana concentran la mayor cantidad de eventos."""
    # Validación previa: si no hay registros, cancela la ejecución
    if not verificar_registros(registros): 
        return
    
    # --- DICCIONARIO DE TRADUCCIÓN ---
    # Python numera los días de la semana del 0 (Lunes) al 6 (Domingo). 
    # Este diccionario nos permite mapear esos números a nombres legibles en español.
    dias_nombres = {
        0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 
        3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
    }
    
    # --- PROCESAMIENTO DE DATOS ---
    # Inicializamos un contador en 0 para cada día de la semana asegurando el orden cronológico de Lunes a Domingo
    dias_conteo = {dia: 0 for dia in dias_nombres.values()}
    
    # Recorremos cada registro, transformamos su fecha y determinamos a qué día de la semana corresponde
    for r in registros:
        dt = datetime.strptime(r["fecha"], "%d/%m/%Y")
        nombre_dia = dias_nombres[dt.weekday()]  # dt.weekday() devuelve un entero del 0 al 6
        dias_conteo[nombre_dia] += 1

    # --- CONFIGURACIÓN DE LA FIGURA ---
    plt.figure(figsize=(9, 5))
    
    # Creamos el gráfico de barras con un tono violeta/púrpura moderno y bordes definidos
    barras = plt.bar(
        list(dias_conteo.keys()), 
        list(dias_conteo.values()), 
        color='#9b59b6',     # Color violeta institucional
        edgecolor='#2c3e50', # Borde oscuro para contraste
        linewidth=1.2          # Grosor del borde
    )
    
    # --- ETIQUETAS DE VALORES EXACTOS ---
    # Recorremos cada barra para imprimir su valor numérico exacto flotando justo arriba de ella
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:  # Solo muestra el texto si la barra tiene al menos 1 evento
            plt.text(
                barra.get_x() + barra.get_width() / 2, 
                altura + 0.1, 
                str(int(altura)), 
                ha='center', 
                va='bottom', 
                fontsize=10, 
                fontweight='bold'
            )

    # --- ETIQUETAS Y ESTÉTICA ---
    plt.title("Distribución de Eventos por Día de la Semana", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Día de la Semana", fontsize=11, fontweight='bold')
    plt.ylabel("Cantidad de Eventos", fontsize=11, fontweight='bold')
    
    # Cuadrícula horizontal sutil para facilitar la lectura visual
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # --- DISEÑO LIMPIO (CLEAN LOOK) ---
    # Ocultamos los bordes superior y derecho para un acabado profesional
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# ==============================================================
# 5. PANEL GENERAL DE SUBPLOTS 2x2 (Integra los 4 gráficos)
# ==============================================================
def mostrar_panel_subplots(registros):
    """Genera una única ventana con una cuadrícula de 2x2 subplots con el orden correcto (2 del ejemplo, 2 investigados)."""
    # Validación previa: si no hay registros, cancela la ejecución
    if not verificar_registros(registros): 
        return
    
    # Creamos la figura con un tamaño de 14x10 pulgadas
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Panel General de Estadísticas - Calendario de Eventos", fontsize=16, fontweight='bold', y=0.96)
    
    # --- PREPARACIÓN DE DATOS ---
    # 1. Datos para Torta (Lugares)
    lugares = [r["lugar"] for r in registros]
    conteo_lugares = {l: lugares.count(l) for l in set(lugares)}

    # 2. Datos para Líneas (Fechas ordenadas cronológicamente con datetime)
    fechas_objs = [datetime.strptime(r["fecha"], "%d/%m/%Y") for r in registros]
    conteo_fechas = {}
    for f in fechas_objs:
        conteo_fechas[f] = conteo_fechas.get(f, 0) + 1
    fechas_ordenadas = sorted(conteo_fechas.keys())
    cantidades_fechas = [conteo_fechas[f] for f in fechas_ordenadas]
    fechas_str = [f.strftime("%d/%m/%Y") for f in fechas_ordenadas]

    # 3. Datos para Dispersión e Histograma
    ids = [r["id"] for r in registros]
    longitudes_notas = [len(r["notas"]) for r in registros]

    # --- SUBPLOT 1 (Superior Izquierda): Gráfico de Torta (Ejemplo 1/2) ---
    axs[0, 0].pie(conteo_lugares.values(), labels=conteo_lugares.keys(), autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    axs[0, 0].set_title("1. Proporción por Lugar (Torta)", fontweight='bold', fontsize=12)

    # --- SUBPLOT 2 (Superior Derecha): Dispersión / Scatter (Ejemplo 2/2) ---
    axs[0, 1].scatter(ids, longitudes_notas, color='#8e44ad', s=80, edgecolor='#2c3e50', alpha=0.85)
    axs[0, 1].set_title("2. Dispersión: ID vs Longitud de Notas", fontweight='bold', fontsize=12)
    axs[0, 1].grid(True, linestyle='--', alpha=0.5)
    axs[0, 1].spines['top'].set_visible(False)
    axs[0, 1].spines['right'].set_visible(False)

    # --- SUBPLOT 3 (Inferior Izquierda): Líneas Temporal (Investigado 1/2) ---
    axs[1, 0].plot(fechas_str, cantidades_fechas, marker='o', color='#27ae60', linestyle='-', linewidth=2)
    axs[1, 0].set_title("3. Evolución Cronológica (Líneas)", fontweight='bold', fontsize=12)
    axs[1, 0].tick_params(axis='x', rotation=20)
    axs[1, 0].grid(True, linestyle='--', alpha=0.5)
    axs[1, 0].spines['top'].set_visible(False)
    axs[1, 0].spines['right'].set_visible(False)

    # --- SUBPLOT 4 (Inferior Derecha): Histograma (Investigado 2/2) ---
    axs[1, 1].hist(longitudes_notas, bins=5, color='#e67e22', edgecolor='#2c3e50', alpha=0.85)
    axs[1, 1].set_title("4. Histograma: Longitud de Notas", fontweight='bold', fontsize=12)
    axs[1, 1].grid(axis='y', linestyle='--', alpha=0.5)
    axs[1, 1].spines['top'].set_visible(False)
    axs[1, 1].spines['right'].set_visible(False)

    # Ajustamos el diseño general
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])
    plt.show()