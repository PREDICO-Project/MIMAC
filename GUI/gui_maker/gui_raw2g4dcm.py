import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import json
import SimpleITK as sitk
from PIL import Image, ImageTk
from resources.pyresources.names import Names as nm
from resources.pyresources.configs import Cfgs as cfg
from resources.pyresources.configs import Rules
from src.wg_factory.cplWidget_fc import COMPLEXWIDGETFactory as cwgf
from src.gui_handler.window_handler import WINDOWHandler as wh
from resources.pyresources.paths import base_paths
from resources.pyresources.paths import Paths
from src.tool_handler.treeview_handler import TreeViewHandler
from src.tool_handler.selectPlane import SelectPlane
from resources.pyresources.lists import Lists as lst
from mamMC_scripts.pyrawTog4 import DCM2G4


class raw2g4dcm_gui():

    ###############
    # Constructor #
    ###############

    def __init__(self, root:tk.Tk, callback_volver: callable ) -> None:

        self.__root = root  # save la referencia al root pasado 
        self.__root.title(nm.Windows.g4dcm) 
        self.__callback_volver = callback_volver  # save la referencia del callback para "back"

        #Inicializa variables
        self.__init_vars()
        self.__init_gui_elements_config()

        # Main window configuration
        self.__setup_main_frame()
        
        # panel control setup
        self.__setup_control_panel()
        self.__bind_checkbutton_variables()
        self.__load_default_config()
        
        # Visualize frame setup
        self.__setup_visualization_panel()

        # Actions
        self.__get_view_widgets()
        self.__init_gui_elements_actions()     
        self.__init_combobox_content()  
        self.__bind_wl_mouse_events()

        #Centramos la window
        self.__root.update_idletasks()
        #self.__root.geometry("")  # Hace que la window se ajuste automáticamente
        wh.maximizar_ventana(self.__root)

        self.__root.mainloop()
    
    ##########################
    # Initialization methods #
    # Private methods        #
    ##########################

    def __init_vars(self) -> None:

        # Control_panel cfg And elements
        self.__pc1_elements = None
        self.__pc2_elements = None
        self.__pc3_elements = None
        self.__pc1_elements_cfg = None 
        self.__pc2_elements_cfg = None
        self.__pc3_elements_cfg = None
        self.__tk_vars = {}  # para save BooleanVar de cada Checkbutton 

        # Visualization Frame cfg and elements
        self.__vis_elements_cfg = None
        self.__vis_elements = None

        # Execution variables
        self.__file_path = None
        self.__image = None
        self.__array = None

        # Object variables
        self.__axial_scale = None
        self.__axial_canvas = None
        self.__axial_frame = None
        self.__coronal_scale = None
        self.__coronal_canvas = None
        self.__coronal_frame = None
        self.__sagittal_scale = None
        self.__sagittal_canvas = None
        self.__sagittal_frame = None
        self.__tv_data = None

        # SelectPlane instances
        self.__selector_axial = None
        self.__selector_coronal = None
        self.__selector_sagittal = None

        # Scale index values
        self.__slice_idx_axial = 0
        self.__slice_idx_coronal = 0
        self.__slice_idx_sagittal = 0

        # phantom creation parameters
        self.__phantom_params = {}

        # Window/level variables
        self.__window_center = tk.DoubleVar(value=0.0)
        self.__window_width  = tk.DoubleVar(value=1.0)

        self.__mapping = {
            'phantom_lbe1': 'SliceIni',
            'phantom_lbe2': 'SliceEnd',
            'phantom_lbe3': 'ColumIni',
            'phantom_lbe4': 'ColumEnd',
            'phantom_lbe5': 'RowIni',
            'phantom_lbe6': 'RowEnd',
            'phantom_cb1': 'ResetOrigin',
            'phantom_cb2': 'RemoveCW',
            'phantom_cb3': 'IncludePaddle',
            'phantom_cb4': 'RemoveAirSlices',
            'phantom_cb5': 'FreeCut',
            'phantom_cb6': 'DCM',
            'phantom_cb7': 'MHD',
            'phantom_lcb1': 'Materials',
        }

    def __init_gui_elements_config(self) -> None:

        self.__pc1_elements_cfg = cfg.Raw2g4_phatom.pc1_cfg
        self.__pc2_elements_cfg = cfg.Raw2g4_phatom.pc2_cfg
        self.__pc3_elements_cfg = cfg.Raw2g4_phatom.pc3_cfg
        self.__vis_elements_cfg = cfg.Raw2g4_phatom.vis_cfg
    
    def __init_gui_elements_actions(self) -> None:
        # buttons del panel de control
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt5']].config(command=self.go_back)
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt1']].config(command=self.select_raw_nrrd_file)
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt3']].config(command=self.show_plane_selectors)
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt6']].config(command=self.hide_plane_selectors)
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt2']].config(command=self.create_phantom)
        self.__pc3_elements['button'][nm.Buttons.PHANTOM_CP['bt7']].config(
            command=lambda: (self.__auto_window_level(), self.__on_wl_change())
        )

        # Vincular scales con la actualización de canvas
        self.__axial_scale.config(command=lambda v: self.__render_canvas_slice(self.__axial_canvas, int(float(v))))
        self.__coronal_scale.config(command=lambda v: self.__render_canvas_slice(self.__coronal_canvas, int(float(v))))
        self.__sagittal_scale.config(command=lambda v: self.__render_canvas_slice(self.__sagittal_canvas, int(float(v))))

    def __get_view_widgets(self):
        if not self.__vis_elements:
            raise ValueError("No se han creado elementos visuales aún.")

        try:
            self.__axial_canvas = self.__vis_elements["Axial view"]["canvas"]
            self.__axial_scale = self.__vis_elements["Axial view"]["scale"]
            self.__axial_frame = self.__vis_elements["Axial view"]["frame"]

            self.__coronal_canvas = self.__vis_elements["Sagittal view"]["canvas"]
            self.__coronal_scale = self.__vis_elements["Sagittal view"]["scale"]
            self.__coronal_frame = self.__vis_elements["Sagittal view"]["frame"]

            self.__sagittal_canvas = self.__vis_elements["Coronal view"]["canvas"]
            self.__sagittal_scale = self.__vis_elements["Coronal view"]["scale"]
            self.__sagittal_frame = self.__vis_elements["Coronal view"]["frame"]

            #self.__tv_data = self.__vis_elements["data from mhd file"]["treeview"]
            self.__tv_data = self.__pc2_elements["treeview"][nm.Treeview.PHANTOM_CP['tv1']]

            # Bind manual del frame contenedor (por PanedWindow)
            self.__axial_frame.bind("<Configure>", lambda e: self.__render_canvas_slice(
                self.__axial_canvas, self.__slice_idx_axial))
            self.__coronal_frame.bind("<Configure>", lambda e: self.__render_canvas_slice(
                self.__coronal_canvas, self.__slice_idx_coronal))
            self.__sagittal_frame.bind("<Configure>", lambda e: self.__render_canvas_slice(
                self.__sagittal_canvas, self.__slice_idx_sagittal))

        except KeyError as e:
            raise KeyError(f"No se encontró el elemento esperado: {e}")
    
    def __init_combobox_content(self) -> None:
        """
        Asigna dinámicamente valores a los combobox en diferentes pestañas usando un diccionario de mapeo.
        """
        self.__pc2_elements['label_combobox'][nm.LabelCombobox.PHANTOM_CP['lcb1']].config(values=lst.phantom.materials)

    def __load_default_config(self):
        try:
            with open(Paths.Raw2G4DCM.default_config, "r", encoding="utf-8") as f:
                self.__phantom_params = json.load(f)
                self.__apply_config_to_widgets(self.__phantom_params)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar configuración por defecto: {e}")

    def __apply_config_to_widgets(self, params: dict):
        on, off = ("Yes", "No")
        for key, param in self.__mapping.items():
            value = params.get(param, "")

            # Checkbox
            if key.startswith("phantom_cb"):
                var = self.__tk_vars.get(key)
                if var:
                    var.set(on if value in (True, 1, "Yes") else off)
                    #print(f"{key} → widget: {widget}, value: {value}")

            # Combobox
            elif key.startswith("phantom_lcb"):
                widget = self.__get_widget_by_key(key)
                if widget:
                    widget.set(value)
                    #print(f"{key} → widget: {widget}, value: {value}")

            # Entries
            elif key.startswith("phantom_lbe"):
                widget = self.__get_widget_by_key(key)
                if widget:
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
                    #print(f"{key} → widget: {widget}, value: {value}")

    
    ######################
    # GUI filled methods #
    # Private methods    #
    ######################

    def __setup_main_frame(self) -> None:
        """
        Create the main container within the root window (Ventana principal).        
        """       
        # Creamos el main_frame
        self.__phantom_frame = ttk.Frame(self.__root, style='TFrame')      
        self.__phantom_frame.pack(fill=tk.BOTH, expand=True)  
        #self.__setupsim_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configure grid expansion
        self.__phantom_frame.columnconfigure(0, weight=0)  # Primer panel
        self.__phantom_frame.columnconfigure(1, weight=0)  # Segundo panel
        self.__phantom_frame.columnconfigure(2, weight=1)  # Frame de visualization (se expande)
        self.__phantom_frame.rowconfigure(0, weight=1)


        #wh.maximizar_ventana(self.__root)

        self.__root.update_idletasks()
    
    def __setup_control_panel(self) -> None:
        """
        Create and place the control panel on the top-left.
        """
        panel_control_frame1 = ttk.Frame(self.__phantom_frame, style='TFrame')
        panel_control_frame1.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        panel_control_frame2 = ttk.Frame(self.__phantom_frame, style='TFrame')
        panel_control_frame2.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        # create los buttons dentro del contenedor
        self.__pc1_elements = cwgf.populate_control_panel(
            root = panel_control_frame1, 
            list_cfg = self.__pc1_elements_cfg, 
            horizontal = False
        )
        
        self.__pc2_elements = cwgf.populate_control_panel(
            root = panel_control_frame2, 
            list_cfg = self.__pc2_elements_cfg, 
            horizontal = False
        )

        self.__root.update_idletasks()
    
    def __setup_visualization_panel(self) -> None:
        """
        Create an empty Notebook with tabs and expand it properly.
        """
        # create un frame contenedor para el Notebook y el panel de control superior
        container_frame = ttk.Frame(self.__phantom_frame, style='TFrame')
        container_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        pc_frame = ttk.Frame(container_frame, style='TFrame')
        pc_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.__pc3_elements = cwgf.populate_control_panel(
            root = pc_frame, 
            list_cfg = self.__pc3_elements_cfg, 
            horizontal = True
        )

        views_frame = ttk.Frame(container_frame, style='TFrame')
        views_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.__vis_elements = cwgf.populate_elemnts_panels_dev(
            root = views_frame, 
            grid = [2,2],
            panel_configs = self.__vis_elements_cfg
        )


        self.__root.update_idletasks()
    
    #############################
    # Visual management methods #
    # Private methods           #
    #############################

    def __auto_window_level(self):
        """
        Calculate window/level using 2nd and 98th percentiles
        de la slice axial central del volumen.
        """
        # Índice de la slice central axial
        z_mid = self.__array.shape[0] // 2
        # Extraemos esa slice y la aplanamos
        central = self.__array[z_mid, :, :].flatten()

        # Calculamos percentiles
        p2, p98 = np.percentile(central, (2, 98))

        ww = float(p98 - p2)
        wc = float((p98 + p2) / 2.0)

        # Evitamos width cero
        ww = max(1.0, ww)

        # Asignamos
        self.__window_width.set(ww)
        self.__window_center.set(wc)
    
    def __load_image_and_render_views(self, phantom: bool = False) -> None:
        self.__image = sitk.ReadImage(self.__file_path)
        self.__array = sitk.GetArrayFromImage(self.__image)

        # ── Nuevo: calcula WL sobre la slice central ──
        self.__auto_window_level()

        # update escalas
        shape = self.__array.shape  # (z, y, x)
        self.__axial_scale.config(to=shape[0] - 1)
        self.__coronal_scale.config(to=shape[1] - 1)
        self.__sagittal_scale.config(to=shape[2] - 1)

        # show primera slice con WL optimizado
        self.__render_canvas_slice(self.__axial_canvas, 0)
        self.__render_canvas_slice(self.__coronal_canvas, 0)
        self.__render_canvas_slice(self.__sagittal_canvas, 0)

    def __render_canvas_slice(self, canvas: tk.Canvas, slice_index: int) -> None:
        """
        Extract the specified slice and store its index,
        aplica window/level y la dibuja en el canvas.
        """
        if self.__array is None:
            return

        # Selección de slice y actualización del índice
        if canvas is self.__axial_canvas:
            slice_array = self.__array[slice_index, :, :]
            selector    = self.__selector_axial
            self.__slice_idx_axial = slice_index
        elif canvas is self.__coronal_canvas:
            slice_array = self.__array[:, slice_index, :]
            selector    = self.__selector_coronal
            self.__slice_idx_coronal = slice_index
        elif canvas is self.__sagittal_canvas:
            slice_array = self.__array[:, :, slice_index]
            selector    = self.__selector_sagittal
            self.__slice_idx_sagittal = slice_index
        else:
            return

        # Cálculo de window/level
        wc = self.__window_center.get()
        ww = max(1.0, self.__window_width.get())
        lo = wc - ww/2.0
        hi = wc + ww/2.0

        arr = slice_array.astype(float)
        win = (arr - lo) / ww * 255.0
        win = np.clip(win, 0, 255).astype(np.uint8)

        def _redraw():
            # Redibuja la image ajustada
            self.__show_image_on_canvas(canvas, win)
            if selector:
                selector.redraw_lines()
                selector.update_entries()

        # Usamos after_idle para repintar en cuanto el loop esté libre
        canvas.after_idle(_redraw)
   
    def __show_image_on_canvas(self, canvas: tk.Canvas, array: np.ndarray) -> None:
        """
        Draw or update the image in the canvas without full redraw.
        """
        width, height = canvas.winfo_width(), canvas.winfo_height()
        
        if width < 2 or height < 2:
            # Espera a que el canvas tenga tamaño
            canvas.after(50, lambda: self.__show_image_on_canvas(canvas, array))
            return

        # Genera el PhotoImage
        pil_img = Image.fromarray(array)
        resized = pil_img.resize((width, height), Image.LANCZOS)
        photo   = ImageTk.PhotoImage(resized)

        ratio = min(width / pil_img.size[0], height / pil_img.size[1])
        new_width = int(pil_img.size[0] * ratio)
        new_height = int(pil_img.size[1] * ratio)

        xcoord = (width - new_width) // 2
        ycoord = (height - new_height) // 2

        #print('Old Dim: ', (width,height))
        #print('New Dim: ', ( new_width, new_height))

        '''if rel_height_width_image > 1:
            orig_width = width
            width = int(height /rel_height_width_image)
            xcoord = orig_width//2
            ycoord = height//2
        else:
            orig_height = height
            height = int(width * rel_height_width_image)
            #xcoord = width//2
            xcoord = width//2
            ycoord = orig_height//2'''

        canvas.orig_image_dim = (pil_img.size[0], pil_img.size[1])
        canvas.image_offset = (xcoord, ycoord)
        canvas.image_dim = (new_width, new_height)
        resized = pil_img.resize((new_width, new_height), Image.LANCZOS)
        photo   = ImageTk.PhotoImage(resized)
        # Si no existe aún, lo creamos y guardamos el id

        if not hasattr(canvas, "_img_id"):

            canvas._img_id = canvas.create_image(xcoord, ycoord, image=photo, anchor = 'nw')
            #canvas._img_id = canvas.create_image(0, 0, image=photo, anchor="nw")

        else:
            # Sólo actualizamos la image del item existente
            canvas.itemconfig(canvas._img_id, image=photo)

        # Guardamos la referencia para evitar que se recoja
        canvas._photo = photo

    def __init_plane_selectors(self):

        shape = self.__array.shape  # (z, y, x)

        # Diccionario de entries y dimensiones para cada vista
        planos = {
            "axial": {
                "canvas": self.__axial_canvas,
                "orient": "vertical",
                "entry1": nm.LabelEntry.PHANTOM_CP['lbe1'],
                "entry2": nm.LabelEntry.PHANTOM_CP['lbe2'],
                "shape": (shape[2], shape[1])
            },
            "coronal": {
                "canvas": self.__coronal_canvas,
                "orient": "horizontal",
                "entry1": nm.LabelEntry.PHANTOM_CP['lbe3'],
                "entry2": nm.LabelEntry.PHANTOM_CP['lbe4'],
                "shape": (shape[2], shape[0])
            },
            "sagittal": {
                "canvas": self.__sagittal_canvas,
                "orient": "vertical",
                "entry1": nm.LabelEntry.PHANTOM_CP['lbe5'],
                "entry2": nm.LabelEntry.PHANTOM_CP['lbe6'],
                "shape": (shape[1], shape[0])
            }
        }

        # create los selectores
        self.__selector_axial = SelectPlane(
            planos["axial"]["canvas"],
            planos["axial"]["orient"],
            self.__pc2_elements["label_entry"][planos["axial"]["entry1"]],
            self.__pc2_elements["label_entry"][planos["axial"]["entry2"]],
            planos["axial"]["shape"],
            enable_var=self.__tk_vars["phantom_cb5"]
        )

        self.__selector_coronal = SelectPlane(
            planos["coronal"]["canvas"],
            planos["coronal"]["orient"],
            self.__pc2_elements["label_entry"][planos["coronal"]["entry1"]],
            self.__pc2_elements["label_entry"][planos["coronal"]["entry2"]],
            planos["coronal"]["shape"],
            enable_var=self.__tk_vars["phantom_cb5"]
        )

        self.__selector_sagittal = SelectPlane(
            planos["sagittal"]["canvas"],
            planos["sagittal"]["orient"],
            self.__pc2_elements["label_entry"][planos["sagittal"]["entry1"]],
            self.__pc2_elements["label_entry"][planos["sagittal"]["entry2"]],
            planos["sagittal"]["shape"],
            enable_var=self.__tk_vars["phantom_cb5"]
        )
    
    def __bind_entries_to_selectors(self):
        if self.__selector_axial:
            for entry in [self.__selector_axial.entry1, self.__selector_axial.entry2]:
                entry.bind("<Return>", lambda e, origin=entry: self.__selector_axial.update_lines_from_entry(origin))
                entry.bind("<FocusOut>", lambda e, origin=entry: self.__selector_axial.update_lines_from_entry(origin))

        if self.__selector_coronal:
            for entry in [self.__selector_coronal.entry1, self.__selector_coronal.entry2]:
                entry.bind("<Return>", lambda e, origin=entry: self.__selector_coronal.update_lines_from_entry(origin))
                entry.bind("<FocusOut>", lambda e, origin=entry: self.__selector_coronal.update_lines_from_entry(origin))

        if self.__selector_sagittal:
            for entry in [self.__selector_sagittal.entry1, self.__selector_sagittal.entry2]:
                entry.bind("<Return>", lambda e, origin=entry: self.__selector_sagittal.update_lines_from_entry(origin))
                entry.bind("<FocusOut>", lambda e, origin=entry: self.__selector_sagittal.update_lines_from_entry(origin))

    def __bind_wl_mouse_events(self):
        """
        Bindea el click, el drag y el release sobre cada canvas
        para controlar window/level y repintar al soltar.
        """
        for canvas in (self.__axial_canvas,
                       self.__coronal_canvas,
                       self.__sagittal_canvas):
            canvas.bind("<ButtonPress-2>",   self.__on_mouse_press_wl)
            canvas.bind("<B2-Motion>",       self.__on_mouse_drag_wl)

    def __on_mouse_press_wl(self, event):
        """
        Guarda la posición inicial del ratón y los valores de window/level
        al comenzar el drag.
        """
        self.__wl_drag_start_x = event.x
        self.__wl_drag_start_y = event.y
        self.__wl_start_width  = self.__window_width.get()
        self.__wl_start_center = self.__window_center.get()

    def __on_mouse_drag_wl(self, event):
        """
        Calcula el desplazamiento dx/dy y ajusta window (width) y level (center).
        Luego repinta las vistas.
        """
        dx = event.x - self.__wl_drag_start_x
        dy = event.y - self.__wl_drag_start_y

        # Sensibilidad: unidades de HU por pixel
        sens_width  = 1.0
        sens_center = 1.0

        new_width  = max(1.0, self.__wl_start_width  + dx * sens_width)
        new_center = self.__wl_start_center     - dy * sens_center

        self.__window_width.set(new_width)
        self.__window_center.set(new_center)

        self.__on_wl_change()

    def __on_wl_change(self):
        """
        Repinta las tres vistas con el window/level actual.
        """
        for canvas, idx in (
            (self.__axial_canvas,    self.__slice_idx_axial),
            (self.__coronal_canvas,  self.__slice_idx_coronal),
            (self.__sagittal_canvas, self.__slice_idx_sagittal)
        ):
        
            self.__render_canvas_slice(canvas, idx)

        self.__root.update_idletasks()
       
    ##########################
    # Parameter handler methods #
    ##########################

    def __bind_checkbutton_variables(self):
        """
        Crea y asocia un StringVar inicializado en 'Yes' a cada Checkbutton del panel 2,
        lo guarda en self.__tk_vars[key], configura on/off para mostrar 'Yes'/'No',
        y añade un trace para disparar la lógica al cambiar.
        """
        for suffix, name in nm.CheckBoxes.PHANTOM_CP.items():
            full_key = f"phantom_{suffix}"
            widget = self.__pc2_elements["check_box_label"].get(name)
            if widget:
                var = tk.StringVar(value=nm.common.checkBoxText[0])
                widget.config(
                    variable=var,
                    textvariable=var,
                    onvalue=nm.common.checkBoxText[0],
                    offvalue=nm.common.checkBoxText[1]
                )
                self.__tk_vars[full_key] = var
                var.trace_add("write", lambda *_: self.__apply_control_logic())

    def __get_checkbox_state(self, key: str) -> bool:
        """
        Devuelve True si el StringVar vale "Yes", False si vale "No".
        """
        val = self.__tk_vars[key].get()
        return val == nm.common.checkBoxText[0]

    def __get_phantom_parameters(self) -> dict:
        """
        Devuelve los parámetros del fantasma, devolviendo 0 en los campos numéricos vacíos.
        """
        # helper para leer un entry y convertir a int o 0 si está vacío
        def _get_int(entry):
            s = entry.get().strip()
            return int(s) if s else 0
        return {
            'Materials'      : self.__pc2_elements["label_combobox"][nm.LabelCombobox.PHANTOM_CP['lcb1']].get(),
            'DCM'            : self.__get_checkbox_state("phantom_cb6"),
            'MHD'            : self.__get_checkbox_state("phantom_cb7"),
            'ResetOrigin'    : self.__get_checkbox_state("phantom_cb1"),
            'RemoveCW'       : self.__get_checkbox_state("phantom_cb2"),
            'IncludePaddle'  : self.__get_checkbox_state("phantom_cb3"),
            'RemoveAirSlices': self.__get_checkbox_state("phantom_cb4"),
            'FreeCut'        : self.__get_checkbox_state("phantom_cb5"),
            'SliceIni'       : _get_int(self.__pc2_elements["label_entry"][nm.LabelEntry.PHANTOM_CP['lbe1']]),
            'SliceEnd'       : _get_int(self.__pc2_elements["label_entry"][nm.LabelEntry.PHANTOM_CP['lbe2']]),
            'ColumIni'       : _get_int(self.__pc2_elements["label_entry"][nm.LabelEntry.PHANTOM_CP['lbe3']]),
            'ColumEnd'       : _get_int(self.__pc2_elements["label_entry"][nm.LabelEntry.PHANTOM_CP['lbe4']]),
            'RowIni'         : _get_int(self.__pc2_elements["label_entry"][nm.LabelEntry.PHANTOM_CP['lbe5']]),
            'RowEnd'         : _get_int(self.__pc2_elements["label_entry"][nm.LabelEntry.PHANTOM_CP['lbe6']]),
        }

    def __apply_control_logic(self) -> None:
        """
        Aplica reglas de lógica entre widgets según Rules.phantom_gui_rules.
        """
        for rule in Rules.phantom_gui_rules:
            trigger = rule["trigger"]
            expected = bool(rule["expected"])
            action = rule["action"]
            targets = rule["targets"]
            value = rule.get("value", None)

            # 1) Extrae value actual del trigger
            var = self.__tk_vars.get(trigger)
            if var is None:
                print(f"[WARN] Variable de trigger '{trigger}' no registrada.")
                continue

            raw_val = var.get()
            trigger_val = raw_val == nm.common.checkBoxText[0] if isinstance(raw_val, str) else bool(raw_val)

            # 2) Compara con el esperado
            apply_action = (trigger_val == expected)

            # 3) Aplica la acción a los targets
            for target in targets:
                widget = self.__get_widget_by_key(target)
                if not widget:
                    print(f"[WARN] Widget '{target}' no encontrado.")
                    continue

                if action == "disable":
                    widget.config(state="disabled" if apply_action else "normal")
                elif action == "normal":
                    widget.config(state="normal" if apply_action else "disabled")
                elif action == "set" and apply_action:
                    var_t = self.__tk_vars.get(target)
                    if var_t:
                        var_t.set(value)
                else:
                    print(f"[WARN] Acción desconocida '{action}' en regla.")

    def __get_widget_by_key(self, key: str):
        """
        Dado un nombre como 'phantom_cb5' o 'phantom_lbe2', devuelve el widget asociado del panel 2.
        """
        try:
            section, suffix = key.split('_', 1)
        except ValueError:
            print(f"[ERROR] Formato de clave inválido: {key}")
            return None

        # Alias para mapear correctamente la sección al atributo del diccionario de nombres
        section_aliases = {
            "phantom": "PHANTOM_CP"
        }

        # Diccionarios de widgets por sección (aquí sólo panel 2)
        element_map = {
            'phantom': self.__pc2_elements
        }

        # Tipos de widgets que soportamos
        widget_types = {
            'lbe': ('label_entry', nm.LabelEntry),
            'lcb': ('label_combobox', nm.LabelCombobox),
            'cb':  ('check_box_label', nm.CheckBoxes)
        }

        for prefix in widget_types:
            if suffix.startswith(prefix):
                if section in element_map:
                    dict_name, nm_class = widget_types[prefix]
                    widget_dict = element_map[section].get(dict_name, {})

                    try:
                        section_key = section_aliases.get(section, f"{section.upper()}_CP")
                        widget_name = getattr(nm_class, section_key)[suffix]
                        widget = widget_dict.get(widget_name)

                        if isinstance(widget, dict):
                            for part in ("entry", "combobox", "checkbutton"):
                                if part in widget:
                                    return widget[part]
                        return widget
                    except Exception as e:
                        print(f"[ERROR] No se pudo recuperar el widget '{key}': {e}")
                        return None

        print(f"[WARN] Sufijo '{suffix}' no coincide con tipos conocidos ('lbe', 'lcb', 'cb')")
        return None

    ##################
    # Button methods #
    ##################

    def select_raw_nrrd_file(self):
        '''
        Dialog to select and load a MHD file.
        '''
        # Diálogo para select file
        self.__file_path = filedialog.askopenfilename(
            master=self.__root,
            title="Select a MHD File",
            initialdir=base_paths.original_mhd,
            filetypes=[("MHD files", "*.mhd")]
        )

        if self.__file_path:
            # Leemos y mostramos el content en el text area si lo tienes
            with open(self.__file_path, 'r') as file:
                lines = file.read().splitlines()

            # Process lines and round ElementSpacing if present
            new_lines = []
            for line in lines:
                if line.startswith("ElementSpacing"):
                    # Separar la key del content numérico
                    key, values = line.split("=", 1)
                    numbers = values.strip().split()
                    # Round to 3 decimals
                    rounded = [f"{float(n):.3f}" for n in numbers]
                    new_line = f"{key.strip()} = {' '.join(rounded)}"
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)

            #TreeViewHandler.clear_treeview(self.__tv_data)
            TreeViewHandler.fill_treeview(self.__tv_data, new_lines,clearData=True)

            self.__filename = os.path.splitext(os.path.basename(self.__file_path))[0]

            # Cargamos y visualizamos
            self.__load_image_and_render_views()

            # Actualizamos el nombre del phantom en la etiqueta
            self.__pc2_elements['label'][nm.Labels.PHANTOM_CP['lb3']].config(text=self.__filename)
           
    def show_plane_selectors(self):
        if self.__array is None:
            messagebox.showinfo("Warning", "A .mhd file must be uploaded first.")
            return

        self.__tk_vars['phantom_cb5'].set('Yes') # Don't eliminate this line, it is important to solve a bug!!
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt3']].config(state='disabled')
        #self.__repaint_all_views(force_index=0)

        # Resize fantasma para forzar actualización real del canvas
        for canvas in [self.__axial_canvas, self.__coronal_canvas, self.__sagittal_canvas]:
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            canvas.config(width=w + 1, height=h + 1)
            canvas.update_idletasks()
            canvas.config(width=w, height=h)

        self.__root.after(10, lambda: [
            self.__init_plane_selectors(),
            self.__bind_entries_to_selectors()
        ])

        # Habilitar entries
        if self.__get_checkbox_state("phantom_cb5"):
            for entry_id in [
                nm.LabelEntry.PHANTOM_CP['lbe1'], nm.LabelEntry.PHANTOM_CP['lbe2'],
                nm.LabelEntry.PHANTOM_CP['lbe3'], nm.LabelEntry.PHANTOM_CP['lbe4'],
                nm.LabelEntry.PHANTOM_CP['lbe5'], nm.LabelEntry.PHANTOM_CP['lbe6']
            ]:
                widget = self.__pc2_elements["label_entry"].get(entry_id)
                if widget:
                    widget.config(state='normal')

    def hide_plane_selectors(self):
        # Elimina líneas y referencias
        if self.__selector_axial:
            self.__selector_axial.eliminar()
            self.__selector_axial = None

        if self.__selector_coronal:
            self.__selector_coronal.eliminar()
            self.__selector_coronal = None

        if self.__selector_sagittal:
            self.__selector_sagittal.eliminar()
            self.__selector_sagittal = None

        # Forzar repintado sin líneas
        self.__render_canvas_slice(self.__axial_canvas, self.__slice_idx_axial)
        self.__render_canvas_slice(self.__coronal_canvas, self.__slice_idx_coronal)
        self.__render_canvas_slice(self.__sagittal_canvas, self.__slice_idx_sagittal)

        # Vaciar y desactivar entries
        entry_ids = [
            nm.LabelEntry.PHANTOM_CP['lbe1'], nm.LabelEntry.PHANTOM_CP['lbe2'],
            nm.LabelEntry.PHANTOM_CP['lbe3'], nm.LabelEntry.PHANTOM_CP['lbe4'],
            nm.LabelEntry.PHANTOM_CP['lbe5'], nm.LabelEntry.PHANTOM_CP['lbe6']
        ]

        for entry_id in entry_ids:
            entry_widget = self.__pc2_elements["label_entry"].get(entry_id)
            if entry_widget:
                entry_widget.delete(0, tk.END)
                #entry_widget.config(state='disable') # Not needed, already disabled by logic
                
        self.__tk_vars['phantom_cb5'].set('No') # Don't eliminate this line, it is important to solve a bug!!
        self.__pc1_elements['button'][nm.Buttons.PHANTOM_CP['bt3']].config(state='normal')

    def create_phantom(self):
        """
        Method to create the phantom based on selected parameters.
        """
        # Obtener los parámetros actualizados
        self.__phantom_params = self.__get_phantom_parameters()

        #print("Parámetros del fantasma:", self.__phantom_params)
    
        
        if self.__file_path:

            # pyrawTog4
            g4dcm = DCM2G4(self.__root)
            params = self.__get_phantom_parameters()

           
            if params['Materials'] is None:
                pass
            else:
                g4dcm.materials_filename = params['Materials']
        
            g4dcm.filein_name = self.__filename
            g4dcm.reset_origin = params['ResetOrigin']
            g4dcm.remove_chest_wall = params['RemoveCW']
            #g4dcm.in_or_out = params['IncludePaddle']
            #g4dcm.cut_only_air = params['CutOnlyAir']
            g4dcm.free_cut = params['FreeCut']
            g4dcm.slice_ini = params['SliceIni']
            g4dcm.slice_end = params['SliceEnd']
            g4dcm.colum_ini = params['ColumIni']
            g4dcm.colum_end = params['ColumEnd']
            g4dcm.row_ini = params['RowIni']
            g4dcm.row_end = params['RowEnd']
            g4dcm.dcm = params['DCM']
            g4dcm.raw = params['MHD']
    
            #g4dcm.materials_to_remove = values

            #g4dcm.create_phantom_file()
            g4dcm.start_processing()

            #self.view_pantom_button['state'] = 'normal'
            self.raw = params['MHD']
        
        else:
            messagebox.showinfo("Warning", "Not file has been selected.")

        # show message de éxito
        #messagebox.showinfo("Éxito", "Fantasma creado con éxito.")
    
    def go_back(self) -> None:
        """
        Método para go_back a la interfaz principal.
        """
        for widget in self.__root.winfo_children():
            widget.destroy()  # Destruir todo el content actual
        
        # Alternativa: Destruir el `main_frame` completamente y recrearlo
        self.__phantom_frame.destroy()
        self.__callback_volver()  # Llamar al callback para reconstruir la interfaz main