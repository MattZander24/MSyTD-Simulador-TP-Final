"""
Módulo de interfaz gráfica de usuario utilizando CustomTkinter.

Este módulo contiene la interfaz gráfica completa para el simulador
del problema del Juego EBRIO.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional, Tuple
import time

from simulation import RandomWalkSimulation, SimulationResult
from statistics import MonteCarloStatistics
from visualization import SimulationVisualizer


class DrunkWalkApp(ctk.CTk):
    """
    Aplicación principal del simulador de Random Walk.
    
    Esta clase implementa la interfaz gráfica completa con tres paneles:
    - Panel izquierdo: Configuración
    - Panel central: Visualización
    - Panel derecho: Resultados
    """
    
    def __init__(self):
        """Inicializa la aplicación principal."""
        super().__init__()
        
        # Configuración de la ventana
        self.title("Simulador Juego EBRIO - Random Walk Bidimensional")
        self.geometry("1400x800")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables de configuración (crear antes de los widgets)
        self.steps_var = ctk.StringVar(value="10")
        self.keys_x_var = ctk.StringVar(value="2")
        self.keys_y_var = ctk.StringVar(value="2")
        self.num_simulations_var = ctk.StringVar(value="10000")
        self.target_x_var = ctk.StringVar(value="0")
        self.target_y_var = ctk.StringVar(value="0")
        self.seed_var = ctk.StringVar(value="")
        self.speed_var = ctk.StringVar(value="media")
        
        # Inicializar componentes
        self.simulator = RandomWalkSimulation()
        self.visualizer = SimulationVisualizer()
        self.current_result: Optional[SimulationResult] = None
        self.current_stats: Optional[MonteCarloStatistics] = None
        self.animation_running = False
        self.simulation_thread: Optional[threading.Thread] = None
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz gráfica."""
        # Crear frame principal con tres columnas
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Crear los tres paneles
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
    
    def create_left_panel(self):
        """Crea el panel izquierdo de configuración."""
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Título
        title_label = ctk.CTkLabel(
            self.left_panel, 
            text="Configuración", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Frame de parámetros
        params_frame = ctk.CTkFrame(self.left_panel)
        params_frame.pack(fill="x", padx=10, pady=5)
        
        # Cantidad de pasos
        self.create_input_field(
            params_frame, "Cantidad de Pasos:", 
            self.steps_var, 0
        )
        
        # Posición X de llaves
        self.create_input_field(
            params_frame, "Posición X Llaves:", 
            self.keys_x_var, 1
        )
        
        # Posición Y de llaves
        self.create_input_field(
            params_frame, "Posición Y Llaves:", 
            self.keys_y_var, 2
        )
        
        # Cantidad de simulaciones
        self.create_input_field(
            params_frame, "Simulaciones Monte Carlo:", 
            self.num_simulations_var, 3
        )
        
        # Coordenada objetivo X
        self.create_input_field(
            params_frame, "Coordenada Objetivo X:", 
            self.target_x_var, 4
        )
        
        # Coordenada objetivo Y
        self.create_input_field(
            params_frame, "Coordenada Objetivo Y:", 
            self.target_y_var, 5
        )
        
        # Semilla aleatoria
        seed_label = ctk.CTkLabel(params_frame, text="Semilla (opcional):")
        seed_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        seed_entry = ctk.CTkEntry(params_frame, textvariable=self.seed_var)
        seed_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        
        # Velocidad de animación
        speed_label = ctk.CTkLabel(params_frame, text="Velocidad Animación:")
        speed_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        speed_menu = ctk.CTkOptionMenu(
            params_frame, 
            values=["lenta", "media", "rápida"],
            variable=self.speed_var
        )
        speed_menu.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
        
        # Botones principales
        buttons_frame = ctk.CTkFrame(self.left_panel)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.run_single_btn = ctk.CTkButton(
            buttons_frame,
            text="Ejecutar Simulación Individual",
            command=self.run_single_simulation,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.run_single_btn.pack(fill="x", padx=5, pady=5)
        
        self.run_monte_carlo_btn = ctk.CTkButton(
            buttons_frame,
            text="Ejecutar Monte Carlo",
            command=self.run_monte_carlo,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.run_monte_carlo_btn.pack(fill="x", padx=5, pady=5)
        
        self.calc_prob_btn = ctk.CTkButton(
            buttons_frame,
            text="Calcular Probabilidad Coordenada",
            command=self.calculate_position_probability,
            height=40
        )
        self.calc_prob_btn.pack(fill="x", padx=5, pady=5)
        
        self.random_run_btn = ctk.CTkButton(
            buttons_frame,
            text="Generar Corrida Aleatoria",
            command=self.generate_random_run,
            height=40
        )
        self.random_run_btn.pack(fill="x", padx=5, pady=5)
        
        # Botones de utilidad
        utility_frame = ctk.CTkFrame(self.left_panel)
        utility_frame.pack(fill="x", padx=10, pady=10)
        
        self.export_btn = ctk.CTkButton(
            utility_frame,
            text="Exportar CSV",
            command=self.export_csv,
            state="disabled"
        )
        self.export_btn.pack(fill="x", padx=5, pady=2)
        
        self.clear_btn = ctk.CTkButton(
            utility_frame,
            text="Limpiar",
            command=self.clear_all,
            fg_color="red"
        )
        self.clear_btn.pack(fill="x", padx=5, pady=2)
        
        # Barra de progreso
        self.progress_frame = ctk.CTkFrame(self.left_panel)
        self.progress_frame.pack(fill="x", padx=10, pady=10)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Progreso:")
        self.progress_label.pack(anchor="w", padx=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        self.progress_bar.set(0)
    
    def create_input_field(self, parent, label_text, variable, row):
        """Crea un campo de entrada con etiqueta."""
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = ctk.CTkEntry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
    
    def create_center_panel(self):
        """Crea el panel central de visualización."""
        self.center_panel = ctk.CTkFrame(self.main_frame)
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Título
        title_label = ctk.CTkLabel(
            self.center_panel, 
            text="Visualización", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Frame para el gráfico
        self.plot_frame = ctk.CTkFrame(self.center_panel)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la simulación actual
        self.info_frame = ctk.CTkFrame(self.center_panel)
        self.info_frame.pack(fill="x", padx=10, pady=10)
        
        self.step_label = ctk.CTkLabel(self.info_frame, text="N° Paso Actual: -")
        self.step_label.pack(anchor="w", padx=5)
        
        self.position_label = ctk.CTkLabel(self.info_frame, text="Posición Actual: -")
        self.position_label.pack(anchor="w", padx=5)
        
        self.distance_label = ctk.CTkLabel(self.info_frame, text="Distancia al Origen Actual: -")
        self.distance_label.pack(anchor="w", padx=5)
        
        self.keys_label = ctk.CTkLabel(self.info_frame, text="Llaves Encontradas: -")
        self.keys_label.pack(anchor="w", padx=5)
    
    def create_right_panel(self):
        """Crea el panel derecho de resultados."""
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Título
        title_label = ctk.CTkLabel(
            self.right_panel, 
            text="Resultados", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Frame de resultados numéricos
        self.results_frame = ctk.CTkFrame(self.right_panel)
        self.results_frame.pack(fill="x", padx=10, pady=10)
        
        # Labels de resultados
        self.prob_dist_2_label = ctk.CTkLabel(
            self.results_frame, 
            text="P(D=2): -"
        )
        self.prob_dist_2_label.pack(anchor="w", padx=5, pady=2)
        
        self.prob_keys_label = ctk.CTkLabel(
            self.results_frame, 
            text="P(Encontrar Llaves): -"
        )
        self.prob_keys_label.pack(anchor="w", padx=5, pady=2)
        
        self.avg_dist_label = ctk.CTkLabel(
            self.results_frame, 
            text="Distancia Promedio al Origen: -"
        )
        self.avg_dist_label.pack(anchor="w", padx=5, pady=2)
        
        self.freq_pos_label = ctk.CTkLabel(
            self.results_frame, 
            text="Posición Más Frecuente: -"
        )
        self.freq_pos_label.pack(anchor="w", padx=5, pady=2)
        
        self.returns_label = ctk.CTkLabel(
            self.results_frame, 
            text="Retornos al Origen: -"
        )
        self.returns_label.pack(anchor="w", padx=5, pady=2)
        
        self.target_prob_label = ctk.CTkLabel(
            self.results_frame, 
            text="P(Terminar en Coordenada Objetivo): -"
        )
        self.target_prob_label.pack(anchor="w", padx=5, pady=2)
        
        # Frame de gráficos
        self.graphs_frame = ctk.CTkFrame(self.right_panel)
        self.graphs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de gráficos
        graph_buttons_frame = ctk.CTkFrame(self.graphs_frame)
        graph_buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(
            graph_buttons_frame, 
            text="Gráficos", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(5, 10))
        
        self.dist_graph_btn = ctk.CTkButton(
            graph_buttons_frame,
            text="Distribución Posiciones",
            command=self.show_distribution_graph,
            state="disabled"
        )
        self.dist_graph_btn.pack(fill="x", padx=5, pady=2)
        
        self.hist_graph_btn = ctk.CTkButton(
            graph_buttons_frame,
            text="Histograma Distancias",
            command=self.show_histogram_graph,
            state="disabled"
        )
        self.hist_graph_btn.pack(fill="x", padx=5, pady=2)
        
        self.conv_graph_btn = ctk.CTkButton(
            graph_buttons_frame,
            text="Convergencia Monte Carlo",
            command=self.show_convergence_graph,
            state="disabled"
        )
        self.conv_graph_btn.pack(fill="x", padx=5, pady=2)
        
        self.heatmap_btn = ctk.CTkButton(
            graph_buttons_frame,
            text="Mapa de Calor",
            command=self.show_heatmap,
            state="disabled"
        )
        self.heatmap_btn.pack(fill="x", padx=5, pady=2)
    
    def get_simulation_params(self) -> Tuple[int, Tuple[int, int], Optional[int]]:
        """
        Obtiene los parámetros de simulación de la interfaz.
        
        Returns:
            Tupla con (steps, keys_position, seed)
        """
        try:
            steps_str = self.steps_var.get()
            keys_x_str = self.keys_x_var.get()
            keys_y_str = self.keys_y_var.get()
            num_sim_str = self.num_simulations_var.get()
            seed_str = self.seed_var.get()
            
            # Validar que los campos no estén vacíos
            if not steps_str or not keys_x_str or not keys_y_str or not num_sim_str:
                messagebox.showerror("Error", "Todos los campos numéricos deben tener un valor")
                raise ValueError("Empty field")
            
            steps = int(steps_str)
            keys_x = int(keys_x_str)
            keys_y = int(keys_y_str)
            seed = int(seed_str) if seed_str else None
            
            # Validar que la semilla sea no negativa
            if seed is not None and seed < 0:
                messagebox.showerror("Error", "La semilla debe ser un número entero no negativo")
                raise ValueError("Seed must be non-negative")
            
            return steps, (keys_x, keys_y), seed
        except ValueError as e:
            if "Empty field" not in str(e):
                messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            raise
    
    def run_single_simulation(self):
        """Ejecuta una simulación individual con animación."""
        try:
            steps, keys_position, seed = self.get_simulation_params()
            
            # Reiniciar simulador con semilla si se proporcionó
            if seed is not None:
                self.simulator = RandomWalkSimulation(seed)
            
            # Ejecutar simulación
            self.current_result = self.simulator.simulate_single(steps, keys_position)
            
            # Animar la simulación
            self.animate_simulation()
            
        except ValueError:
            pass
    
    def animate_simulation(self):
        """Anima la simulación paso a paso."""
        if not self.current_result:
            return
        
        # Configurar velocidad
        speed_map = {"lenta": 1000, "media": 500, "rápida": 200}
        interval = speed_map.get(self.speed_var.get(), 500)
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear figura matplotlib
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Configurar gráfico
        x_coords = [pos[0] for pos in self.current_result.path]
        y_coords = [pos[1] for pos in self.current_result.path]
        
        keys_x = int(self.keys_x_var.get())
        keys_y = int(self.keys_y_var.get())
        all_x = x_coords + [keys_x]
        all_y = y_coords + [keys_y]
        max_range = max(max(abs(x) for x in all_x), max(abs(y) for y in all_y)) + 2
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_aspect('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Simulación Individual')
        
        # Elementos estáticos
        ax.plot(0, 0, 'go', markersize=12, label='Origen', zorder=5)
        ax.plot(keys_x, keys_y, 'y*', 
               markersize=15, label='Llaves', zorder=5)
        
        # Elementos dinámicos
        line, = ax.plot([], [], 'b-', linewidth=2, alpha=0.7, label='Trayectoria')
        point, = ax.plot([], [], 'ro', markersize=10, label='Posición Actual', zorder=5)
        ax.legend(loc='upper right')
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Animar
        self.animation_running = True
        self.animate_step(0, x_coords, y_coords, line, point, canvas, interval)
    
    def animate_step(self, step, x_coords, y_coords, line, point, canvas, interval):
        """Ejecuta un paso de la animación."""
        if not self.animation_running or step >= len(x_coords):
            self.animation_running = False
            return
        
        # Actualizar trayectoria
        line.set_data(x_coords[:step+1], y_coords[:step+1])
        
        # Actualizar posición actual
        point.set_data([x_coords[step]], [y_coords[step]])
        
        # Actualizar información
        current_pos = self.current_result.path[step]
        distance = abs(current_pos[0]) + abs(current_pos[1])
        
        self.step_label.configure(text=f"Paso: {step}")
        self.position_label.configure(text=f"Posición: {current_pos}")
        self.distance_label.configure(text=f"Distancia: {distance}")
        
        found = "Sí" if self.current_result.found_keys and step >= self.current_result.steps_to_keys else "No"
        self.keys_label.configure(text=f"Llaves: {found}")
        
        canvas.draw()
        
        # Programar siguiente paso
        self.after(interval, lambda: self.animate_step(
            step + 1, x_coords, y_coords, line, point, canvas, interval
        ))
    
    def run_monte_carlo(self, num_simulations: Optional[int] = None):
        """Ejecuta simulaciones Monte Carlo en un hilo separado."""
        try:
            steps, keys_position, seed = self.get_simulation_params()
            
            if num_simulations is None:
                num_sim_str = self.num_simulations_var.get()
                if not num_sim_str:
                    messagebox.showerror("Error", "La cantidad de simulaciones debe tener un valor")
                    return
                num_simulations = int(num_sim_str)
            
            # Deshabilitar botones durante simulación
            self.disable_buttons()
            
            # Reiniciar simulador con semilla si se proporcionó
            if seed is not None:
                self.simulator = RandomWalkSimulation(seed)
            
            # Crear hilo para simulación
            self.simulation_thread = threading.Thread(
                target=self._run_monte_carlo_thread,
                args=(steps, num_simulations, keys_position)
            )
            self.simulation_thread.start()
            
        except ValueError:
            self.enable_buttons()
    
    def _run_monte_carlo_thread(self, steps, num_simulations, keys_position):
        """Ejecuta las simulaciones Monte Carlo en un hilo separado."""
        def progress_callback(current, total):
            progress = current / total
            self.after(0, lambda: self.progress_bar.set(progress))
            self.after(0, lambda: self.progress_label.configure(
                text=f"Progreso: {current}/{total}"
            ))
        
        results = self.simulator.simulate_monte_carlo(
            steps, num_simulations, keys_position, progress_callback
        )
        
        # Actualizar UI en el hilo principal
        self.after(0, lambda: self._update_monte_carlo_results(results))
    
    def _update_monte_carlo_results(self, results):
        """Actualiza la UI con los resultados de Monte Carlo."""
        self.current_stats = MonteCarloStatistics(results)
        
        # Obtener estadísticas
        summary = self.current_stats.get_summary()
        
        # Actualizar labels
        self.prob_dist_2_label.configure(
            text=f"P(D=2): {summary['prob_distance_2']:.4f}"
        )
        self.prob_keys_label.configure(
            text=f"P(Encontrar Llaves): {summary['prob_find_keys']:.4f}"
        )
        self.avg_dist_label.configure(
            text=f"Distancia Promedio al Origen: {summary['avg_distance']:.2f}"
        )
        self.freq_pos_label.configure(
            text=f"Posición Más Frecuente: {summary['most_frequent_position']}"
        )
        self.returns_label.configure(
            text=f"Retornos al Origen: {summary['total_returns_origin']}"
        )
        
        # Habilitar botones
        self.enable_buttons()
        self.export_btn.configure(state="normal")
        self.dist_graph_btn.configure(state="normal")
        self.hist_graph_btn.configure(state="normal")
        self.conv_graph_btn.configure(state="normal")
        self.heatmap_btn.configure(state="normal")
        
        # Resetear barra de progreso
        self.progress_bar.set(0)
        self.progress_label.configure(text="Progreso:")
    
    def calculate_position_probability(self):
        """Calcula la probabilidad de terminar en una coordenada específica."""
        if not self.current_stats:
            messagebox.showwarning("Advertencia", "Ejecute primero Monte Carlo")
            return
        
        try:
            target_x_str = self.target_x_var.get()
            target_y_str = self.target_y_var.get()
            
            if not target_x_str or not target_y_str:
                messagebox.showerror("Error", "Las coordenadas objetivo deben tener un valor")
                return
            
            target_x = int(target_x_str)
            target_y = int(target_y_str)
            target_position = (target_x, target_y)
            
            prob = self.current_stats.calculate_position_probability(target_position)
            
            self.target_prob_label.configure(
                text=f"P(Terminar en {target_position}): {prob:.6f}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Coordenadas inválidas")
    
    def generate_random_run(self):
        """Genera una corrida aleatoria rápida."""
        try:
            steps, keys_position, _ = self.get_simulation_params()
            
            # Ejecutar simulación sin animación
            self.current_result = self.simulator.simulate_single(steps, keys_position)
            
            # Mostrar resultado estático
            self.show_static_result()
            
        except ValueError:
            pass
    
    def show_static_result(self):
        """Muestra el resultado de una simulación de forma estática."""
        if not self.current_result:
            return
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico
        fig = self.visualizer.plot_single_simulation(
            self.current_result,
            (int(self.keys_x_var.get()), int(self.keys_y_var.get()))
        )
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Actualizar información
        final_pos = self.current_result.final_position
        distance = abs(final_pos[0]) + abs(final_pos[1])
        
        self.step_label.configure(text=f"Paso: {len(self.current_result.path) - 1}")
        self.position_label.configure(text=f"Posición: {final_pos}")
        self.distance_label.configure(text=f"Distancia: {distance}")
        
        found = "Sí" if self.current_result.found_keys else "No"
        self.keys_label.configure(text=f"Llaves: {found}")
    
    def show_distribution_graph(self):
        """Muestra el gráfico de distribución de posiciones finales."""
        if not self.current_stats:
            return
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico
        fig = self.visualizer.plot_final_positions_distribution(self.current_stats)
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def show_histogram_graph(self):
        """Muestra el histograma de distancias finales."""
        if not self.current_stats:
            return
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico
        fig = self.visualizer.plot_distance_histogram(self.current_stats)
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def show_convergence_graph(self):
        """Muestra el gráfico de convergencia Monte Carlo."""
        if not self.current_stats:
            return
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico
        fig = self.visualizer.plot_convergence(self.current_stats)
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def show_heatmap(self):
        """Muestra el mapa de calor de posiciones finales."""
        if not self.current_stats:
            return
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear gráfico
        fig = self.visualizer.plot_heatmap(self.current_stats)
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def export_csv(self):
        """Exporta los resultados a un archivo CSV."""
        if not self.current_stats:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_stats.export_to_csv(filename)
                messagebox.showinfo("Éxito", f"Resultados exportados a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def clear_all(self):
        """Limpia todos los resultados y gráficos."""
        # Detener animación si está corriendo
        self.animation_running = False
        
        # Limpiar variables
        self.current_result = None
        self.current_stats = None
        
        # Limpiar frame de gráfico
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Resetear labels
        self.step_label.configure(text="Paso: -")
        self.position_label.configure(text="Posición: -")
        self.distance_label.configure(text="Distancia: -")
        self.keys_label.configure(text="Llaves: -")
        
        self.prob_dist_2_label.configure(text="P(D=2): -")
        self.prob_keys_label.configure(text="P(Encontrar Llaves): -")
        self.avg_dist_label.configure(text="Distancia Promedio al Origen: -")
        self.freq_pos_label.configure(text="Posición Más Frecuente: -")
        self.returns_label.configure(text="Retornos al Origen: -")
        self.target_prob_label.configure(text="P(Terminar en Coordenada Objetivo): -")
        
        # Resetear barra de progreso
        self.progress_bar.set(0)
        self.progress_label.configure(text="Progreso:")
        
        # Deshabilitar botones
        self.export_btn.configure(state="disabled")
        self.dist_graph_btn.configure(state="disabled")
        self.hist_graph_btn.configure(state="disabled")
        self.conv_graph_btn.configure(state="disabled")
        self.heatmap_btn.configure(state="disabled")
    
    def disable_buttons(self):
        """Deshabilita los botones durante la simulación."""
        self.run_single_btn.configure(state="disabled")
        self.run_monte_carlo_btn.configure(state="disabled")
        self.calc_prob_btn.configure(state="disabled")
        self.random_run_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
    
    def enable_buttons(self):
        """Habilita los botones después de la simulación."""
        self.run_single_btn.configure(state="normal")
        self.run_monte_carlo_btn.configure(state="normal")
        self.calc_prob_btn.configure(state="normal")
        self.random_run_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación limpiando recursos."""
        # Detener animación si está corriendo
        self.animation_running = False
        
        # Forzar cierre sin esperar callbacks pendientes
        self.quit()
        self.destroy()
