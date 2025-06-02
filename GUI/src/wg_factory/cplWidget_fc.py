import tkinter as tk
from typing import Any, List, Dict, Tuple, Optional
from tkinter import ttk
from src.wg_factory.widget_fc import WIDGETFactory as wgf
from src.wg_factory.adWidget_fc import AdvancedWidgets as awgf
from src.tool_handler.path_handler import PATHHandler as path

class COMPLEXWIDGETFactory():

    ####################
    # Métodos Internos #
    ####################
    @staticmethod
    def _configure_grid(root: Any, rows: int, columns: int) -> None:
        """Configura las filas y columnas de un contenedor con pesos uniformes."""
        for r in range(rows):
            root.rowconfigure(r, weight=1)
        for c in range(columns):
            root.columnconfigure(c, weight=1)
    
    ####################
    # Métodos Externos #
    ####################
        
    @staticmethod
    def populate_control_panel(
        root: Any,
        list_cfg: List[Dict[str, Any]],
        horizontal: bool = False,
        pos_in_frame: Optional[Tuple[int, int]] = (0, 0),
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Dict[str, Dict[str, Any]]:
        """
        Crea un panel dinámico basado en una configuración que puede incluir botones, separadores, imágenes y espacios vacíos.

        Args:
            root (Any): El objeto raíz donde se agregarán los elementos.
            list_cfg (List[Dict[str, Any]]): Lista de configuraciones para los elementos.
            horizontal (bool): Si True, organiza los elementos horizontalmente. Por defecto, False.
            pos_in_frame (Optional[Tuple[int, int]]): Posición inicial en el frame (fila, columna). Por defecto, (0, 0).
            default_padding (Tuple[int, int]): Espaciado predeterminado (padx, pady). Por defecto, (5, 5).

        Returns:
            Dict[str, Dict[str, Any]]: Diccionario con los elementos creados categorizados (botones, etiquetas, imágenes).
        """
        elements = {
            "button": {}, "label": {}, "image": {}, 
            "label_combobox": {}, "label_entry": {}, "check_box_label": {}, "radiobutton": {},
            "treeview":{}
        }
        current_row, current_column = pos_in_frame
        column_tracker = {}  # Diccionario para hacer seguimiento de filas por columna
        padx, pady = default_padding

        for config in list_cfg:
            column = config.get("column", current_column)  # Obtiene la columna si se especifica
            
            mergecolumns = config.get("mergecolumns", 1)  # Permite definir cuántas columnas ocupa (por defecto 1)

            # Asegurar que todas las columnas tengan un índice de fila en column_tracker
            for col in range(column, column + mergecolumns):
                if col not in column_tracker:
                    column_tracker[col] = current_row

            row_conse = max(column_tracker[col] for col in range(column, column + mergecolumns))  # Tomar la fila más alta
            row = config.get("row", row_conse) # Obtiene la fila si se especifica

            if "separator" in config and config["separator"]:
                separator = ttk.Separator(root, orient="horizontal" if not horizontal else "vertical")
                separator.grid(row=row, column=column, columnspan=mergecolumns, sticky="ns" if horizontal else "ew", padx=padx, pady=pady)

            elif "image" in config:
                label_with_image = wgf.create_label_with_image(
                    master=root,
                    image_path=path.resource_path(config['image']),
                    row=row,
                    column=column,
                    sticky=config.get('sticky','w'),
                    img_sizeX = config.get('img_sizeX', 150),
                    img_sizeY = config.get('img_sizeY', 150),
                    columnspan = config.get('columnspan', 1),
                    rowspan = config.get('rowspan', 1),
                )
                elements["image"][f"image_{row}_{column}"] = label_with_image

            elif "space" in config and config["space"]:
                space_label = wgf.create_label(
                    master=root,
                    text='',
                    row=row,
                    column=column,
                    padx=padx,
                    pady=pady
                )

            elif 'button' in config:
                button = wgf.create_button(
                    master=root,
                    button_text=config["button"],
                    row=row,
                    column=column,
                    command=config.get("command",None),
                    sticky=config.get('sticky', 'ew'),
                    padx=config.get('padx', padx),
                    pady=config.get('pady', pady),
                    state=config.get("state", "normal"),
                    width=config.get("width", None),
                )
                elements["button"][config["button"]] = button

            elif 'label' in config:

                # Verificar si el elemento debe mostrarse
                if config.get('show', True) is False:
                    continue  # No crear este elemento

                label = wgf.create_label(
                    master=root,
                    text=config['label'],
                    row=row,
                    column=column,
                    text_size=config.get('text_size', 10),
                    colorText=config.get('colorText', ''),
                    sticky=config.get('sticky', 'w'),
                    bold=config.get('bold', False),
                    text_align=config.get('text_align', 'left')
                )
                label.grid(columnspan=mergecolumns)  # Aplicar fusión de columnas si está especificado
                elements["label"][config["label"]] = label
            
            elif 'treeview' in config:

                treeview = awgf.create_treeview_panel(
                        parent_frame=root,
                        title=config['treeview'],
                        row=row,
                        column=column,
                        width_px=config.get('width', 200),
                        height_px=config.get('height', 200),
                    )
                 
                # Aplicar mergecolumns en el frame contenedor
                panel_frame = treeview.master
                panel_frame.grid_configure(columnspan=mergecolumns)
                 
                elements["treeview"][config['treeview']] = treeview

            elif 'label_combobox' in config:
                _, CbANDlabel = wgf.create_label_combobox(
                    master=root,
                    label_text=config['label_combobox'],
                    names=config.get('names', None),
                    row=row,
                    column=column,
                    sticky=config.get('sticky', 'w'),
                    horizontal=config.get('horizontal', True),
                    combobox_width=config.get('combobox_width', None),
                    callback=config.get('action', None)
                )
                elements["label_combobox"][config["label_combobox"]] = CbANDlabel
                if config['horizontal'] is not True:
                    row += 1  # Si no es horizontal, pasamos a la siguiente fila
            
            elif 'label_entry' in config:
                _, labelANDentry = wgf.create_label_entry(
                    master=root,
                    label_text=config['label_entry'],
                    row=row,
                    column=column,
                    width_entry=config.get('width_entry', 20),
                    vertical=config['vertical']
                )
                elements["label_entry"][config["label_entry"]] = labelANDentry

            elif 'check_box_label' in config:
                checkBoxVar = tk.BooleanVar()
                checkBoxVar.set(bool(config.get('check', False)))
                _, checkBox = wgf.create_label_checkbox(
                    master=root,
                    label_text=config['check_box_label'],
                    checkbox_text=config['check_box_text'],
                    row=row,
                    column=column,
                    horizontal=True,
                    variable=checkBoxVar,
                    padx=default_padding[0],
                    pady=default_padding[1]
                )
                elements["check_box_label"][config["check_box_label"]] = checkBox

            elif 'radiobutton' in config:
                
                radio_button = wgf.create_radiobutton(
                    master=root,
                    text=config['radiobutton'],
                    row=row,
                    column=column,
                    variable=config['variable'],
                    value=config['value'],
                    padx=padx,
                    pady=pady
                )
                elements["radiobutton"][config["radiobutton"]] = radio_button

            # Actualizar la fila para TODAS las columnas afectadas por mergecolumns
            new_row_value = row + 1
            for col in range(column, column + mergecolumns):
                column_tracker[col] = new_row_value

        root.update_idletasks()
        
        return elements

    @staticmethod
    def populate_frame_WITH_frames(
        root: Any,
        panels_config: List[Dict[str, Any]],
    ) -> Tuple[List[Any], Dict[str, Any]]:
        """
        Crea frames y los llena con elementos definidos en `panels_config`.

        Args:
            root (Any): Contenedor raíz donde se agregarán los frames.
            panels_config (List[Dict[str, Any]]): Configuración de los paneles.

        Returns:
            Tuple[List[Any], Dict[str, Any]]: 
                - Lista de todos los elementos creados.
                - Diccionario con los nombres de los paneles como claves y sus frames como valores.
        """
        panel_frames = {}  # Diccionario para almacenar los paneles por nombre
        elements = []      # Lista para almacenar todos los elementos creados

        for panel_cfg in panels_config:
            # Crear un frame para cada panel
            panel_frame = ttk.Frame(root)
            panel_frame.grid(
                row=panel_cfg['panel_pos']['row'],
                column=panel_cfg['panel_pos']['col'],
                sticky="nsew"
            )

            # Crear los elementos dentro del frame utilizando COMPLEXWIDGETFactory
            elements_to_add = COMPLEXWIDGETFactory.populate_buttons_panel(panel_frame, panel_cfg['buttons_cfg'], horizontal=False)
            elements.extend(elements_to_add)  # Agregar elementos a la lista principal

            # Asociar el nombre del panel con el frame creado
            panel_frames[panel_cfg['name']] = panel_frame

        return elements, panel_frames
    
    @staticmethod
    def populate_frame_WITH_notebook(
        parent_frame: Any,
        tabs_config: List[Dict[str, Any]],
        notebook_position: Tuple[int, int] = (0, 0),
        notebook_padding: Tuple[int, int] = (5, 5),
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Tuple[ttk.Notebook, Dict[str, Any]]:
        """
        Crea un Notebook y lo rellena con pestañas que contienen **solo un tipo de elemento** (Treeview o Frame vacío).

        Args:
            parent_frame (Any): Frame donde se colocará el Notebook.
            tabs_config (List[Dict[str, Any]]): Configuración de cada pestaña.
            notebook_position (Tuple[int, int], optional): Posición en la cuadrícula (fila, columna). Por defecto (0,0).
            notebook_padding (Tuple[int, int], optional): Padding del Notebook. Por defecto (5,5).
            default_padding (Tuple[int, int], optional): Padding entre elementos. Por defecto (5,5).

        Returns:
            Tuple[ttk.Notebook, Dict[str, Any]]:
                - `ttk.Notebook`: El Notebook creado.
                - `Dict[str, Any]`: Diccionario con los elementos creados en cada pestaña.
        """

        # Configurar el estilo de las pestañas a la izquierda
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[5, 2], anchor="w")  

        # Configurar el parent_frame
        parent_frame.rowconfigure(notebook_position[0], weight=1)
        parent_frame.columnconfigure(notebook_position[1], weight=1)

        # Crear el Notebook
        row, column = notebook_position
        padx, pady = notebook_padding
        notebook = awgf.create_notebook(
            parent_frame=parent_frame,
            tabs=None,
            row=row,
            column=column,
            padx=padx,
            pady=pady,
        )

        # Asegurar que el notebook esté en la columna 0 (izquierda)
        notebook.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)

        # Diccionario para almacenar los elementos creados
        elements_dict = {}

        # Iterar sobre la configuración de las pestañas
        for tab_cfg in tabs_config:
            tab_title = tab_cfg.get("tab_title", "Untitled Tab")
            grid = tab_cfg.get("grid", [1, 1])
            elements_config = tab_cfg.get("elements", [])

            # Verificar qué tipo de elementos hay en la pestaña
            if not elements_config:
                continue  # Si no hay elementos, no creamos la pestaña

            first_element = elements_config[0]  # Solo tomamos el primer elemento
            element_type = first_element.get("type", "")
            element_title = first_element.get("element_title", "")

            # Crear el Frame contenedor para la pestaña
            tab_frame = ttk.Frame(notebook)
            tab_frame.grid(row=0, column=0, sticky="nsew")
            tab_frame.rowconfigure(0, weight=1)
            tab_frame.columnconfigure(0, weight=1)

            if element_type == "treeview":
                # Crear un Treeview en la pestaña
                elements = COMPLEXWIDGETFactory.populate_treeview_panels_moviles(
                    root=tab_frame,
                    grid=tuple(grid),
                    treeview_configs=[{"title": element_title}],
                    default_padding=default_padding,
                )
                elements_dict[tab_title] = elements

            elif element_type == "frame":
                # Crear un Frame vacío en la pestaña
                frame = ttk.Frame(tab_frame)
                frame.grid(row=0, column=0, sticky="nsew", padx=default_padding[0], pady=default_padding[1])
                elements_dict[tab_title] = frame

            # Agregar la pestaña al Notebook
            notebook.add(tab_frame, text=tab_title)

        return notebook, elements_dict
    
    @staticmethod
    def populate_treeview_panels_fijos(
        root: Any,
        num_panels: int,
        grid: Tuple[int, int],
        treeview_configs: Optional[List[Dict[str, Any]]] = None,
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Dict[str, ttk.Treeview]:
        """
        Crea y organiza múltiples TreeView panels en un frame utilizando `create_treeview_panel`.

        Args:
            root (Any): El objeto raíz donde se agregarán los TreeView panels.
            num_panels (int): Número total de TreeView panels a crear.
            grid (Tuple[int, int]): Número de filas y columnas para organizar los TreeView panels.
            treeview_configs (Optional[List[Dict[str, Any]]], optional): Lista de configuraciones para cada TreeView.
                Cada configuración puede incluir "title", etc. Si no se proporciona, se usa un valor predeterminado.
            default_padding (Tuple[int, int], optional): Espaciado predeterminado entre TreeView panels (padx, pady).

        Returns:
            Dict[str, ttk.Treeview]: Diccionario con los TreeView creados, identificados por sus títulos.
        """
        # Validar que grid es suficiente para num_panels
        rows, columns = grid
        if rows * columns < num_panels:
            raise ValueError("El grid proporcionado no tiene suficientes espacios para los TreeViews solicitados.")

        # Inicializar configuraciones si no se proporcionan
        if treeview_configs is None:
            treeview_configs = [{} for _ in range(num_panels)]
        elif len(treeview_configs) < num_panels:
            # Rellenar configuraciones faltantes
            treeview_configs += [{} for _ in range(num_panels - len(treeview_configs))]

        treeview_panels = {}
        padx, pady = default_padding

        # Configurar filas y columnas del root con pesos uniformes
        COMPLEXWIDGETFactory._configure_grid(root, rows, columns)

        current_panel = 0
        for r in range(rows):
            for c in range(columns):
                if current_panel >= num_panels:
                    break

                # Configuración del TreeView actual
                config = treeview_configs[current_panel]
                title = config.get("title", f"TreeView {current_panel + 1}")

                # Crear el TreeView panel usando `create_treeview_panel`
                tree_view = awgf.create_treeview_panel(
                    parent_frame=root,
                    title=title,
                    row=r,
                    column=c,
                    padding=(padx, pady),
                )

                # Guardar el TreeView en el diccionario usando el título como clave
                treeview_panels[title] = tree_view

                current_panel += 1

        return treeview_panels

    @staticmethod
    def populate_treeview_panels_moviles(
        root: Any,
        grid: Tuple[int, int],
        treeview_configs: List[Dict[str, Any]],
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Dict[str, ttk.Treeview]:
        """
        Crea y organiza múltiples TreeView panels en un PanedWindow ajustable en ambas dimensiones.

        Args:
            root (Any): El objeto raíz donde se agregarán los TreeView panels.
            grid (Tuple[int, int]): Número de filas y columnas para organizar los TreeView panels.
            treeview_configs (List[Dict[str, Any]]): Lista de configuraciones para cada TreeView.
                Cada configuración puede incluir "title", etc.
            default_padding (Tuple[int, int], optional): Espaciado predeterminado entre TreeView panels (padx, pady).

        Returns:
            Dict[str, ttk.Treeview]: Diccionario con los TreeView creados, identificados por sus títulos.
        """
        num_panels = len(treeview_configs)
        rows, columns = grid

        if rows * columns < num_panels:
            raise ValueError("El grid proporcionado no tiene suficientes espacios para los TreeViews solicitados.")

        treeview_panels = {}
        padx, pady = default_padding

        # Crear un PanedWindow principal con orientación vertical
        main_paned_window = ttk.PanedWindow(root, orient="vertical")
        main_paned_window.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        current_panel = 0

        # Crear filas como PanedWindows horizontales dentro del PanedWindow principal
        for r in range(rows):
            row_paned_window = ttk.PanedWindow(main_paned_window, orient="horizontal")
            main_paned_window.add(row_paned_window, weight=1)

            for c in range(columns):
                if current_panel >= num_panels:
                    break

                # Configuración del TreeView actual
                config = treeview_configs[current_panel]
                title = config.get("title", f"TreeView {current_panel + 1}")

                # Crear un frame para cada TreeView
                frame = ttk.Frame(row_paned_window)
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # Crear el TreeView en el frame
                tree_view = awgf.create_treeview_panel(
                    parent_frame=frame,
                    title=title,
                    row=0,
                    column=0,
                )

                # Agregar el frame al PanedWindow horizontal
                row_paned_window.add(frame, weight=1)

                # Guardar el TreeView en el diccionario usando el título como clave
                treeview_panels[title] = tree_view

                current_panel += 1

        return treeview_panels

    @staticmethod
    def populate_elements_panels(
        root: Any,
        grid: Tuple[int, int],
        element_configs: List[Dict[str, Any]],
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Dict[str, Any]:
        """
        Crea y organiza múltiples elementos (TreeView, gráficos o Scrollable Canvas) en un PanedWindow.

        Args:
            root (Any): El objeto raíz donde se agregarán los elementos.
            grid (Tuple[int, int]): Número de filas y columnas para organizar los elementos.
            element_configs (List[Dict[str, Any]]): Lista de configuraciones para cada elemento.
                Cada configuración puede incluir "type" (treeview, graph o scrollable_canvas), "title", etc.
            default_padding (Tuple[int, int], optional): Espaciado predeterminado entre elementos (padx, pady).

        Returns:
            Dict[str, Any]: Diccionario con los elementos creados, identificados por sus títulos.
        """
        num_panels = len(element_configs)

        rows, columns = grid
        if rows * columns < num_panels:
            raise ValueError("El grid proporcionado no tiene suficientes espacios para los elementos solicitados.")

        elements_panels = {}
        padx, pady = default_padding
        current_panel = 0

        for r in range(rows):
            root.rowconfigure(r, weight=1)

        for r in range(rows):
            paned_window = ttk.PanedWindow(root, orient="horizontal")
            paned_window.grid(row=r, column=0, columnspan=columns, sticky="nsew", padx=padx, pady=pady)

            for c in range(columns):
                if current_panel >= num_panels:
                    break

                config = element_configs[current_panel]
                title = config.get("title", f"Element {current_panel + 1}")
                element_type = config.get("type", "treeview")

                frame = ttk.Frame(paned_window)
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # Elemento que se almacenará en el diccionario final
                element = {"frame": frame}

                # Treeview
                if element_type == "treeview":
                    treeview = awgf.create_treeview_panel(
                        parent_frame=frame,
                        title=title,
                        row=0,
                        column=0,
                    )
                    element["treeview"] = treeview

                elif element_type == "scrollable_canvas":
                    update_function = config.get("update_function", None)

                    # No lanzamos ninguna excepción aquí
                    canvas, scale = awgf.create_scrollable_canvas(
                        parent=frame,
                        row=0,
                        column=0,
                        label_text=title,
                        update_canvas_slice=update_function  # puede ser None y lo asignas luego
                    )
                    element["canvas"] = canvas
                    element["scale"] = scale

                else:
                    raise ValueError(f"Tipo de elemento desconocido: {element_type}")

                paned_window.add(frame, weight=1)

                # Guardar el elemento por su título
                elements_panels[title] = element

                current_panel += 1

            for c in range(columns):
                root.columnconfigure(c, weight=1)

        return elements_panels
    
    @staticmethod
    def populate_elemnts_panels_new(
        root: Any,
        grid: Tuple[int, int],
        panel_configs: List[Dict[str, Any]],
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Dict[str, Any]:
        """
        Crea y organiza múltiples paneles (treeviews, scrollable_canvas o frames vacíos)
        en PanedWindows, para permitir que todos los paneles sean movibles.

        Args:
            root (Any): Contenedor raíz donde se agregarán los paneles.
            grid (Tuple[int, int]): Número de filas y columnas.
            panel_configs (List[Dict[str, Any]]): Configuración de cada panel.
            default_padding (Tuple[int, int]): Padding entre paneles.

        Returns:
            Dict[str, Any]: Diccionario con los widgets creados.
        """

        num_panels = len(panel_configs)
        rows, columns = grid
        padx, pady = default_padding

        if rows * columns < num_panels:
            raise ValueError("El grid proporcionado no tiene suficientes espacios para los paneles solicitados.")

        panel_widgets = {}

        asymmetric = any(("row" in config and "column" in config) for config in panel_configs)

        main_paned_window = ttk.PanedWindow(root, orient="vertical")
        main_paned_window.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # ======================================================
        # LAYOUT ASIMÉTRICO
        # ======================================================
        if asymmetric:
            for r in range(rows):
                row_paned_window = ttk.PanedWindow(main_paned_window, orient="horizontal")
                main_paned_window.add(row_paned_window, weight=1)

                elements_in_row = [p for p in panel_configs if p.get("row") == r]
                elements_in_row.sort(key=lambda x: x.get("column", 0))

                for config in elements_in_row:
                    title = config.get("title", f"Panel_{r}")
                    widget_type = config.get("type", "treeview")
                    update_function = config.get("update_function", None)

                    frame = ttk.Frame(row_paned_window, borderwidth=1, relief="solid")
                    frame.grid_rowconfigure(0, weight=1)
                    frame.grid_columnconfigure(0, weight=1)

                    element = {"frame": frame}

                    if widget_type == "treeview":
                        treeview = awgf.create_treeview_panel(
                            parent_frame=frame,
                            title=title,
                            row=0,
                            column=0,
                        )
                        element["treeview"] = treeview

                    elif widget_type == "scrollable_canvas":
                        canvas, scale = awgf.create_scrollable_canvas(
                            parent=frame,
                            row=0,
                            column=0,
                            label_text=title,
                            update_canvas_slice=update_function
                        )
                        element["canvas"] = canvas
                        element["scale"] = scale

                    elif widget_type == "frame":
                        sub_frame = ttk.Frame(frame)
                        sub_frame.grid(row=0, column=0, sticky="nsew")

                        '''prueba_button = ttk.Button(sub_frame, text=f"Botón en {title}")
                        prueba_button.pack(expand=True, fill="both")
                        '''
                        element["frame_content"] = sub_frame

                    else:
                        treeview = awgf.create_treeview_panel(
                            parent_frame=frame,
                            title=title,
                            row=0,
                            column=0,
                        )
                        element["treeview"] = treeview

                    row_paned_window.add(frame, weight=1)
                    panel_widgets[title] = element

        # ======================================================
        # LAYOUT SIMÉTRICO
        # ======================================================
        else:
            current_panel = 0

            for r in range(rows):
                row_paned_window = ttk.PanedWindow(main_paned_window, orient="horizontal")
                main_paned_window.add(row_paned_window, weight=1)

                for c in range(columns):
                    if current_panel >= num_panels:
                        break

                    config = panel_configs[current_panel]
                    title = config.get("title", f"Panel_{current_panel}")
                    widget_type = config.get("type", "treeview")
                    update_function = config.get("update_function", None)

                    frame = ttk.Frame(row_paned_window, borderwidth=1, relief="solid")
                    frame.grid_rowconfigure(0, weight=1)
                    frame.grid_columnconfigure(0, weight=1)

                    element = {"frame": frame}

                    if widget_type == "treeview":
                        treeview = awgf.create_treeview_panel(
                            parent_frame=frame,
                            title=title,
                            row=0,
                            column=0,
                        )
                        element["treeview"] = treeview

                    elif widget_type == "scrollable_canvas":
                        canvas, scale = awgf.create_scrollable_canvas(
                            parent=frame,
                            row=0,
                            column=0,
                            label_text=title,
                            update_canvas_slice=update_function
                        )
                        element["canvas"] = canvas
                        element["scale"] = scale

                    elif widget_type == "frame":
                        sub_frame = ttk.Frame(frame)
                        sub_frame.grid(row=0, column=0, sticky="nsew")

                        '''prueba_button = ttk.Button(sub_frame, text=f"Botón en {title}")
                        prueba_button.pack(expand=True, fill="both")'''

                        element["frame_content"] = sub_frame

                    else:
                        treeview = awgf.create_treeview_panel(
                            parent_frame=frame,
                            title=title,
                            row=0,
                            column=0,
                        )
                        element["treeview"] = treeview

                    row_paned_window.add(frame, weight=1)
                    panel_widgets[title] = element
                    current_panel += 1

        return panel_widgets
   
    @staticmethod
    def populate_elemnts_panels_dev(
        root: Any,
        grid: Tuple[int, int],
        panel_configs: List[Dict[str, Any]],
        default_padding: Tuple[int, int] = (5, 5),
    ) -> Dict[str, Any]:
        import tkinter as tk

        num_panels = len(panel_configs)
        rows, columns = grid
        padx, pady = default_padding

        if rows * columns < num_panels:
            raise ValueError("El grid proporcionado no tiene suficientes espacios para los paneles solicitados.")

        panel_widgets = {}
        asymmetric = any(("row" in config and "column" in config) for config in panel_configs)

        # 🔧 Estilo para paned windows
        pane_style = {
            "bg": "#f0f0f0",
            "sashwidth": 5,
            "sashrelief": "flat",
            "bd": 0
        }

        main_paned_window = tk.PanedWindow(root, orient="vertical", **pane_style)
        main_paned_window.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        current_panel = 0

        for r in range(rows):
            row_paned_window = tk.PanedWindow(main_paned_window, orient="horizontal", **pane_style)
            row_index = r * columns
            row_height = panel_configs[row_index].get("height", 400)
            row_paned_window.configure(height=row_height)
            main_paned_window.add(row_paned_window)
            # 🔄 Eliminado minsize para permitir redimensionado más pequeño

            for c in range(columns):
                if current_panel >= num_panels:
                    break

                config = panel_configs[current_panel]
                title = config.get("title", f"Panel_{current_panel}")
                widget_type = config.get("type", "treeview")
                update_function = config.get("update_function", None)

                frame = ttk.Frame(
                    row_paned_window,
                    borderwidth=1,
                    relief="solid",
                    height=config.get("height", 400),
                    width=config.get("width", 400)
                )
                frame.grid_propagate(False)
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                element = {"frame": frame}

                if widget_type == "treeview":
                    treeview = awgf.create_treeview_panel(frame, title, 0, 0)
                    element["treeview"] = treeview

                elif widget_type == "scrollable_canvas":
                    canvas, scale = awgf.create_scrollable_canvas(
                        frame, 0, 0, label_text=title, update_canvas_slice=update_function)
                    element["canvas"] = canvas
                    element["scale"] = scale

                elif widget_type == "frame":
                    sub_frame = ttk.Frame(frame)
                    sub_frame.grid(row=0, column=0, sticky="nsew")
                    element["frame_content"] = sub_frame
                    
                elif widget_type == "canvas":
                    canvas = awgf.create_canvas(
                        parent=frame,
                        row=0,
                        column=0,
                        label_text=title,
                    )
                    element["canvas"] = canvas

                else:
                    treeview = awgf.create_treeview_panel(frame, title, 0, 0)
                    element["treeview"] = treeview

                row_paned_window.add(frame)

                # 🔄 Aplicado solo si minsize viene explícitamente en config
                if "minsize" in config:
                    row_paned_window.paneconfigure(frame, minsize=config["minsize"])

                panel_widgets[title] = element
                current_panel += 1

        return panel_widgets




