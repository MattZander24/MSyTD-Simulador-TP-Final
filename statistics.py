"""
Módulo de estadísticas para el análisis de simulaciones Monte Carlo.

Este módulo contiene funciones para calcular estadísticas
a partir de los resultados de múltiples simulaciones.
"""

from typing import List, Tuple, Dict
from collections import Counter
import numpy as np
from simulation import SimulationResult


class MonteCarloStatistics:
    """
    Clase para calcular estadísticas a partir de simulaciones Monte Carlo.
    """
    
    def __init__(self, results: List[SimulationResult]):
        """
        Inicializa el analizador estadístico.
        
        Args:
            results: Lista de SimulationResult de las simulaciones
        """
        self.results = results
        self.num_simulations = len(results)
    
    def probability_distance_2(self) -> float:
        """
        Calcula la probabilidad de terminar a distancia Manhattan 2.
        
        Returns:
            Probabilidad estimada (entre 0 y 1)
        """
        count = 0
        for result in self.results:
            distance = abs(result.final_position[0]) + abs(result.final_position[1])
            if distance == 2:
                count += 1
        return count / self.num_simulations
    
    def probability_find_keys(self) -> float:
        """
        Calcula la probabilidad de encontrar las llaves.
        
        Returns:
            Probabilidad estimada (entre 0 y 1)
        """
        count = sum(1 for result in self.results if result.found_keys)
        return count / self.num_simulations
    
    def average_distance_to_origin(self) -> float:
        """
        Calcula la distancia promedio al origen de las posiciones finales.
        
        Returns:
            Distancia Manhattan promedio
        """
        distances = []
        for result in self.results:
            distance = abs(result.final_position[0]) + abs(result.final_position[1])
            distances.append(distance)
        return np.mean(distances)
    
    def most_frequent_final_position(self) -> Tuple[int, int]:
        """
        Determina la posición final más frecuente.
        
        Returns:
            Coordenada (x, y) más frecuente
        """
        positions = [result.final_position for result in self.results]
        counter = Counter(positions)
        return counter.most_common(1)[0][0]
    
    def total_returns_to_origin(self) -> int:
        """
        Calcula el total de veces que el borracho volvió al origen.
        
        Returns:
            Cantidad total de retornos al origen
        """
        return sum(result.returns_to_origin for result in self.results)
    
    def final_positions_distribution(self) -> Dict[Tuple[int, int], int]:
        """
        Obtiene la distribución de posiciones finales.
        
        Returns:
            Diccionario con coordenadas como clave y frecuencia como valor
        """
        positions = [result.final_position for result in self.results]
        return dict(Counter(positions))
    
    def distance_distribution(self) -> Dict[int, int]:
        """
        Obtiene la distribución de distancias finales Manhattan.
        
        Returns:
            Diccionario con distancia como clave y frecuencia como valor
        """
        distances = []
        for result in self.results:
            distance = abs(result.final_position[0]) + abs(result.final_position[1])
            distances.append(distance)
        return dict(Counter(distances))
    
    def convergence_data(
        self,
        target_distance: int = 2
    ) -> List[Tuple[int, float]]:
        """
        Genera datos para graficar la convergencia de la probabilidad estimada.
        
        Args:
            target_distance: Distancia objetivo para calcular convergencia
            
        Returns:
            Lista de tuplas (n_simulations, probability) para diferentes tamaños de muestra
        """
        convergence_points = [100, 500, 1000, 5000, 10000]
        convergence_data = []
        
        for n in convergence_points:
            if n > self.num_simulations:
                continue
            
            count = 0
            for i in range(n):
                distance = abs(self.results[i].final_position[0]) + abs(self.results[i].final_position[1])
                if distance == target_distance:
                    count += 1
            
            probability = count / n
            convergence_data.append((n, probability))
        
        return convergence_data
    
    def calculate_position_probability(
        self,
        target_position: Tuple[int, int]
    ) -> float:
        """
        Calcula la probabilidad de terminar en una coordenada específica.
        
        Args:
            target_position: Coordenada (x, y) objetivo
            
        Returns:
            Probabilidad estimada (entre 0 y 1)
        """
        count = sum(1 for result in self.results if result.final_position == target_position)
        return count / self.num_simulations
    
    def get_summary(self) -> Dict[str, any]:
        """
        Obtiene un resumen de todas las estadísticas principales.
        
        Returns:
            Diccionario con todas las estadísticas calculadas
        """
        return {
            'prob_distance_2': self.probability_distance_2(),
            'prob_find_keys': self.probability_find_keys(),
            'avg_distance': self.average_distance_to_origin(),
            'most_frequent_position': self.most_frequent_final_position(),
            'total_returns_origin': self.total_returns_to_origin(),
            'num_simulations': self.num_simulations
        }
    
    def export_to_csv(self, filename: str) -> None:
        """
        Exporta los resultados de las simulaciones a un archivo CSV.
        
        Args:
            filename: Nombre del archivo CSV a crear
        """
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir encabezados
            writer.writerow([
                'Simulacion',
                'Posicion_Final_X',
                'Posicion_Final_Y',
                'Distancia_Origen',
                'Encontro_Llaves',
                'Pasos_Hasta_Llaves',
                'Retornos_Origen'
            ])
            
            # Escribir datos
            for i, result in enumerate(self.results, 1):
                distance = abs(result.final_position[0]) + abs(result.final_position[1])
                writer.writerow([
                    i,
                    result.final_position[0],
                    result.final_position[1],
                    distance,
                    result.found_keys,
                    result.steps_to_keys if result.steps_to_keys else 'N/A',
                    result.returns_to_origin
                ])
