"""
Punto de entrada principal para el Simulador Juego EBRIO.

Este módulo inicializa y ejecuta la aplicación de simulación
de Random Walk bidimensional.
"""

import sys
import customtkinter as ctk
from ui import DrunkWalkApp


def main():
    """
    Función principal que inicia la aplicación.
    
    Configura CustomTkinter y crea la instancia principal
    de la aplicación DrunkWalkApp.
    """
    try:
        # Configurar CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear y ejecutar la aplicación
        app = DrunkWalkApp()
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
        sys.exit(0)
    except Exception as e:
        # Ignorar errores de Tkinter durante cierre (callbacks pendientes)
        if "invalid command name" in str(e) or "update" in str(e) or "check_dpi_scaling" in str(e):
            sys.exit(0)
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
