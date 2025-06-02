import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional, List, Tuple, Union
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AdvancedWidgets:
    """
    Clase para manejar la creación de widgets avanzados en Tkinter.

    Esta clase proporciona métodos estáticos para crear widgets más complejos y avanzados,
    que requieren configuraciones específicas y ofrecen funcionalidades adicionales
    en comparación con los widgets básicos. Los widgets avanzados permiten construir
    interfaces de usuario más interactivas y ricas en características, facilitando
    la gestión y visualización de datos complejos.

    """

    ''' @staticmethod
    def create_treeview_panel(parent_frame: Any, title: str = "Tree View",
                              row: int = 0, column: int = 0) -> ttk.Treeview:
        """
        Crea un panel con un Treeview y un título en una posición específica dentro del grid.

        Args:
            parent_frame (Any): Frame donde se colocará el Treeview.
            title (str, optional): Título que identificará el contenido del Treeview. Por defecto es "Tree View".
            row (int, optional): Fila donde se colocará el panel. Por defecto es 0.
            column (int, optional): Columna donde se colocará el panel. Por defecto es 0.

        Returns:
            ttk.Treeview: Treeview creado dentro del panel.

        """
        # Crear un frame contenedor
        panel_frame = ttk.Frame(parent_frame)
        panel_frame.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

        # Etiqueta de título
        label = ttk.Label(panel_frame, text=title, font=("Arial", 10), anchor="center")
        label.pack(fill="x", pady=(5, 0))  # Margen superior para separar del contenido anterior

        # Treeview
        tree_view = ttk.Treeview(panel_frame)
        tree_view.pack(expand=True, fill='both', pady=(5, 5))  # Margen para separar del borde

        return tree_view'''
    @staticmethod
    def create_treeview_panel(parent_frame: Any,
                            title: str = "Tree View",
                            row: int = 0,
                            column: int = 0,
                            *,
                            width_px: int = None,
                            height_px: int = None
                            ) -> ttk.Treeview:
        """
        Crea un panel con un Treeview y un título, fijando su tamaño en píxeles.

        Args:
            parent_frame (Any): Frame donde se colocará el Treeview.
            title (str, optional): Título del panel. Por defecto "Tree View".
            row (int, optional): Fila del grid. Por defecto 0.
            column (int, optional): Columna del grid. Por defecto 0.

        Keyword Args:
            width_px (int, optional): ancho del panel en píxeles.
            height_px (int, optional): alto del panel en píxeles.

        Returns:
            ttk.Treeview: Treeview creado dentro del panel.
        """
        # Frame contenedor
        panel_frame = ttk.Frame(parent_frame)
        panel_frame.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

        # Fijamos tamaño en píxeles y bloqueamos propagate
        if width_px is not None or height_px is not None:
            if width_px is not None:
                panel_frame.config(width=width_px)
            if height_px is not None:
                panel_frame.config(height=height_px)
            panel_frame.grid_propagate(False)

        # Título
        label = ttk.Label(panel_frame, text=title, font=("Arial", 10), anchor="center")
        label.grid(row=0, column=0, sticky="w", pady=(5, 0))

        # Treeview sin controlar filas visibles ni columnas
        tree_view = ttk.Treeview(panel_frame, show='headings')
        tree_view.grid(row=1, column=0, sticky="nsew", pady=(5, 5))

        # Para que el Treeview ocupe todo el panel
        panel_frame.rowconfigure(1, weight=1)
        panel_frame.columnconfigure(0, weight=1)

        return tree_view

    @staticmethod
    def create_notebook(parent_frame: Any, tabs: Optional[List[Tuple[str, Any]]] = None,
                        row: int = 0, column: int = 0, padx: int = 5, pady: int = 5) -> ttk.Notebook:
        """
        Crea un widget Notebook con pestañas en una posición específica dentro del grid.

        Args:
            parent_frame (Any): Frame donde se colocará el Notebook.
            tabs (Optional[List[Tuple[str, Any]]], optional): Lista de tuplas que contienen el título de la pestaña y el contenido (Frame)
                que se colocará dentro de cada pestaña. Por defecto es None.
            row (int, optional): Fila donde se colocará el Notebook. Por defecto es 0.
            column (int, optional): Columna donde se colocará el Notebook. Por defecto es 0.
            padx (int, optional): Padding en el eje x. Por defecto es 5.
            pady (int, optional): Padding en el eje y. Por defecto es 5.

        Returns:
            ttk.Notebook: Notebook creado con las pestañas especificadas.
        """
        notebook = ttk.Notebook(parent_frame)
        notebook.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")

        if tabs:
            for tab_title, tab_content in tabs:
                notebook.add(tab_content, text=tab_title)

        return notebook

    @staticmethod
    def create_empty_notebook(parent_frame: Any, 
                            tabs_config: List[Dict[str, str]], 
                            notebook_padding: tuple = (5, 5)
                            ) -> Tuple[ttk.Notebook, Dict[str, ttk.Frame]]:
        """
        Crea un Notebook vacío con pestañas dentro de un frame.

        Args:
            parent_frame (Any): Frame donde se colocará el Notebook.
            tabs_config (List[Dict[str, str]]): Lista con la configuración de las pestañas.
            notebook_padding (tuple, optional): Padding del Notebook. Por defecto (5,5).

        Returns:
            Tuple[ttk.Notebook, Dict[str, ttk.Frame]]: 
                - El Notebook creado con pestañas vacías.
                - Diccionario con los Frames de cada pestaña.
        """

        # Asegurar que el parent_frame se expanda completamente
        parent_frame.rowconfigure(0, weight=1)
        parent_frame.columnconfigure(0, weight=1)

        # Crear el Notebook dentro del parent_frame
        notebook = ttk.Notebook(parent_frame)
        notebook.grid(row=0, column=0, sticky="nsew", padx=notebook_padding[0], pady=notebook_padding[1])

        #notebook.pack(fill=tk.BOTH, expand=True, padx=notebook_padding[0], pady=notebook_padding[1])

        # Diccionario para almacenar referencias a los frames de las pestañas
        tab_frames = {}

        # Crear las pestañas vacías
        for tab_cfg in tabs_config:
            tab_title = tab_cfg.get("tab_title", "Untitled Tab")

            # Crear un Frame vacío dentro del Notebook
            tab_frame = ttk.Frame(notebook)
            tab_frame.pack(fill=tk.BOTH, expand=True)  # IMPORTANTE

            # Agregar la pestaña al Notebook
            notebook.add(tab_frame, text=tab_title)

            # Guardar la referencia del frame en el diccionario
            tab_frames[tab_title] = tab_frame

            #print(f"Se ha creado la pestaña: {tab_title}")  # Debug

        return notebook, tab_frames

    @staticmethod
    def embed_matplotlib_graph(parent_frame: Any, figure: Any, row: int = 0, column: int = 0,
                              padx: int = 5, pady: int = 5) -> Any:
        """
        Incrusta un gráfico de Matplotlib dentro de una interfaz de Tkinter.

        Args:
            parent_frame (Any): Frame donde se colocará el gráfico.
            figure (Any): Objeto Figure de Matplotlib a incrustar.
            row (int, optional): Fila donde se colocará el gráfico. Por defecto es 0.
            column (int, optional): Columna donde se colocará el gráfico. Por defecto es 0.
            padx (int, optional): Padding en el eje x. Por defecto es 5.
            pady (int, optional): Padding en el eje y. Por defecto es 5.

        Returns:
            Any: Objeto Canvas de Matplotlib incrustado en Tkinter.

        Version:
            1.0.0

        Last Modified:
            2024-12-05
        """
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        canvas = FigureCanvasTkAgg(figure, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")
        return canvas

    @staticmethod
    def create_scrollable_canvas(parent, row, column, label_text, update_canvas_slice=None):
        # Frame principal
        frame = ttk.Frame(parent, padding=10)
        frame.grid(row=row, column=column, sticky='nsew')
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(column, weight=1)

        # Label superior
        label = ttk.Label(
            frame,
            text=label_text,
            font=("Arial", 12, "bold")
        )
        label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        # Separador simple
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Frame para el canvas
        canvas_frame = ttk.Frame(frame)
        canvas_frame.grid(row=2, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Canvas con fondo gris corporativo
        canvas = tk.Canvas(
            canvas_frame,
            bg="#2e2e2e",
            highlightthickness=1,
            highlightbackground="#aaaaaa"
        )
        canvas.pack(expand=True, fill="both")

        # Scale vertical de tk (muestra el valor automáticamente)
        scale = tk.Scale(
            frame,
            from_=0,
            to=1,
            orient="vertical",
            command=lambda value, c=canvas: update_canvas_slice(c, int(float(value))) if update_canvas_slice else None
        )
        scale.grid(row=2, column=1, sticky="ns", padx=(10, 0))

        return canvas, scale 
    
    @staticmethod
    def create_canvas(parent, row, column, label_text):

        canvas_frame = ttk.Frame(parent)
        canvas_frame.grid(row=row, column=column, sticky="nsew")
        
        canvas = tk.Canvas(
            canvas_frame,
            bg="#2e2e2e",
            highlightthickness=1,
            highlightbackground="#aaaaaa"
        )
        canvas.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(1, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        #canvas.pack(expand=True, fill="both")
        
        return canvas
            