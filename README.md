# Simulador Juego EBRIO - Random Walk Bidimensional

Aplicación de escritorio completa en Python para resolver mediante simulación el problema "Juego EBRIO" de la materia Modelos, Simulación y Teoría de la Decisión.

## Descripción del Problema

El simulador implementa una caminata aleatoria bidimensional (Random Walk) donde un borracho parte desde el origen (0,0) y en cada esquina decide aleatoriamente moverse una calle hacia:

- **Norte** → (x, y+1)
- **Sur** → (x, y-1)
- **Este** → (x+1, y)
- **Oeste** → (x-1, y)

Todas las direcciones tienen probabilidad uniforme P = 0.25.

## Características

### Simulación Individual Animada
- Ejecución paso a paso de una única caminata
- Visualización de grilla, origen, llaves, trayectoria y posición actual
- Control de velocidad (lenta, media, rápida)
- Información en tiempo real: paso actual, coordenada, distancia al origen

### Simulación Monte Carlo
- Ejecución masiva de simulaciones (100, 1000, 10000, o valor personalizado)
- Cálculo de estadísticas:
  - Probabilidad de terminar a distancia Manhattan 2
  - Probabilidad de encontrar las llaves
  - Distancia promedio al origen
  - Posición final más frecuente
  - Cantidad de retornos al origen

### Consulta de Probabilidad
- Cálculo mediante Monte Carlo de la probabilidad de terminar en una coordenada específica

### Gráficos Interactivos
- **Distribución de posiciones finales**: Muestra las posiciones más frecuentes
- **Histograma de distancias**: Distribución de distancias Manhattan finales
- **Convergencia Monte Carlo**: Evolución de la probabilidad estimada
- **Mapa de calor**: Visualización de densidad de posiciones finales

### Funcionalidades Extra
- Barra de progreso para simulaciones largas
- Exportación de resultados a CSV
- Guardado de gráficos como PNG
- Semilla aleatoria opcional para reproducibilidad
- Generación de corridas aleatorias rápidas

## Tecnologías

- **Python 3.12+**
- **CustomTkinter**: Interfaz gráfica moderna
- **Matplotlib**: Gráficos y visualizaciones
- **NumPy**: Operaciones numéricas

## Estructura del Proyecto

```
MSyTD-Simulador-TP-Final/
│
├── main.py              # Punto de entrada
├── simulation.py        # Lógica de Random Walk
├── statistics.py        # Cálculos estadísticos Monte Carlo
├── visualization.py     # Gráficos con Matplotlib
├── ui.py                # Interfaz gráfica CustomTkinter
├── requirements.txt     # Dependencias
├── README.md           # Este archivo
│
└── assets/             # Carpeta para recursos
```

## Instalación

