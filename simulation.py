"""
Módulo de simulación para el problema del Juego EBRIO (Random Walk Bidimensional).

Este módulo contiene la lógica de simulación de la caminata aleatoria
de un borracho en una grilla bidimensional.
"""

import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class SimulationResult:
    """
    Clase para almacenar los resultados de una simulación individual.
    
    Attributes:
        path: Lista de coordenadas (x, y) visitadas durante la caminata
        final_position: Coordenada final (x, y)
        found_keys: Booleano indicando si se encontraron las llaves
        steps_to_keys: Número de pasos para encontrar las llaves (None si no se encontraron)
        returns_to_origin: Cantidad de veces que volvió al origen
    """
    path: List[Tuple[int, int]]
    final_position: Tuple[int, int]
    found_keys: bool
    steps_to_keys: Optional[int]
    returns_to_origin: int


class RandomWalkSimulation:
    """
    Clase principal para ejecutar simulaciones de Random Walk bidimensional.
    
    El borracho comienza en el origen (0,0) y en cada paso se mueve
    aleatoriamente en una de las cuatro direcciones cardinales con
    probabilidad uniforme (0.25 cada una).
    """
    
    # Definición de movimientos: (dx, dy)
    MOVES = {
        'N': (0, 1),   # Norte
        'S': (0, -1),  # Sur
        'E': (1, 0),   # Este
        'W': (-1, 0)   # Oeste
    }
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa el simulador.
        
        Args:
            seed: Semilla aleatoria opcional para reproducibilidad
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
    def manhattan_distance(self, position: Tuple[int, int]) -> int:
        """
        Calcula la distancia Manhattan desde el origen.
        
        Args:
            position: Coordenada (x, y)
            
        Returns:
            Distancia Manhattan = |x| + |y|
        """
        return abs(position[0]) + abs(position[1])
    
    def get_random_move(self) -> Tuple[int, int]:
        """
        Obtiene un movimiento aleatorio con probabilidad uniforme.
        
        Returns:
            Tupla (dx, dy) representando el movimiento
        """
        direction = random.choice(['N', 'S', 'E', 'W'])
        return self.MOVES[direction]
    
    def simulate_single(
        self,
        steps: int,
        keys_position: Tuple[int, int]
    ) -> SimulationResult:
        """
        Ejecuta una simulación individual de Random Walk.
        
        Args:
            steps: Cantidad de pasos a simular
            keys_position: Coordenada (x, y) donde están las llaves
            
        Returns:
            SimulationResult con los datos de la simulación
        """
        # Posición inicial
        x, y = 0, 0
        path = [(x, y)]
        
        found_keys = False
        steps_to_keys = None
        returns_to_origin = 0
        
        for step in range(1, steps + 1):
            # Paso 2: A partir de un generador de números aleatorios se obtienen
            # observaciones o datos (movimiento aleatorio)
            dx, dy = self.get_random_move()
            
            # Paso 3: Esas observaciones se transforman en entradas aptas para el modelo
            # (transformar el movimiento aleatorio en coordenadas)
            x += dx
            y += dy
            
            # Agregar al camino
            path.append((x, y))
            
            # Verificar si encontró las llaves
            if not found_keys and (x, y) == keys_position:
                found_keys = True
                steps_to_keys = step
            
            # Verificar si volvió al origen
            if (x, y) == (0, 0):
                returns_to_origin += 1
        
        return SimulationResult(
            path=path,
            final_position=(x, y),
            found_keys=found_keys,
            steps_to_keys=steps_to_keys,
            returns_to_origin=returns_to_origin
        )
    
    def simulate_monte_carlo(
        self,
        steps: int,
        num_simulations: int,
        keys_position: Tuple[int, int],
        progress_callback=None
    ) -> List[SimulationResult]:
        """
        Ejecuta múltiples simulaciones utilizando el método Monte Carlo.
        
        Args:
            steps: Cantidad de pasos por simulación
            num_simulations: Cantidad de simulaciones a ejecutar
            keys_position: Coordenada (x, y) donde están las llaves
            progress_callback: Función opcional para reportar progreso
            
        Returns:
            Lista de SimulationResult con los resultados de todas las simulaciones
        """
        # Paso 1: Construir el modelo
        # El modelo se construye en la inicialización de la clase RandomWalkSimulation
        # con las reglas de movimiento y la estructura de la caminata aleatoria
        
        results = []
        
        # Paso 4: Operar el modelo de manera tal que transforme las entradas en salidas,
        # iterando las veces necesarias
        for i in range(num_simulations):
            result = self.simulate_single(steps, keys_position)
            results.append(result)
            
            # Reportar progreso si se proporcionó callback
            if progress_callback:
                progress_callback(i + 1, num_simulations)
        
        # Paso 5: Realizar la "Contabilidad" de las salidas y utilizar estadísticas
        # para describir el comportamiento del sistema y tomar decisiones
        # La contabilidad se realiza en la clase MonteCarloStatistics que procesa
        # los resultados y calcula estadísticas descriptivas
        return results
    
    def calculate_position_probability(
        self,
        target_position: Tuple[int, int],
        steps: int,
        num_simulations: int
    ) -> float:
        """
        Calcula la probabilidad de terminar en una coordenada específica
        utilizando Monte Carlo.
        
        Args:
            target_position: Coordenada (x, y) objetivo
            steps: Cantidad de pasos por simulación
            num_simulations: Cantidad de simulaciones a ejecutar
            
        Returns:
            Probabilidad estimada de terminar en la coordenada objetivo
        """
        count = 0
        
        for _ in range(num_simulations):
            result = self.simulate_single(steps, (0, 0))  # Keys position no importa aquí
            if result.final_position == target_position:
                count += 1
        
        return count / num_simulations
