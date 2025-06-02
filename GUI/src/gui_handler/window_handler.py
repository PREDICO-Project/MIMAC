from typing import Any, List, Dict, Tuple, Optional
import tkinter as tk


class WINDOWHandler:
    """
    Clase para manejar la configuración y manipulación de ventanas en Tkinter.

    Esta clase proporciona métodos estáticos para posicionar, ajustar y maximizar ventanas en la interfaz de usuario de Tkinter.
    """

    @staticmethod
    def config_grid(frame: Any, rows: int, columns: int,
                   exp_rows: bool = True, exp_columns: bool = True) -> None:
        """
        Configura el grid layout de un frame, estableciendo el peso de las filas y columnas.

        Args:
            frame (Any): Frame de Tkinter cuyo grid layout se configurará.
            rows (int): Número de filas en el grid.
            columns (int): Número de columnas en el grid.
            exp_rows (bool, optional): Si es True, las filas se expanden proporcionalmente. Por defecto es True.
            exp_columns (bool, optional): Si es True, las columnas se expanden proporcionalmente. Por defecto es True.
        Version:
            1.0.0

        Last Modified:
            2024-12-05
        """
        for i in range(columns):
            weight = 1 if exp_columns else 0
            frame.grid_columnconfigure(i, weight=weight)

        for j in range(rows):
            weight = 1 if exp_rows else 0
            frame.grid_rowconfigure(j, weight=weight)
    
    @staticmethod
    def window_position(master: tk.Tk, x_pos: int, y_pos: int,
                       x_dim: Optional[int] = None, y_dim: Optional[int] = None) -> None:
        """
        Posiciona la ventana en la pantalla según las coordenadas proporcionadas.

        Calcula la posición de la ventana para centrarla en relación a la pantalla o a otros parámetros definidos.

        Args:
            master (tk.Tk): La ventana de Tkinter que se desea posicionar.
            x_pos (int): Factor para calcular la posición horizontal.
            y_pos (int): Factor para calcular la posición vertical.
            x_dim (Optional[int], optional): Ancho de la ventana. Si es None, usa el ancho actual. Por defecto es None.
            y_dim (Optional[int], optional): Alto de la ventana. Si es None, usa el alto actual. Por defecto es None.

        Version:
            1.0.0

        Last Modified:
            2024-12-05
        """
        master.update_idletasks()

        if x_dim is None:
            x_dim = master.winfo_width()
        if y_dim is None:
            y_dim = master.winfo_height()

        x = (master.winfo_screenwidth() // x_pos) - (x_dim // 2)
        y = (master.winfo_screenheight() // y_pos) - (y_dim // 2)
        master.geometry(f'{x_dim}x{y_dim}+{x}+{y}')

    @staticmethod
    def adjust_window_to_tab(master: tk.Tk, tab_frame: Any, button_frame: Any,
                             x_margin: int = 20, min_width: int = 700) -> None:
        """
        Ajusta el tamaño de la ventana según los tamaños requeridos por los widgets internos,
        asegurando un mínimo de ancho.

        Args:
            master (tk.Tk): La ventana de Tkinter que se desea ajustar.
            tab_frame (Any): Frame que contiene las pestañas (Notebook).
            button_frame (Any): Frame que contiene botones u otros widgets.
            x_margin (int, optional): Margen adicional para el ancho total. Por defecto es 20.
            min_width (int, optional): Ancho mínimo de la ventana. Por defecto es 700.

        Version:
            1.0.0

        Last Modified:
            2024-12-05
        """
        tab_frame.update_idletasks()
        button_frame.update_idletasks()

        tab_width = tab_frame.winfo_reqwidth()
        button_width = button_frame.winfo_reqwidth()
        total_width = tab_width + button_width + x_margin

        # Asegurarse de que el ancho total no sea menor que el ancho mínimo
        total_width = max(total_width, min_width)

        height = max(tab_frame.winfo_reqheight(),
                    button_frame.winfo_reqheight(), master.winfo_height())
        master.geometry(f'{total_width}x{height}')

    @staticmethod
    def maximizar_ventana(root: tk.Tk) -> None:
        """
        Maximiza la ventana principal. Funciona en Windows y ajusta el tamaño en otras plataformas.

        Args:
            root (tk.Tk): La ventana de Tkinter que se desea maximizar.

        Version:
            1.0.0

        Last Modified:
            2024-12-05
        """
        root.update()
        try:
            root.state('zoomed')  # Solo en Windows
        except:
            # Para otras plataformas, ajustar al tamaño de la pantalla
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.geometry(f'{screen_width-10}x{screen_height-10}+0+0')
    
    @staticmethod
    def centrar_ventana(master: tk.Tk) ->None:
        
        master.update_idletasks()  # Asegura que la geometría está actualizada
        width = master.winfo_width()
        height = master.winfo_height()

        # Si la ventana aún no ha sido renderizada, usa reqwidth/reqheight
        if width == 1 or height == 1:  
            width = master.winfo_reqwidth()
            height = master.winfo_reqheight()

        # Calcula la posición para centrar la ventana
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)

        master.geometry(f"{width}x{height}+{x}+{y}")