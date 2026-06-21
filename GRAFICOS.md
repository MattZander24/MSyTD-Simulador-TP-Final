# Guía de Gráficos - Simulador Juego EBRIO

Este documento explica en detalle cada uno de los gráficos generados por el simulador y cómo interpretarlos correctamente para obtener información valiosa de las simulaciones.

## Índice

1. [Simulación Individual](#simulación-individual)
2. [Distribución de Posiciones Finales](#distribución-de-posiciones-finales)
3. [Histograma de Distancias Finales](#histograma-de-distancias-finales)
4. [Convergencia Monte Carlo](#convergencia-monte-carlo)
5. [Mapa de Calor de Posiciones Finales](#mapa-de-calor-de-posiciones-finales)
6. [Animación Paso a Paso](#animación-paso-a-paso)

---

## Simulación Individual

### Descripción

Muestra la trayectoria completa de una única caminata aleatoria (Random Walk) en una grilla bidimensional.

### Elementos del Gráfico

- **Punto verde (Origen)**: Representa el punto de partida (0, 0) del borracho.
- **Estrella amarilla (Llaves)**: Indica la posición donde se encuentran las llaves configuradas.
- **Línea azul (Trayectoria)**: Muestra el camino completo seguido por el borracho durante todos los pasos.
- **Punto rojo (Posición Final)**: Indica dónde terminó el borracho después de completar todos los pasos.
- **Texto "¡Encontrado!"**: Aparece cerca de las llaves si el borracho pasó por esa coordenada durante el recorrido.

### Interpretación

**Para entender el comportamiento de una caminata individual:**

1. **Observar la trayectoria**: La línea azul muestra cómo el borracho se mueve aleatoriamente en las cuatro direcciones cardinales. No hay patrón predecible.

2. **Verificar si encontró las llaves**: Si aparece el texto "¡Encontrado!" cerca de la estrella amarilla, significa que el borracho pasó por esa coordenada en algún momento del recorrido.

3. **Analizar la posición final**: El punto rojo indica dónde terminó. Compare con el origen para ver qué tan lejos se alejó.

4. **Distancia al origen**: La distancia Manhattan desde el origen se puede calcular como |x| + |y|, donde (x, y) es la posición final.

**Ejemplo de interpretación:**
- Si la trayectoria muestra muchos cambios de dirección, esto es típico del comportamiento aleatorio.
- Si el borracho termina cerca del origen, indica que la caminata no se alejó mucho.
- Si el borracho termina lejos del origen, muestra cómo el movimiento aleatorio puede acumularse.

---

## Distribución de Posiciones Finales

### Descripción

Muestra un gráfico de barras con las 15 posiciones finales más frecuentes después de ejecutar múltiples simulaciones Monte Carlo.

### Elementos del Gráfico

- **Eje X**: Posiciones finales expresadas como coordenadas (x, y).
- **Eje Y**: Frecuencia (cantidad de simulaciones que terminaron en esa posición).
- **Barras azules**: Cada barra representa una posición final y su frecuencia.

### Interpretación

**Para entender la distribución de posiciones:**

1. **Identificar las posiciones más probables**: Las barras más altas indican las coordenadas donde es más probable terminar después de la cantidad de pasos configurada.

2. **Analizar la dispersión**: Si hay pocas barras altas y muchas bajas, indica que el borracho tiende a terminar en pocas posiciones específicas. Si las barras son más uniformes, indica mayor dispersión.

3. **Comparar con el origen**: Observe si (0, 0) aparece entre las posiciones más frecuentes. Esto indica la probabilidad de volver al origen.

4. **Simetría**: En un Random Walk bidimensional simétrico, se espera cierta simetría en la distribución (por ejemplo, si (2, 1) es frecuente, (-2, -1) también debería serlo).

**Ejemplo de interpretación:**
- Si (0, 0) tiene la barra más alta, significa que es muy probable volver al origen.
- Si las posiciones más frecuentes están a distancia 2 del origen, indica que después de esa cantidad de pasos, el borracho tiende a estar cerca.
- La distribución puede ayudar a identificar patrones o anomalías en el comportamiento del sistema.

---

## Histograma de Distancias Finales

### Descripción

Muestra la distribución de distancias Manhattan finales desde el origen para todas las simulaciones ejecutadas.

### Elementos del Gráfico

- **Eje X**: Distancia Manhattan (|x| + |y|).
- **Eje Y**: Frecuencia (cantidad de simulaciones que terminaron a esa distancia).
- **Barras coral con bordes negros**: Cada barra representa una distancia específica y cuántas simulaciones terminaron a esa distancia.

### Interpretación

**Para entender la distribución de distancias:**

1. **Distancia más probable**: La barra más alta indica la distancia Manhattan más frecuente desde el origen.

2. **Rango de distancias**: Observe el rango de distancias presentes. Un rango amplio indica que el borracho puede terminar muy cerca o muy lejos del origen.

3. **Tendencia central**: La mayoría de las simulaciones deberían concentrarse alrededor de una distancia central. Esto representa la distancia esperada.

4. **Colas de la distribución**: Las barras en los extremos (distancias muy pequeñas o muy grandes) representan eventos poco probables pero posibles.

**Ejemplo de interpretación:**
- Si la barra más alta está en distancia 2, significa que es más probable terminar a 2 unidades del origen.
- Si hay una barra alta en distancia 0, indica que es bastante probable volver exactamente al origen.
- La forma del histograma puede aproximarse a una distribución normal para un número grande de pasos, según el teorema del límite central.

---

## Convergencia Monte Carlo

### Descripción

Muestra cómo la probabilidad estimada converge a su valor verdadero a medida que aumenta el número de simulaciones.

### Elementos del Gráfico

- **Eje X**: Número de simulaciones (escala logarítmica).
- **Eje Y**: Probabilidad estimada para una distancia objetivo específica (por defecto distancia = 2).
- **Línea púrpura con puntos**: Muestra la evolución de la probabilidad estimada.
- **Escala logarítmica en X**: Permite ver claramente el comportamiento tanto para pocas como para muchas simulaciones.

### Interpretación

**Para entender la convergencia:**

1. **Estabilidad**: Cuando la línea se vuelve horizontal y estable, indica que la probabilidad estimada ha convergido.

2. **Velocidad de convergencia**: Observe cuántas simulaciones son necesarias para que la probabilidad se estabilice. Una convergencia rápida indica que se necesitan menos simulaciones para obtener una estimación confiable.

3. **Fluctuaciones iniciales**: Al principio (pocas simulaciones), la probabilidad puede fluctuar mucho. Esto es normal y esperado.

4. **Valor final**: El valor donde la línea se estabiliza es la mejor estimación de la probabilidad verdadera.

**Ejemplo de interpretación:**
- Si la línea se estabiliza alrededor de 0.25 después de 1000 simulaciones, significa que la probabilidad de terminar a distancia 2 es aproximadamente 25%.
- Si la línea sigue fluctuando incluso después de muchas simulaciones, puede indicar que se necesitan más simulaciones o que hay algún problema en el modelo.
- La convergencia es un concepto clave en Monte Carlo: más simulaciones generalmente llevan a estimaciones más precisas.

---

## Mapa de Calor de Posiciones Finales

### Descripción

Muestra una visualización bidimensional de la densidad de posiciones finales usando colores para indicar frecuencia.

### Elementos del Gráfico

- **Celdas de la grilla**: Cada celda representa una coordenada (x, y).
- **Colores (escala amarillo-naranja-rojo)**: 
  - Amarillo claro: Baja frecuencia (pocas simulaciones terminaron allí).
  - Naranja: Frecuencia media.
  - Rojo oscuro: Alta frecuencia (muchas simulaciones terminaron allí).
- **Barra de color (colorbar)**: Indica la escala de frecuencias.
- **Ejes X e Y**: Coordenadas de la grilla.

### Interpretación

**Para entender la distribución espacial:**

1. **Zonas calientes (rojo)**: Representan las posiciones donde el borracho termina con mayor frecuencia. Estas son las zonas más probables.

2. **Zonas frías (amarillo)**: Representan posiciones poco probables donde rara vez termina el borracho.

3. **Patrones espaciales**: Observe si hay patrones como anillos, clusters o simetrías. En un Random Walk simétrico, se espera simetría respecto al origen.

4. **Expansión desde el origen**: El mapa de calor puede mostrar cómo la probabilidad se distribuye en el espacio a partir del origen.

**Ejemplo de interpretación:**
- Si hay una zona roja alrededor del origen, indica que es probable terminar cerca de donde se empezó.
- Si el mapa muestra un patrón de anillos concéntricos, esto es típico de caminatas aleatorias donde la distancia al origen sigue una distribución específica.
- La simetría del mapa puede validar que el modelo está funcionando correctamente (debería ser simétrico si las probabilidades de movimiento son iguales en todas direcciones).

---

## Animación Paso a Paso

### Descripción

Muestra una animación de la simulación individual, visualizando cada paso del recorrido en tiempo real.

### Elementos de la Animación

- **Punto verde (Origen)**: Posición inicial (0, 0), estático durante toda la animación.
- **Estrella amarilla (Llaves)**: Posición de las llaves, estática durante toda la animación.
- **Línea azul (Trayectoria)**: Se dibuja progresivamente a medida que el borracho avanza.
- **Punto rojo (Posición Actual)**: Se mueve paso a paso mostrando la posición actual del borracho.
- **Caja de información**: Muestra en tiempo real:
  - Paso actual
  - Coordenada actual (x, y)
  - Distancia Manhattan al origen

### Interpretación

**Para entender el comportamiento dinámico:**

1. **Observar el movimiento aleatorio**: Cada paso es independiente y aleatorio, sin memoria de pasos anteriores.

2. **Seguir la distancia al origen**: La distancia puede aumentar, disminuir o mantenerse según la dirección del movimiento.

3. **Identificar patrones (o falta de ellos)**: En un Random Walk verdadero, no debería haber patrones predecibles en el movimiento.

4. **Verificar encuentros con las llaves**: Si el punto rojo pasa por la estrella amarilla, el borracho ha encontrado las llaves.

**Ejemplo de interpretación:**
- La animación ayuda a visualizar cómo el movimiento aleatorio puede llevar al borracho en cualquier dirección.
- Es útil para entender que aunque cada paso es aleatorio, después de muchos pasos puede haber una tendencia estadística (como alejarse del origen en promedio).
- La animación es especialmente útil para演示 (demostrar) el concepto a personas que no están familiarizadas con caminatas aleatorias.

---

## Consideraciones Generales

### Relación entre Gráficos

Los diferentes gráficos proporcionan perspectivas complementarias:

- **Simulación Individual + Animación**: Muestran el comportamiento de una única realización.
- **Distribución + Histograma + Heatmap**: Muestran el comportamiento estadístico de muchas realizaciones.
- **Convergencia**: Muestra la calidad de la estimación estadística.

### Tamaño de Muestra

- Para simulaciones con pocas corridas (ej. 100), los gráficos estadísticos pueden mostrar mucho ruido.
- Para simulaciones con muchas corridas (ej. 10000), los gráficos estadísticos serán más estables y confiables.
- La convergencia ayuda a determinar cuántas simulaciones son necesarias.

### Parámetros que Afectan los Gráficos

- **Cantidad de pasos**: Más pasos generalmente llevan a mayor dispersión en las posiciones finales.
- **Posición de las llaves**: Afecta la probabilidad de encontrarlas en simulaciones individuales.
- **Semilla aleatoria**: Permite reproducir exactamente los mismos gráficos para comparación.

---

## Recomendaciones de Uso

1. **Para exploración inicial**: Comience con una simulación individual y su animación para entender el comportamiento básico.

2. **Para análisis estadístico**: Ejecute Monte Carlo con al menos 1000 simulaciones y examine la distribución, histograma y heatmap.

3. **Para validar resultados**: Use el gráfico de convergencia para asegurarse de que la probabilidad estimada es estable.

4. **Para presentación**: El mapa de calor y la animación son excelentes para presentar resultados de forma visual.

5. **Para investigación**: Combine todos los gráficos para obtener una comprensión completa del comportamiento del sistema.