### Requisitos Previos
- Python 3.12 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Navegar al directorio del proyecto**
   ```bash
   cd "c:\Users\MATT\Desktop\LICENC. EN SISTEMAS\7TO CUATRIMESTRE\MODELOS, SIMULACION Y TEORÍA DE LA DECISION\TRABAJOS PRÁCTICOS\TP FINAL\I- SIMULADOR DE EVENTOS DISCRETOS\MSyTD-Simulador-TP-Final"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Iniciar la Aplicación

```bash
python main.py
```

### Uso Básico

1. **Configurar parámetros** en el panel izquierdo:
   - Cantidad de pasos (por defecto: 10)
   - Posición de las llaves (por defecto: 2, 2)
   - Cantidad de simulaciones (por defecto: 10000)
   - Coordenada objetivo para consulta de probabilidad (por defecto: 0, 0)
   - Semilla aleatoria (opcional, para reproducibilidad)
   - Velocidad de animación

2. **Ejecutar simulaciones**:
   - **Simulación Individual**: Animación paso a paso de una caminata
   - **Monte Carlo**: Ejecuta simulaciones masivas para estimar probabilidades
   - **Botones rápidos**: 100, 1000, o 10000 simulaciones con un clic

3. **Visualizar resultados**:
   - Panel central: Gráfico de la simulación actual
   - Panel derecho: Estadísticas numéricas
   - Botones de gráficos: Distribución, histograma, convergencia, heatmap

4. **Exportar datos**:
   - **Exportar CSV**: Guarda todos los resultados de las simulaciones
   - **Guardar Gráfico PNG**: Exporta el gráfico actual como imagen

## Parámetros por Defecto

- **Pasos**: 10
- **Llaves**: (2, 2)
- **Simulaciones Monte Carlo**: 10000
- **Velocidad de animación**: Media
- **Coordenada objetivo**: (0, 0)

## Distancia Manhattan

La aplicación utiliza exclusivamente distancia Manhattan:

```
distancia = |x| + |y|
```

## Definición de Encontrar las Llaves

Las llaves están ubicadas en una coordenada configurable. El borracho encuentra las llaves si en cualquier momento del recorrido pasa por dicha coordenada. No es necesario terminar sobre las llaves.

**Ejemplo**: Si las llaves están en (2,1) y el recorrido visita (2,1) en el paso 4, entonces `encontro_llaves = True` aunque termine en otra posición.

## Semilla Aleatoria

La semilla aleatoria es un parámetro opcional que permite controlar la generación de números aleatorios para garantizar la reproducibilidad de las simulaciones.

### Tipo de Dato
- **Tipo**: `int` (entero no negativo)
- **Opcional**: Si no se especifica, se utiliza `None` y los generadores aleatorios se inicializan con un valor impredecible
- **Restricción**: La semilla debe ser un número entero mayor o igual a 0

### Funcionamiento
Cuando se proporciona una semilla:
1. Se inicializa el generador aleatorio de Python (`random.seed(seed)`)
2. Se inicializa el generador aleatorio de NumPy (`np.random.seed(seed)`)
3. Todas las simulaciones ejecutadas con esa semilla producirán exactamente la misma secuencia de movimientos aleatorios

### Uso Práctico
- **Reproducibilidad**: Usar la misma semilla permite obtener resultados idénticos en diferentes ejecuciones
- **Depuración**: Facilita la identificación de errores al poder replicar exactamente una simulación problemática
- **Comparación**: Permite comparar diferentes configuraciones con la misma secuencia aleatoria

**Ejemplo**: Si se usa `semilla = 42`, todas las simulaciones ejecutadas con ese valor seguirán la misma trayectoria, independientemente de cuándo se ejecuten.

## Arquitectura del Código

### simulation.py
- `RandomWalkSimulation`: Clase principal para ejecutar simulaciones
- `SimulationResult`: Dataclass para almacenar resultados
- Métodos para caminata aleatoria y cálculo de distancia Manhattan

### statistics.py
- `MonteCarloStatistics`: Clase para análisis estadístico
- Cálculo de probabilidades, distribuciones y convergencia
- Exportación a CSV

### visualization.py
- `SimulationVisualizer`: Clase para generar gráficos
- Gráficos de distribución, histogramas, convergencia y heatmaps
- Animaciones de simulaciones individuales

### ui.py
- `DrunkWalkApp`: Clase principal de la interfaz gráfica
- Tres paneles: configuración, visualización, resultados
- Manejo de hilos para simulaciones largas sin bloquear la UI

### main.py
- Punto de entrada de la aplicación
- Configuración inicial de CustomTkinter

## Requisitos de Calidad

✅ Código completamente comentado
✅ Type hints cuando es posible
✅ Separación clara entre lógica y UI
✅ Sin variables globales
✅ Uso de clases cuando tiene sentido
✅ Manejo de errores en entradas numéricas
✅ UI responsiva mediante threading
✅ Arquitectura modular

## Licencia

Este proyecto fue desarrollado como trabajo práctico final para la materia Modelos, Simulación y Teoría de la Decisión.

## Autor

Trabajo Práctico Final - Simulación de Eventos Discretos
Carrera: Licenciatura en Sistemas
Materia: Modelos, Simulación y Teoría de la Decisión
