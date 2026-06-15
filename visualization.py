"""
Módulo de visualización para gráficos y animaciones.

Este módulo contiene funciones para generar gráficos con Matplotlib
y visualizaciones de las simulaciones.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import List, Tuple, Dict, Optional
from simulation import SimulationResult
from statistics import MonteCarloStatistics


class SimulationVisualizer:
    """
    Clase para visualizar simulaciones y resultados estadísticos.
    """
    
    def __init__(self):
        """Inicializa el visualizador con configuración de estilo."""
        plt.style.use('seaborn-v0_8-darkgrid')
        self.figures = []
    
    def plot_single_simulation(
        self,
        result: SimulationResult,
        keys_position: Tuple[int, int],
        ax: Optional[plt.Axes] = None
    ) -> plt.Figure:
        """
        Grafica una simulación individual con la trayectoria completa.
        
        Args:
            result: Resultado de la simulación
            keys_position: Coordenada de las llaves
            ax: Eje matplotlib opcional (si se proporciona, se usa en lugar de crear figura nueva)
            
        Returns:
            Figure de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        else:
            fig = ax.figure
        
        # Extraer coordenadas del camino
        x_coords = [pos[0] for pos in result.path]
        y_coords = [pos[1] for pos in result.path]
        
        # Determinar límites del gráfico
        all_x = x_coords + [keys_position[0]]
        all_y = y_coords + [keys_position[1]]
        max_range = max(max(abs(x) for x in all_x), max(abs(y) for y in all_y)) + 2
        
        # Graficar grilla
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_aspect('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Simulación Individual - Random Walk')
        
        # Graficar origen
        ax.plot(0, 0, 'go', markersize=12, label='Origen', zorder=5)
        
        # Graficar llaves
        ax.plot(keys_position[0], keys_position[1], 'y*', markersize=15, 
               label='Llaves', zorder=5)
        
        # Graficar trayectoria
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.7, label='Trayectoria')
        
        # Graficar posición final
        ax.plot(result.final_position[0], result.final_position[1], 'ro', 
               markersize=10, label='Posición Final', zorder=5)
        
        # Marcar si encontró llaves
        if result.found_keys:
            ax.text(keys_position[0], keys_position[1] + 0.3, '¡Encontrado!', 
                   ha='center', va='bottom', fontsize=10, color='red', fontweight='bold')
        
        ax.legend(loc='upper right')
        
        return fig
    
    def plot_final_positions_distribution(
        self,
        stats: MonteCarloStatistics,
        ax: Optional[plt.Axes] = None
    ) -> plt.Figure:
        """
        Grafica la distribución de posiciones finales.
        
        Args:
            stats: Objeto de estadísticas Monte Carlo
            ax: Eje matplotlib opcional
            
        Returns:
            Figure de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        else:
            fig = ax.figure
        
        distribution = stats.final_positions_distribution()
        
        if not distribution:
            ax.text(0.5, 0.5, 'No hay datos para graficar', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Ordenar por frecuencia
        sorted_positions = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        positions = [f"({x}, {y})" for (x, y), _ in sorted_positions[:15]]
        frequencies = [freq for _, freq in sorted_positions[:15]]
        
        ax.bar(range(len(positions)), frequencies, color='steelblue', alpha=0.8)
        ax.set_xticks(range(len(positions)))
        ax.set_xticklabels(positions, rotation=45, ha='right')
        ax.set_xlabel('Posición Final')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Distribución de Posiciones Finales (Top 15)')
        ax.tight_layout()
        
        return fig
    
    def plot_distance_histogram(
        self,
        stats: MonteCarloStatistics,
        ax: Optional[plt.Axes] = None
    ) -> plt.Figure:
        """
        Grafica el histograma de distancias finales Manhattan.
        
        Args:
            stats: Objeto de estadísticas Monte Carlo
            ax: Eje matplotlib opcional
            
        Returns:
            Figure de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        else:
            fig = ax.figure
        
        distance_dist = stats.distance_distribution()
        
        if not distance_dist:
            ax.text(0.5, 0.5, 'No hay datos para graficar', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        distances = sorted(distance_dist.keys())
        frequencies = [distance_dist[d] for d in distances]
        
        ax.bar(distances, frequencies, color='coral', alpha=0.8, edgecolor='black')
        ax.set_xlabel('Distancia Manhattan')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Histograma de Distancias Finales')
        ax.grid(axis='y', alpha=0.3)
        
        return fig
    
    def plot_convergence(
        self,
        stats: MonteCarloStatistics,
        target_distance: int = 2,
        ax: Optional[plt.Axes] = None
    ) -> plt.Figure:
        """
        Grafica la convergencia de la probabilidad estimada.
        
        Args:
            stats: Objeto de estadísticas Monte Carlo
            target_distance: Distancia objetivo para convergencia
            ax: Eje matplotlib opcional
            
        Returns:
            Figure de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        else:
            fig = ax.figure
        
        convergence_data = stats.convergence_data(target_distance)
        
        if not convergence_data:
            ax.text(0.5, 0.5, 'No hay suficientes datos para graficar convergencia', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        n_simulations = [n for n, _ in convergence_data]
        probabilities = [p for _, p in convergence_data]
        
        ax.plot(n_simulations, probabilities, 'o-', linewidth=2, markersize=8, color='purple')
        ax.set_xlabel('Número de Simulaciones')
        ax.set_ylabel(f'Probabilidad (Distancia = {target_distance})')
        ax.set_title('Convergencia Monte Carlo')
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        
        return fig
    
    def plot_heatmap(
        self,
        stats: MonteCarloStatistics,
        ax: Optional[plt.Axes] = None
    ) -> plt.Figure:
        """
        Genera un mapa de calor de las posiciones finales.
        
        Args:
            stats: Objeto de estadísticas Monte Carlo
            ax: Eje matplotlib opcional
            
        Returns:
            Figure de matplotlib
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        else:
            fig = ax.figure
        
        distribution = stats.final_positions_distribution()
        
        if not distribution:
            ax.text(0.5, 0.5, 'No hay datos para graficar', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Crear matriz para el heatmap
        all_x = [pos[0] for pos in distribution.keys()]
        all_y = [pos[1] for pos in distribution.keys()]
        
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        
        heatmap_data = np.zeros((y_max - y_min + 1, x_max - x_min + 1))
        
        for (x, y), freq in distribution.items():
            heatmap_data[y - y_min, x - x_min] = freq
        
        im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto', origin='lower')
        
        # Configurar etiquetas
        ax.set_xticks(range(x_max - x_min + 1))
        ax.set_yticks(range(y_max - y_min + 1))
        ax.set_xticklabels(range(x_min, x_max + 1))
        ax.set_yticklabels(range(y_min, y_max + 1))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Mapa de Calor de Posiciones Finales')
        
        # Agregar colorbar
        plt.colorbar(im, ax=ax, label='Frecuencia')
        
        return fig
    
    def create_animation(
        self,
        result: SimulationResult,
        keys_position: Tuple[int, int],
        interval: int = 500
    ) -> animation.FuncAnimation:
        """
        Crea una animación de la simulación paso a paso.
        
        Args:
            result: Resultado de la simulación
            keys_position: Coordenada de las llaves
            interval: Intervalo entre frames en milisegundos
            
        Returns:
            Objeto FuncAnimation de matplotlib
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Configurar gráfico
        x_coords = [pos[0] for pos in result.path]
        y_coords = [pos[1] for pos in result.path]
        
        all_x = x_coords + [keys_position[0]]
        all_y = y_coords + [keys_position[1]]
        max_range = max(max(abs(x) for x in all_x), max(abs(y) for y in all_y)) + 2
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_aspect('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Animación - Random Walk')
        
        # Elementos estáticos
        ax.plot(0, 0, 'go', markersize=12, label='Origen', zorder=5)
        ax.plot(keys_position[0], keys_position[1], 'y*', markersize=15, 
               label='Llaves', zorder=5)
        
        # Elementos dinámicos
        line, = ax.plot([], [], 'b-', linewidth=2, alpha=0.7, label='Trayectoria')
        point, = ax.plot([], [], 'ro', markersize=10, label='Posición Actual', zorder=5)
        step_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                           va='top', ha='left', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.legend(loc='upper right')
        
        def init():
            line.set_data([], [])
            point.set_data([], [])
            step_text.set_text('')
            return line, point, step_text
        
        def update(frame):
            # Actualizar trayectoria hasta el frame actual
            line.set_data(x_coords[:frame+1], y_coords[:frame+1])
            
            # Actualizar posición actual
            point.set_data([x_coords[frame]], [y_coords[frame]])
            
            # Actualizar texto
            current_pos = result.path[frame]
            distance = abs(current_pos[0]) + abs(current_pos[1])
            step_text.set_text(f'Paso: {frame}\nPosición: {current_pos}\nDistancia: {distance}')
            
            return line, point, step_text
        
        ani = animation.FuncAnimation(
            fig, update, frames=len(result.path),
            init_func=init, blit=True, interval=interval, repeat=False
        )
        
        return ani
    
    def embed_figure_in_tkinter(self, fig: plt.Figure, parent_widget) -> FigureCanvasTkAgg:
        """
        Embebe una figura de matplotlib en un widget de Tkinter.
        
        Args:
            fig: Figure de matplotlib
            parent_widget: Widget padre de Tkinter
            
        Returns:
            Canvas de matplotlib para Tkinter
        """
        canvas = FigureCanvasTkAgg(fig, master=parent_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        return canvas
    
    def save_figure(self, fig: plt.Figure, filename: str) -> None:
        """
        Guarda una figura como archivo PNG.
        
        Args:
            fig: Figure de matplotlib
            filename: Nombre del archivo de salida
        """
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
