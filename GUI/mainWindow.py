import tkinter as tk
from tkinter import ttk
from resources.pyresources.names import Names as nm
from resources.pyresources.paths import Paths as path
from src.tool_handler.panelControl_handler import PANELCONTROLHandler as pc
from src.tool_handler.path_handler import PATHHandler as path_handler
from src.gui_handler.window_handler import WINDOWHandler as wh
from src.wg_factory.cplWidget_fc import COMPLEXWIDGETFactory as cwgf
from src.gui_handler.theme_handler import THEMEHandler as thm
from gui_maker.gui_sim_setup import sim_setup_gui
from resources.pyresources.configs import Cfgs as cfg
from gui_maker.gui_raw2g4dcm import raw2g4dcm_gui
from gui_maker.gui_image import image_gui


class MainWindow():

    ###############
    # Constructor #
    ###############

    def __init__(self) -> None :

        # Main Window
        self.__root = tk.Tk()
        self.__root.title(nm.Windows.MAIN)

        # Configuramos el estilo
        style = ttk.Style()
        #style.theme_use("clam")
        thm().configure_dark_mode()
        #thm().configure_light_mode()

        # Vars initialization
        self.__ini_vars()
        self.__ini_guiElements_cfg()

        # Main window configuration
        self.__setup_main_window()

        # Panel control setup
        self.__setup_control_panel()
        
        # Acciones
        self.__ini_guiElements_Actions()

        #Centramos la ventana
        self.__root.geometry("")  # Hace que la ventana se ajuste automáticamente
        wh.centrar_ventana(self.__root)


        self.__root.mainloop()

    #####################
    # Secondary methods #
    # Private methods   #
    #####################

    def __ini_vars(self) -> None:

        # Elements AND cfgs
        self.__elements = None
        self.__elements_cfg = None
    
    def __ini_guiElements_cfg(self) -> None:

        self.__elements_cfg = cfg.MainWindow.main_cfg
        
    def __ini_guiElements_Actions(self) -> None:
        
        self.__elements['button'][nm.Buttons.MAIN_CP['bt1']].config(command=self.setup_simulation)
        self.__elements['button'][nm.Buttons.MAIN_CP['bt3']].config(command=self.phantom_setup) 
        self.__elements['button'][nm.Buttons.MAIN_CP['bt2']].config(command=self.image_setup)
        
    def __volver_callback(self) -> None:
        """
        Reconstruye la interfaz principal sin reiniciar mainloop.
        """
        # 1) Título
        self.__root.title(nm.Windows.MAIN)

        # 2) Limpiar todo el contenido anterior
        for w in self.__root.winfo_children():
            w.destroy()

        # 3) Reconstruir tu UI principal
        self.__ini_vars()
        self.__ini_guiElements_cfg()
        self.__setup_main_window()
        self.__setup_control_panel()
        self.__ini_guiElements_Actions()

        # 4) Ajustar geometría y centrar
        self.__root.update_idletasks()
        self.__root.geometry("")           # autoreajusta al layout actual
        wh.centrar_ventana(self.__root)    # centra en pantalla
    
    #############################
    # Creación Interfaz gráfica #
    # Métodos Privados          #
    #############################

    def __setup_main_window(self) -> None:
        """
        Creamos el contenedor principal principal dentro del root (Ventana principal).        
        """       
       
        # Creamos el main_frame
        self.__main_frame = ttk.Frame(self.__root, style='TFrame')        
        self.__main_frame.pack(fill=tk.BOTH, expand=True)

        self.__root.update_idletasks()

    def __setup_control_panel(self) -> None:
        """
        Crea los paneles de botones dinámicamente según la configuración en self.__panels_config.
        """          
        # Configurar la cuadrícula principal:
        self.__main_frame.rowconfigure(0, weight=1)  # Espacio superior -> EXPANDIBLE
        self.__main_frame.rowconfigure(1, weight=0)  # Panel de control -> FIJO
        self.__main_frame.rowconfigure(2, weight=1)  # Espacio inferior -> EXPANDIBLE
        self.__main_frame.columnconfigure(0, weight=1)  # Espacio izquierdo -> EXPANDIBLE
        self.__main_frame.columnconfigure(1, weight=0)  # Panel de control -> FIJO
        self.__main_frame.columnconfigure(2, weight=1)  # Espacio derecho -> EXPANDIBLE

        panel_control_frame = ttk.Frame(self.__main_frame, style='TFrame')
        panel_control_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)     

        # Crear los botones dentro del contenedor
        self.__elements = cwgf.populate_control_panel( 
            root=panel_control_frame, 
            list_cfg=self.__elements_cfg, 
            horizontal=False
        )

        self.__root.update_idletasks()

    ###############################
    # Metodos de Acción (Botones) #
    # Métodos Públicos            #
    ###############################
    
    def setup_simulation(self) -> None:
        
        # Destruir el contenido actual
        for widget in self.__main_frame.winfo_children():
            widget.destroy()
        
        # Alternativa: Destruir el `main_frame` completamente y recrearlo
        self.__main_frame.destroy()        

        sim_setup_gui(self.__root, callback_volver=self.__volver_callback)
    
    def phantom_setup(self) -> None:
        
        # Destruir el contenido actual
        for widget in self.__main_frame.winfo_children():
            widget.destroy()
        
        # Alternativa: Destruir el `main_frame` completamente y recrearlo
        self.__main_frame.destroy()
     
        raw2g4dcm_gui(self.__root, callback_volver=self.__volver_callback)
    
    def image_setup(self) -> None:
        
        # Destruir el contenido actual
        for widget in self.__main_frame.winfo_children():
            widget.destroy()
        
        # Alternativa: Destruir el `main_frame` completamente y recrearlo
        self.__main_frame.destroy()

        image_gui(self.__root, callback_volver=self.__volver_callback)

if __name__ == "__main__":
    MainWindow()