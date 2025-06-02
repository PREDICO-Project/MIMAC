import json
import os
import tkinter as tk
from tkinter import BooleanVar, ttk
from tkinter import filedialog
from tkinter import messagebox
from resources.pyresources.names import Names as nm
from resources.pyresources.paths import Paths as path
from resources.pyresources.configs import Cfgs as cfg
from resources.pyresources.configs import Rules
from resources.pyresources.lists import Lists as lst
from src.gui_handler.window_handler import WINDOWHandler as wh
from src.wg_factory.cplWidget_fc import COMPLEXWIDGETFactory as cwgf
from src.wg_factory.adWidget_fc import AdvancedWidgets as awgf
from mamMC_scripts.sim_setup import SimSetup
from gui_maker.gui_Nevents import Nevents_cal

class sim_setup_gui():

    ###############
    # Constructor #
    ###############
    
    def __init__(self, root:tk.Tk, callback_volver: callable ) -> None:

        self.__root = root  # Guardar la referencia al root pasado 
        self.__root.title(nm.Windows.SIM_SETUP) 
        self.__callback_volver = callback_volver  # Guardar la referencia del callback para "Volver"
        
        #Inicializa variables
        self.__ini_vars()
        self.__ini_guiElements_cfg()
        
        # Main window configuration
        self.__build_main_container()
        self.__setup_main_window()
        
        # Panel control setup
        self.__setup_control_panel()
        
        # Notebook setup
        self.__setup_notebook_panel()
        
        # Sumary frame setup
        self.__setup_sim_summary_frame()

        # Configure notebook tabs
        self.__setup_main_file_frame()
        self.__setup_geometry_frame()
        self.__setup_physicANDfilters_frame()
        self.__setup_source_frame()
        self.__setup_detector_frame()        
        self.__setup_scoring_frame()
        
        # Actions
        self. __ini_guiComboBox_content()
        self.__ini_guiElements_Actions()
        
        # Load default setup parameters
        self.__ini_setupVars()
        self.__load_default_setupParams()
        self.__vincule_vars()
        self.__update_widget_values()
        self.__update_sim_summary()

        # Aseguramos que todos los widgets estén bien colocados
        self.__root.update_idletasks()

        # Centrar la ventana con tamaño ajustado al contenido real       
        self.__root.geometry("1400x790")
        wh.centrar_ventana(self.__root)
        #wh.maximizar_ventana(self.__root)

        # Luego de un tiempo (1s), maximizar
        #self.__root.after(500, lambda: wh.maximizar_ventana(self.__root))

        # Lanzar el loop de la GUI
        self.__root.mainloop()

    ##########################
    # Initialization methods #
    # Private methods        #
    ##########################
    
    def __ini_vars(self) -> None:

        # Main conbtainer
        self.__main_container = None
        
        # Control_panel cfg And elements
        self.__pc_elements = None
        self.__pc_elements_cfg = None
        
        # NoteBook cfg And elements
        self.__nb = None
        self.__nb_elements = None
        self.__nb_elements_cfg = None

        # Summary frame cfg And elements
        self.__summary_frame_elements = None
        self.__summary_frame_cfg = None
        
        # Frames in notebook cfgs And elements
        self.__f_main_elements = None
        self.__f_main_cfg = None
        self.__f_geometry_elements = None
        self.__f_geometry_cfg = None
        self.__f_physicfilters_elements = None
        self.__f_physicfilters_cfg = None
        self.__f_source_elements = None
        self.__f_source_cfg = None        
        self.__f_detector_elements = None
        self.__f_detector_cfg = None      
        self.__f_scoring_elements = None
        self.__f_scoring_cfg = None
        
        # Instancias
        self.__simSetup = SimSetup()

        # Mapeo de nombres de parámetros → nombres legibles para el resumen
        self.__summary_map = {
            # MAIN PARAMETERS
            'Number of events:': 'NEvents',
            # GEOMETRY PARAMETERS
            'World file:': 'WorldFile',
            'Voxelized phantom:': 'DICOMGeom',
            'Phantom file:': lambda params: params['VoxelPhantom'] if params.get('DICOMGeom') == 'Yes' else params.get('GeomtryPhantom', ''),
            'Source-Detector distance:': 'SDD',
            'Physical detector:': lambda params: 'Yes' if params.get('DetectorModel') == 'MCD' else 'No',
            'Source-Object distance:': 'SOD',
            # PHYSICS PARAMETERS
            'Physics list:': 'PhysicList',
            # SOURCE PARAMETERS
            'Spectrum file:': 'Spectra',
            'Source distribution:': 'Distribution',
            'Align source automatically:': 'AlignSource',
            'Auto-size source:': 'AutoSizeSource',
            # DETECTOR PARAMETERS
            'Detector model:': 'DetectorModel',
            'Anti-scatter grid:': 'UseAntiScatterGrid',
        }

        self.__rebuild_summary_trigger_vars = [
            'physic_filters_cb1',  # ApplyF1
            'physic_filters_cb2',  # ApplyF2
            'physic_filters_cb3',  # ApplyF3
            'physic_filters_cb4',  # ApplyF4
        ]

    def __ini_guiElements_cfg(self) -> None:

        self.__pc_elements_cfg = cfg.SetupWindow.pc_cfg
        
        # Configuración de pestañas
        self.__nb_tabs = cfg.NoteBookTabs.setupNotebook
        self.__f_main_cfg = cfg.SetupWindow.main_file
        self.__f_geometry_cfg = cfg.SetupWindow.geometry 
        self.__f_physicfilters_cfg = cfg.SetupWindow.physicANDfilters
        self.__f_source_cfg = cfg.SetupWindow.source
        self.__f_detector_cfg = cfg.SetupWindow.detector
        self.__f_scoring_cfg = cfg.SetupWindow.scoring
        self.__summary_frame_cfg = cfg.SetupWindow.summary_cfg
        self.__main_window_cfg = cfg.SetupWindow.main_window_cfg
        
    def __ini_guiElements_Actions(self) -> None:
        
        self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt1']].config(command=self.apply_cfg)
        self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt2']].config(command=self.load_cfg)
        self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt3']].config(command=self.save_config)
        self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt6']].config(command=self.open_input_file)
        #self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt7']].config(command=self.debug_file)
        self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt4']].config(command=self.cal_Nevents)
        self.__pc_elements['button'][nm.Buttons.SIM_SETUP_CP['bt5']].config(command=self.volver)
        
    def __ini_guiComboBox_content(self) -> None:
        
        """
        Asigna dinámicamente valores a los combobox en diferentes pestañas usando un diccionario de mapeo.
        """
        # Inicializamos el combobox del panel de control con los ficheros inputs
        self.__pc_elements['label_combobox'][nm.LabelCombobox.SIM_SETUP_CP['lcb1']].config(values=list(path.SimSetup.destiny_folder.keys()))

        # Diccionario de mapeo entre pestañas y listas de valores
        combobox_mapping = {
            'physicandfilters': {
                'widget_dict': self.__f_physicfilters_elements['label_combobox'],
                'values_dict': lst.Physicandfilters,
                'mapping': {
                    'lcb1': 'physics_list'
                }
            },
            'geometry': {
                'widget_dict': self.__f_geometry_elements['label_combobox'],
                'values_dict': lst.Geometry,
                'mapping': {
                    'lcb1': 'phantom',
                    'lcb2': 'phantom_voxelized',
                    'lcb3': 'world',
                    'lcb4': 'world_fill'
                }
            },
            'source': {
                'widget_dict': self.__f_source_elements['label_combobox'],
                'values_dict': lst.Source,
                'mapping': {
                    'lcb1': 'particle',
                    'lcb2': 'spectra',
                    'lcb3': 'spectra_filled_mod',
                    'lcb4': 'pos_dist',
                    'lcb5': 'dist_shape'
                }
            },
            'detector': {
                'widget_dict': self.__f_detector_elements['label_combobox'],
                'values_dict': lst.Detector,
                'mapping': {
                    'lcb1': 'model',
                    'lcb2': 'material',
                    'lcb3': 'output_format',
                    'lcb4': 'output_type'
                }
            },
            'scoring': {
                'widget_dict': self.__f_scoring_elements['label_combobox'],
                'values_dict': lst.Scoring,
                'mapping': {
                    'lcb1': 'ioc_fill'
                }
            }
        }

        # Iterar sobre cada pestaña y configurar sus combobox
        for tab, config in combobox_mapping.items():
            widget_dict = config['widget_dict']
            values_dict = config['values_dict']
            for key, value_attr in config['mapping'].items():
                if key in nm.LabelCombobox.__dict__[f"{tab.upper()}_F"]:
                    nm_key = nm.LabelCombobox.__dict__[f"{tab.upper()}_F"][key]
                    widget_dict[nm_key].config(values=getattr(values_dict, value_attr))

    def __ini_setupVars(self) -> None:
        """
        Inicializa las variables de Tkinter y el mapeo de parámetros.
        """
        # Definimos los tipos de variables según el sufijo
        var_types = {
            'lcb': tk.StringVar,
            'lbe': tk.DoubleVar,  # Por defecto, LabelEntry es DoubleVar
            'cb': tk.StringVar
        }

        # Excepciones: Campos que deben ser StringVar en lugar de DoubleVar
        exceptions_lbe = {
            'detector_lbe11',  # Energy File Name
            'detector_lbe12',  # Charge File Name
            'main_lbe3',        # NEvents (scientific notation allowed)
            'scoring_lbe4'     # Scoring output file name
        }

        # Estructura simplificada de categorías y variables
        categories = {
            'main': {
                #'cb1': 'GeometryFile',
                #'cb2': 'PhysicFile',
                #'cb3': 'SourceFile',
                #'cb4': 'FiltersFile',
                #'cb5': 'DetectorFile',
                #'cb6': 'Ana&HistFile',
                #'cb7': 'ScoringIOCFile',
                'cb8': 'RandomSeed',
                'cb9': 'VisFile',
                'cb10': 'DeleteVisFiles',
                'lbe1': 'Seed1',
                'lbe2': 'Seed2',
                'lbe3': 'NEvents',
            },
            'geometry': {
                'lcb3': 'WorldFile',
                'lcb4': 'WorldFilled',
                'lbe1': 'SDD',
                'lbe2': 'WorldSizeBD',
                'cb1': 'DICOMGeom',
                'lcb2': 'VoxelPhantom',
                'lcb1': 'GeomtryPhantom',
                'lbe3': 'SOD',
                'cb2': 'UseJaws',
                'cb3': 'AutoSizeJaws',
                'lbe4': 'Y1JawAperture',
                'lbe5': 'Y2JawAperture',
                'lbe6': 'X1JawAperture',
                'lbe7': 'X2JawAperture',
                'lbe8': 'JawsDepth',
                'lbe9': 'DeltaZJaws',
                'lbe10': 'SJD',
                #'cb4': 'UsePhysicalDetector'
            },
            'physic_filters': {
                'lcb1': 'PhysicList',
                'lbe1': 'Range',
                'cb1': 'ApplyF1',
                'cb2': 'ApplyF2',
                'cb3': 'ApplyF3',
                'cb4': 'ApplyF4',
                #'cb5': 'ApplyF5'
            },
            'source': {
                'lcb1': 'Particle',
                'lcb2': 'Spectra',
                'lcb3': 'SpectraFilled',
                'lcb4': 'PosDistribution',
                'lcb5': 'Distribution',
                'lbe1': 'Energy',
                'lbe2': 'FocusSize',
                'lbe3': 'SourcePosX',
                'lbe4': 'SourcePosY',
                'lbe5': 'ConeAngle',
                'lbe6': 'PyramidX',
                'lbe7': 'PyramidY',
                'cb1': 'AlignSource',
                'cb2': 'AutoSizeSource'
            },
            'detector': {
                'lcb1': 'DetectorModel',
                'lcb2': 'Material',
                'lcb3': 'OutputFormat',
                'lcb4': 'OutputType',
                'lbe2': 'DetectorDepth',
                'lbe3': 'NPixelX',
                'lbe4': 'NPixelY',
                'lbe5': 'PixelSizeX',
                'lbe6': 'PixelSizeY',
                'lbe8': 'GridRatio',
                'lbe9': 'GridFrequency',
                'lbe10': 'GridStripThickness',
                'lbe11': 'OutputFilename',
                'lbe13': 'Weh',
                'cb1': 'UseAntiScatterGrid',
                'cb2': 'AutoSizeDetector'
            },
            'scoring': {
                'cb1': 'kerma',
                'cb2': 'Dose',
                #'cb3': 'MGD',
                'cb4': 'UseIOC',
                'lbe1': 'IOCx',
                'lbe2': 'IOCy',
                'lbe3': 'IOCz',
                'lcb1': 'IOCMaterial',
                'lbe5': 'IOCDistanceFromCW',
                'lbe6': 'IOCDistanceFromS',
                'lbe7': 'IOCLRPosition',
                'lbe4': 'ScoringFileName'
            }
        }

        # Generar dinámicamente self.__mapping y self.__tk_vars
        self.__mapping = {}
        self.__tk_vars = {}

        for category, variables in categories.items():
            for var_suffix, param_name in variables.items():
                var_name = f"{category}_{var_suffix}"
                
                # Determinar el tipo de variable
                var_type = next((k for k in var_types if k in var_suffix), None)
                if var_type:
                    # Si la variable está en excepciones, cambiar a StringVar
                    if var_name in exceptions_lbe:
                        self.__tk_vars[var_name] = tk.StringVar()
                    else:
                        self.__tk_vars[var_name] = var_types[var_type]()

                    self.__mapping[var_name] = param_name

    def __vincule_vars(self):
        """
        Vincula las variables de Tkinter con los elementos de la UI según su categoría,
        y configura los Checkbutton para mostrar Yes/No.
        """
        # Mapeo de categorías con los elementos UI correspondientes
        category_mapping = {
            'main': ('MAIN_FILE_F', self.__f_main_elements),
            'geometry': ('GEOMETRY_F', self.__f_geometry_elements),
            'physic_filters': ('PHYSICANDFILTERS_F', self.__f_physicfilters_elements),
            'source': ('SOURCE_F', self.__f_source_elements),
            'detector': ('DETECTOR_F', self.__f_detector_elements),
            'scoring': ('SCORING_F', self.__f_scoring_elements)
        }

        # Mapeo del tipo de variable a su widget y opción
        elements_mapping = {
            'lcb': ('LabelCombobox', 'label_combobox', 'textvariable'),
            'lbe': ('LabelEntry',     'label_entry',    'textvariable'),
            'cb' : ('CheckBoxes',     'check_box_label','variable')
        }

        for key, var in self.__tk_vars.items():
            # Determinar categoría y conjunto de widgets
            category = next((cat for cat in category_mapping if key.startswith(cat)), None)
            nm_category, widget_dict = category_mapping[category]

            # Tipo de widget y opción de config
            suffix   = key.split('_')[-1]
            prefix   = next(p for p in elements_mapping if p in key)
            _, widget_type, var_option = elements_mapping[prefix]

            # Clave en Names
            nm_dict = getattr(nm, elements_mapping[prefix][0])
            nm_key  = getattr(nm_dict, nm_category)[suffix]

            if nm_key in widget_dict[widget_type]:
                widget = widget_dict[widget_type][nm_key]

                if var_option == "variable":
                    # Configuramos Checkbutton para Yes/No
                    widget.config(
                        variable     = var,
                        textvariable = var,
                        onvalue      = nm.common.checkBoxText[0],  # "Yes"
                        offvalue     = nm.common.checkBoxText[1]   # "No"
                    )
                else:
                    # Combobox o Entry
                    widget.config(textvariable=var)

                # Reemplazo del trace_add para LabelEntry
                if prefix == "lbe":
                    entry_widget = widget  # ya obtenido correctamente

                    # Enlazar validación manual al perder el foco o pulsar Enter
                    entry_widget.bind("<FocusOut>", lambda e, key=key: self.__on_entry_validate(key))
                    entry_widget.bind("<Return>",    lambda e, key=key: self.__on_entry_validate(key))
                    entry_widget.bind("<KP_Enter>", lambda e, key=key: self.__on_entry_validate(key))  # NumPad Enter

                else:
                    # El resto sigue usando trace para CheckBoxes o Comboboxes
                    if key in self.__rebuild_summary_trigger_vars:
                        callback = lambda *_: (self.__update_full_summary(), self.__control_logic())
                        #callback = lambda *_: (self.__control_logic())
                    else:
                        callback = lambda *_: (self.__update_sim_summary(), self.__control_logic())
                        #callback = lambda *_: (self.__control_logic())

                    var.trace_add("write", callback)
            else:
                print(f"No se encontró widget para {nm_key} en {widget_type}")

    def __on_entry_validate(self, tk_key: str):
        
        param_key = self.__mapping.get(tk_key)
        var = self.__tk_vars[tk_key]

        try:
            value = var.get()

            # Validación especial para NEvents (permite notación científica)
            if param_key == "NEvents":
                if isinstance(value, str):
                    if value.strip() == "":
                        print("[INFO] Skipping NEvents: input is empty during initialization.")
                        return  # no validamos si está vacío
                    value = int(float(value.replace(",", ".")))
                else:
                    value = int(value)
                var.set(str(value))  # normalizar visualmente

            # Validación genérica para cualquier DoubleVar
            elif isinstance(var, tk.DoubleVar):
                if isinstance(value, str):
                    value = float(value.replace(",", "."))
                else:
                    value = float(value)
                var.set(value)

            # Actualiza lógica y resumen solo si todo fue correcto
            self.__update_sim_summary()
            self.__control_logic()

        except Exception as e:
            #print(f"[WARN] Invalid input for '{param_key}': '{value}' → {e}")
            messagebox.showerror("Input error", f"Invalid value for {param_key}: {value}")

    def __load_default_setupParams(self) -> None:
        
        self.params={}
        
        self.params=self.__simSetup.load_SimConfg_from_json(
            simConfig_file_path=path.SimSetup.default_cfg
        )
        #print(self.params)
   
    def __update_widget_values(self):
        """
        Actualiza los valores de los widgets con los parámetros actuales,
        mapeando 0/1 → No/Yes en los checkboxes.
        """
        on, off = nm.common.checkBoxText  # ("Yes", "No")
        for tk_key, param_key in self.__mapping.items():
            var = self.__tk_vars[tk_key]
            val = self.params.get(param_key, "")

            # Si es checkbox (mismo StringVar que textvariable/variable):
            # detectarlo por sufijo '_cb'
            if '_cb' in tk_key:
                # Tratamos val numérico o booleano
                truthy = val in (True, 1, '1', on)  
                var.set(on if truthy else off)
            else:
                # resto de widgets: combobox, entries...
                var.set(val)
        
        #self.__control_logic()

    def __get_updated_params(self):
        updated_params = {}

        for tk_key, param_key in self.__mapping.items():
            try:
                value = self.__tk_vars[tk_key].get()
            except Exception as e:
                print(f"[ERROR] Failed to retrieve value from '{tk_key}' (param: '{param_key}'): {e}")
                raise

            # Special handling for NEvents
            if param_key == "NEvents":
                if isinstance(value, str):
                    if value.strip() == "":
                        #print("[INFO] Skipping NEvents: input is empty during init.")
                        continue  # No lo añadimos al dict, se omitirá
                    try:
                        value = int(float(value.replace(',', '.')))
                    except Exception as e:
                        print(f"[ERROR] Invalid value for NEvents: '{value}' → {e}")
                        value = 100000  # o puedes continuar sin añadirlo
                else:
                    value = int(value)

            elif isinstance(value, bool):
                value = "Yes" if value else "No"

            updated_params[param_key] = value

        return updated_params

    def __update_summary_cfg_visibility(self):
        """
        Actualiza la visibilidad (show) de los labels en la configuracion de summary segun los parametros actuales.
        """
        params = self.__get_updated_params()

        for item in self.__summary_frame_cfg:
            label_text = item.get('label')

            if label_text is None:
                continue

            # Aquí defines las condiciones
            if label_text == nm.Labels.SUMMARY_F['lb42']:  # 'Filter 1 - Kill all electrons:'
                item['show'] = params.get('ApplyF1', 'No') == 'Yes'
            elif label_text == nm.Labels.SUMMARY_F['lb43']:  # 'Filter 2 - Kill secondary tracks:'
                item['show'] = params.get('ApplyF2', 'No') == 'Yes'
            elif label_text == nm.Labels.SUMMARY_F['lb44']:  # 'Filter 3 - Kill scattered photons:'
                item['show'] = params.get('ApplyF3', 'No') == 'Yes'
            elif label_text == nm.Labels.SUMMARY_F['lb45']:  # 'Filter 4 - Kill photons at the jaws:'
                item['show'] = params.get('ApplyF4', 'No') == 'Yes'
            else:
                # Si no hay regla, lo dejas como estaba
                item.setdefault('show', True)
    
    def __update_sim_summary(self, foreground_color="yellow"):
        """
        Actualiza el resumen de la simulación con los parámetros actuales.
        Soporta reglas dinámicas y mapeos directos en un solo diccionario.
        """
        current_params = self.__get_updated_params()

        def safe_config(widget, **kwargs):
            if widget.winfo_exists():
                widget.config(**kwargs)


        for _, element_group in self.__summary_frame_elements.items():
            for label_text, label_widget in element_group.items():
                rule = self.__summary_map.get(label_text)
                if rule:
                    if callable(rule):
                        new_value = rule(current_params)
                    else:
                        new_value = current_params.get(rule, '')

                    # 👉 Si es lb21, aplicar notación científica
                    if label_text == nm.Labels.SUMMARY_F['lb21']:
                        try:
                            new_value = float(new_value)
                            new_value = f"{new_value:.2e}"  # 2 cifras decimales en notación científica
                        except (ValueError, TypeError):
                            pass  # deja el valor como esté si no es convertible

                    new_text = f"{label_text} {new_value}"
                    current_text = label_widget.cget("text")

                    if current_text != new_text:
                        label_widget.config(text=new_text, foreground=foreground_color)
                        self.__root.after(1000, lambda w=label_widget: safe_config(w, foreground="white"))

        
        label = self.__summary_frame_elements["label"][nm.Labels.SUMMARY_F['lb7']]
        texto_actual = label.cget("text")
        label.config(text="Configuration applied: NO")

    def __update_full_summary(self):
        # 1. Refrescamos los parámetros
        current_params = self.__get_updated_params()

        # 2. Actualizamos visibilidad según condiciones
        self.__update_summary_cfg_visibility()

        # 3. Limpiamos el frame de resumen (destruimos todos los widgets)
        for widget in self.__summary_frame_container.winfo_children():
            widget.destroy()

        # 4. Reconstruimos el resumen desde 0
        self.__summary_frame_elements = cwgf.populate_control_panel(
            root=self.__summary_frame_container,
            list_cfg=self.__summary_frame_cfg
        )
        self.__main_container.update_idletasks()

        # 5. Actualizamos los textos de las labels visibles
        self.__update_sim_summary(foreground_color="white")
    
    def __to_bool(self, val):
        """
        Convierte un valor a booleano de forma robusta.
        Reconoce strings como 'Yes', 'No', 'true', 'false', etc.
        """
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            val_lower = val.strip().lower()
            if val_lower in ("yes", "true", "1"):
                return True
            if val_lower in ("no", "false", "0"):
                return False
        return bool(val)  # fallback
    
    def __control_logic(self) -> None:
        if hasattr(self, "_is_updating_logic") and self._is_updating_logic:
            return  # Evita recursión

        self._is_updating_logic = True  # Activamos bandera

        try:
            for rule in Rules.setup_gui_rules:
                trigger = rule["trigger"]
                expected = rule["expected"]
                action = rule["action"]
                targets = rule["targets"]
                value = rule.get("value", None)

                var = self.__tk_vars.get(trigger)
                if var is None:
                    continue

                raw_val = var.get()
                trigger_bool = self.__to_bool(raw_val)
                expected_bool = self.__to_bool(expected)

                apply_action = (trigger_bool == expected_bool)

                for target in targets:
                    widget = self.__get_widget_by_key(target)
                    target_var = self.__tk_vars.get(target)

                    if action == "disable":
                        if widget:
                            widget.configure(state="disabled" if apply_action else "normal")

                    elif action == "normal":
                        if widget:
                            widget.configure(state="normal" if apply_action else "disabled")

                    elif action == "set":
                        if apply_action and target_var:
                            target_var.set(value)

        finally:
            self._is_updating_logic = False  # Desactivamos bandera
   
    def __get_widget_by_key(self, key: str):
        """
        Dado un nombre como 'geometry_lbe4', devuelve el widget interactivo asociado
        (por ejemplo: el Entry dentro de un LabelEntry, el Combobox dentro de un LabelCombobox, etc.).
        """

        try:
            section, suffix = key.split('_', 1)
        except ValueError:
            print(f"[ERROR] Formato de clave inválido: {key}")
            return None

        # Alias para mapear correctamente las secciones al atributo de nm
        section_aliases = {
            "main": "MAIN_FILE_F",
            "geometry": "GEOMETRY_F",
            "physic_filters": "PHYSICANDFILTERS_F",
            "source": "SOURCE_F",
            "detector": "DETECTOR_F",
            "scoring": "SCORING_F"
        }

        # Diccionarios de widgets por sección
        element_map = {
            'main': self.__f_main_elements,
            'geometry': self.__f_geometry_elements,
            'physic_filters': self.__f_physicfilters_elements,
            'source': self.__f_source_elements,
            'detector': self.__f_detector_elements,
            'scoring': self.__f_scoring_elements
        }

        # Tipos de widgets
        widget_types = {
            'lbe': ('label_entry', nm.LabelEntry),
            'lcb': ('label_combobox', nm.LabelCombobox),
            'cb': ('check_box_label', nm.CheckBoxes)
        }

        for prefix in widget_types:
            if suffix.startswith(prefix):
                if section in element_map:
                    dict_name, nm_class = widget_types[prefix]
                    widget_dict = element_map[section][dict_name]

                    try:
                        section_key = section_aliases.get(section, f"{section.upper()}_F")
                        widget_name = getattr(nm_class, section_key)[suffix]
                        widget = widget_dict.get(widget_name)

                        # Si es un diccionario compuesto (como LabelCombobox), devolvemos el control interactivo
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

    ######################
    # GUI filled methods #
    # Private methods    #
    ######################

    def __build_main_container(self):
        self.__main_container = ttk.Frame(self.__root)
        self.__main_container.grid(row=0, column=0, sticky="nsew")
        self.__root.rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=1)

    def __setup_main_window(self) -> None:
        """
        Creamos el contenedor principal principal dentro del root (Ventana principal).        
        """       
        self.__main_frames = cwgf.populate_elemnts_panels_dev(
            root=self.__main_container,
            grid=[1,3],
            panel_configs=self.__main_window_cfg
        )

        self.__main_container.update_idletasks()
    
    def __setup_control_panel(self) -> None:
        """
        Sets up and positions the control panel in the top-left corner of the GUI.

        This method configures the layout of the control panel frame, ensuring
        horizontal expansion for its first column. It then populates the control
        panel with buttons or other elements based on a predefined configuration.

        The control panel is created within the 'panel_control_frame' section of
        the main frames and uses the `populate_control_panel` function to generate
        its contents.

        Returns:
            None
        """
        
        frame = self.__main_frames['panel_control_frame']['frame_content']

        # Asegurar expansión horizontal de la columna 0
        frame.columnconfigure(0, weight=1)

        # Crear los botones dentro del contenedor
        self.__pc_elements = cwgf.populate_control_panel(
            root=frame, 
            list_cfg=self.__pc_elements_cfg, 
            horizontal=False
        )

        self.__main_container.update_idletasks()
 
    def __setup_notebook_panel(self) -> None:
        """
        Crea el Notebook vacío con pestañas y lo expande correctamente en la interfaz.
        """
        frame = self.__main_frames['notebook_frame']['frame_content']

        self.__nb, self.__nb_elements = awgf.create_empty_notebook(
            parent_frame=frame,
            tabs_config=self.__nb_tabs
        )

        # Asegurar que el Notebook se expanda dentro de su frame
        self.__nb.grid(row=0, column=0, sticky="nsew")

        self.__main_container.update_idletasks()

    def __setup_sim_summary_frame(self) -> None:
        """
        Crea la pestaña de resumen de simulación que muestra los principales aspectos 
        seleccionados de la misma
        """

        frame = self.__main_frames['summary_frame']['frame_content']
        frame.grid(sticky="nsew")
        # Asegurar expansión horizontal de la columna 0
        frame.columnconfigure(0, weight=1)

        self.__summary_frame_container = frame  

        # Creamos los elementos del panel de resumen
        self.__summary_frame_elements = cwgf.populate_control_panel(
            root=frame,
            list_cfg=self.__summary_frame_cfg
        )

        self.__main_container.update_idletasks()
    
    # Notebook frames
    def __setup_main_file_frame(self) -> None:
        
        frame = self.__nb_elements['Main File']
        
        self.__f_main_elements = cwgf.populate_control_panel(
             root = frame,
             list_cfg = self.__f_main_cfg
         )
                
        # Asegurar que los elementos internos no bloqueen la expansión
        for widget in frame.winfo_children():
            widget.grid_configure(sticky="nsew")
        
        self.__root.update_idletasks()
    
    def __setup_geometry_frame(self) -> None:
        
        frame = self.__nb_elements['Geometry']
        
        self.__f_geometry_elements = cwgf.populate_control_panel(
            root = frame,
            list_cfg=self.__f_geometry_cfg
        )
        
         # Asegurar que los elementos internos no bloqueen la expansión
        for widget in frame.winfo_children():
            widget.grid_configure(sticky="nsew")
        
        self.__root.update_idletasks()
    
    def __setup_physicANDfilters_frame(self) -> None:
        
        frame = self.__nb_elements['Physic & Filters']
        
        self.__f_physicfilters_elements = cwgf.populate_control_panel(
             root = frame,
             list_cfg = self.__f_physicfilters_cfg
         )
        
        # Asegurar que los elementos internos no bloqueen la expansión
        for widget in frame.winfo_children():
            widget.grid_configure(sticky="nsew")
        
        self.__root.update_idletasks()
    
    def __setup_scoring_frame(self) -> None:
        
        frame = self.__nb_elements['Scoring']
        
        self.__f_scoring_elements = cwgf.populate_control_panel(
            root = frame,
            list_cfg=self.__f_scoring_cfg
        )
        
         # Asegurar que los elementos internos no bloqueen la expansión
        for widget in frame.winfo_children():
            widget.grid_configure(sticky="nsew")
        
        self.__root.update_idletasks()
        
    def __setup_source_frame(self) -> None:
        
        frame = self.__nb_elements['Source']
        
        self.__f_source_elements = cwgf.populate_control_panel(
            root = frame,
            list_cfg=self.__f_source_cfg
        )
        
         # Asegurar que los elementos internos no bloqueen la expansión
        for widget in frame.winfo_children():
            widget.grid_configure(sticky="nsew")
        
        self.__root.update_idletasks()
    
    def __setup_detector_frame(self) -> None:
        
        frame = self.__nb_elements['Detector']
        
        self.__f_detector_elements = cwgf.populate_control_panel(
            root = frame,
            list_cfg=self.__f_detector_cfg
        )
        
         # Asegurar que los elementos internos no bloqueen la expansión
        for widget in frame.winfo_children():
            widget.grid_configure(sticky="nsew")
        
        self.__root.update_idletasks()
    
    ##################
    # Button methods #
    ##################
        
    def apply_cfg(self):
        #master=self.master       
         
        self.__simSetup.sim_params = self.__get_updated_params()
        self.__simSetup.run_setup()

        label = self.__summary_frame_elements["label"][nm.Labels.SUMMARY_F['lb7']]
        texto_actual = label.cget("text")
        label.config(text="Configuration applied: YES")

    def save_config(self):
        """
        Guarda toda la configuración actual en un archivo JSON,
        agrupando los parámetros según el prefijo de sus claves de interfaz (main, geometry, etc.).
        """
        updated_params = self.__get_updated_params()
        
        # Crear estructura agrupada automáticamente
        grouped_params = {}
        for tk_key, param_key in self.__mapping.items():
            prefix = tk_key.split('_')[0]  # "main", "geometry", etc.
            grouped_params.setdefault(prefix, {})[param_key] = updated_params.get(param_key)

        # Guardar como JSON
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialdir='GUI/configs',
            initialfile="_simConfg.json",
            title="Guardar configuración"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(grouped_params, f, indent=4)
                messagebox.showinfo("Saved", "Configuration saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save the configuration:\n{e}")

    def load_cfg(self):

        file_path = filedialog.askopenfilename(
            initialdir=r'GUI/configs',
        ) # Abre el cuadro de diálogo para seleccionar un archivo
        
        sim_run = SimSetup()
        self.params=sim_run.load_SimConfg_from_json(file_path)

        self.__update_widget_values()
    
    def open_input_file(self):
        try:
            file_key = self.__pc_elements['label_combobox'][nm.LabelCombobox.SIM_SETUP_CP['lcb1']].get()
            #print("Selected file key:", file_key)

            if file_key not in path.SimSetup.destiny_folder:
                raise KeyError(f"'{file_key}' not found in path.SimSetup.destiny_folder")

            file_path = path.SimSetup.destiny_folder[file_key]
            #print("Resolved path:", file_path)

            if os.path.exists(file_path):
                try:
                    os.startfile(file_path)  # Only works on Windows
                except AttributeError:
                    # Fallback for Linux/macOS
                    import subprocess
                    subprocess.run(["xdg-open", file_path])
            else:
                messagebox.showerror("Error", f"The file does not exist at the path:\n{file_path}")

        except Exception as e:
            print("Exception:", e)
            messagebox.showerror("Error", str(e))
    
    def debug_file(self):
        """
        Método para generar el archivo de depuración principal.
        """
        self.__simSetup.sim_params = self.__get_updated_params()
        self.__simSetup.run_debug_file()
    
    def volver(self) -> None:
        """
        Método para volver a la interfaz principal.
        """
        if self.__main_container:
            self.__main_container.destroy()

        self.__callback_volver()  # Llamar al callback para reconstruir la interfaz principal
    
    def cal_Nevents(self):
        """
        Método para calcular el número de eventos.
        """
        new_window = tk.Toplevel()
        new_window.title("NEvents_Calculator")
        Nevents_cal(new_window)


        