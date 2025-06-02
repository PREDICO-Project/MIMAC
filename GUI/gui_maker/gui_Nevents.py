import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from resources.pyresources.configs import Cfgs as cfg
from src.wg_factory.cplWidget_fc import COMPLEXWIDGETFactory as cwgf
from src.gui_handler.window_handler import WINDOWHandler as wh
from resources.pyresources.names import Names as nm
from resources.pyresources.paths import base_paths
from resources.pyresources.lists import Lists as lst

class Nevents_cal():

    ###############
    # Constructor #
    ###############
    
    def __init__(self, root:tk.Tk) -> None:

        self.__root = root  # Save the reference to the passed root

        # variable initialization
        self.__ini_vars()
        self.__ini_guiElements_cfg()

        # Main window configuration
        self.__build_main_container()
        self.__setup_main_window()

        # Populate frames with elements
        self.__setup_control_panel()
        self.__setup_spectrum_frame()
        self.__setup_calculate_frame()

        # Actions
        self.__ini_guiElements_Actions()
        self.__ini_guiComboBox_content()

        # Aseguramos que todos los widgets estén bien colocados
        self.__root.update_idletasks()

        # Centrar la ventana con tamaño ajustado al contenido real       
        self.__root.geometry("")
        wh.window_position(self.__root,2,3)
    
    ##########################
    # Initialization methods #
    # Private methods        #
    ##########################

    def __ini_vars(self) -> None:
        """
        Initialize the variables for the GUI elements.
        """

        # Main conbtainer
        self.__main_container = None
        self.__main_container_cfg = None
        self.__main_container_elements = None

        # Control_panel cfg And elements
        self.__pc_elements = None
        self.__pc_cfg = None

        # Spectrm data frame cfg And elements
        self.__spectrum_frame_elements = None
        self.__spectrum_frame_cfg = None

        # Calculate frame cfg And elements
        self.__calculate_frame_elements = None
        self.__calculate_frame_cfg = None

        # Spectrum data
        self.__spectrum_data = {}


    def __ini_guiElements_cfg(self) -> None:
        """
        Initialize the GUI elements configuration.
        """

        # Load the configuration for the GUI elements
        self.__main_container_cfg = cfg.Nevents.main_window_cfg
        self.__pc_cfg = cfg.Nevents.pc_cfg
        self.__spectrum_frame_cfg = cfg.Nevents.spectrum_cfg
        self.__calculate_frame_cfg = cfg.Nevents.calculate_cfg
    
    def __ini_guiElements_Actions(self) -> None:

        self.__pc_elements['button'][nm.Buttons.NEVENTS_CP['bt1']].config(command=self.close)
        self.__calculate_frame_elements['button'][nm.Buttons.NEVENTS_Calculate['bt1']].config(command=self.calculate_events_from_mAs)
        self.__calculate_frame_elements['button'][nm.Buttons.NEVENTS_Calculate['bt2']].config(command=self.calculate_mAs_from_events)
        # Bind action to selection change in combobox
        self.__pc_elements['label_combobox'][nm.LabelCombobox.NEVENTS_CP['lcb1']].bind(
            '<<ComboboxSelected>>', 
            self.__on_spectrum_selected
        )


    def __ini_guiComboBox_content(self) -> None:
        
        """
        Asigna dinámicamente valores a los combobox en diferentes pestañas usando un diccionario de mapeo.
        """
        # Inicializamos el combobox del panel de control con los ficheros inputs
        self.__pc_elements['label_combobox'][nm.LabelCombobox.NEVENTS_CP['lcb1']].config(values=list(lst.Source.spectra))
    
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
        self.__main_container_elements = cwgf.populate_elemnts_panels_dev(
            root=self.__main_container,
            grid=[1,3],
            panel_configs=self.__main_container_cfg
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
        
        frame = self.__main_container_elements['panel_control_frame']['frame_content']

        # Asegurar expansión horizontal de la columna 0
        frame.columnconfigure(0, weight=1)

        # Crear los botones dentro del contenedor
        self.__pc_elements = cwgf.populate_control_panel(
            root=frame, 
            list_cfg=self.__pc_cfg, 
            horizontal=False
        )

        self.__main_container.update_idletasks()
    
    def __setup_spectrum_frame(self) -> None:
        """
        Sets up and positions the spectrum frame in the top-right corner of the GUI.

        This method configures the layout of the spectrum frame, ensuring
        horizontal expansion for its first column. It then populates the spectrum
        frame with buttons or other elements based on a predefined configuration.

        The spectrum frame is created within the 'spectrum_frame' section of
        the main frames and uses the `populate_control_panel` function to generate
        its contents.

        Returns:
            None
        """
        
        frame = self.__main_container_elements['spectrum_frame']['frame_content']

        # Asegurar expansión horizontal de la columna 0
        frame.columnconfigure(0, weight=1)

        # Crear los botones dentro del contenedor
        self.__spectrum_frame_elements = cwgf.populate_control_panel(
            root=frame, 
            list_cfg=self.__spectrum_frame_cfg, 
            horizontal=False
        )

        self.__main_container.update_idletasks()
    
    def __setup_calculate_frame(self) -> None:
        """
        Sets up and positions the calculate frame in the bottom-right corner of the GUI.

        This method configures the layout of the calculate frame, ensuring
        horizontal expansion for its first column. It then populates the calculate
        frame with buttons or other elements based on a predefined configuration.

        The calculate frame is created within the 'calculate_frame' section of
        the main frames and uses the `populate_control_panel` function to generate
        its contents.

        Returns:
            None
        """
        
        frame = self.__main_container_elements['calculate_frame']['frame_content']

        # Asegurar expansión horizontal de la columna 0
        frame.columnconfigure(0, weight=1)

        # Crear los botones dentro del contenedor
        self.__calculate_frame_elements = cwgf.populate_control_panel(
            root=frame, 
            list_cfg=self.__calculate_frame_cfg, 
            horizontal=False
        )

        self.__main_container.update_idletasks()
    
    ####################
    # Workflow methods #
    ####################

    def __on_spectrum_selected(self, event=None):
        """
        Callback when a spectrum is selected from the combobox.
        Loads metadata from the .in file and updates the GUI labels in the spectrum frame.
        """
        combobox = self.__pc_elements['label_combobox'][nm.LabelCombobox.NEVENTS_CP['lcb1']]
        selected_file = combobox.get()

        file_path = os.path.join(base_paths.spectra, selected_file)
        self.__spectrum_data.clear()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#'):
                        line = line[1:].strip()
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            if key == 'kvp':
                                value = int(value)
                            elif key in ['filter_thickness_mm', 'energy_mean_keV', 'kerma_SP_uGy_per_mAs', 'kerma_MC_Gy_per_photon']:
                                try:
                                    value = float(value)
                                except ValueError:
                                    value = None
                            self.__spectrum_data[key] = value
                    elif line.strip() == '' or not line.startswith('#'):
                        break
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return

        # Calculate conversion factor if both kerma values are available
        kerma_sp = self.__spectrum_data.get('kerma_SP_uGy_per_mAs')
        kerma_mc = self.__spectrum_data.get('kerma_MC_Gy_per_photon')

        if kerma_sp is not None and kerma_mc is not None and kerma_mc > 0:
            conversion_factor = int(round((kerma_sp * 1e-6) / kerma_mc))  # rounded to nearest int
            self.__spectrum_data['conversion_factor_N_per_mAs'] = conversion_factor
        else:
            self.__spectrum_data['conversion_factor_N_per_mAs'] = 'N/A'


        # Access the labels
        lb = self.__spectrum_frame_elements['label']

        # Helper function to append value to existing base label text
        def update_label(key_label, value):
            widget = lb[nm.Labels.NEVENTS_Spectrum[key_label]]
            base_text = widget.cget('text').split(':')[0]
            widget.config(text=f"{base_text}: {value}")

        # Update each label
        update_label('lb21', self.__spectrum_data.get('kvp', 'N/A'))
        update_label('lb22', selected_file)
        update_label('lb23', self.__spectrum_data.get('anode', 'N/A'))
        update_label('lb24', self.__spectrum_data.get('filter_material', 'N/A'))
        update_label('lb25', self.__spectrum_data.get('filter_thickness_mm', 'N/A'))
        update_label('lb26', self.__spectrum_data.get('energy_mean_keV', 'N/A'))
        update_label('lb31', self.__spectrum_data.get('kerma_SP_uGy_per_mAs', 'N/A'))
        update_label('lb32', self.__spectrum_data.get('kerma_MC_Gy_per_photon', 'N/A'))
        update_label('lb33', self.__spectrum_data.get('conversion_factor_N_per_mAs', 'N/A'))


    ##################
    # Button methods #
    ##################

    def calculate_events_from_mAs(self):
        """
        Calculate and display the number of events required for a given mAs.
        Shows integer values in summary label (lb22), and scientific notation in lb23 and lb24.
        """
        entry_widget = self.__calculate_frame_elements['label_entry'][nm.LabelEntry.NEVENTS_Calculate['lbe2']]
        n_runs_widget = self.__calculate_frame_elements['label_entry'][nm.LabelEntry.NEVENTS_Calculate['lbe1']]

        try:
            mAs = float(entry_widget.get())
            n_runs = int(n_runs_widget.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for mAs and threads.")
            return

        corrected = False
        if mAs <= 0:
            mAs = 1.0
            corrected = True
        if n_runs <= 0:
            n_runs = 1
            corrected = True

        if corrected:
            messagebox.showinfo("Default Values Applied", "mAs and/or threads were ≤ 0. Defaulted to 1.")

        conv_factor = self.__spectrum_data.get('conversion_factor_N_per_mAs')
        if isinstance(conv_factor, int):
            total_events = int(round(mAs * conv_factor))
            events_per_run = total_events // n_runs

            # Format for scientific notation
            total_events_sci = f"{total_events:.2e}"
            events_per_run_sci = f"{events_per_run:.2e}"

            lb = self.__calculate_frame_elements['label']

            # Integer summary (lb22)
            lb[nm.Labels.NEVENTS_Calculate['lb22']].config(
                text=f"- {events_per_run} ev/thread × {n_runs} threads = {total_events} events"
            )

            # Scientific notation
            lb[nm.Labels.NEVENTS_Calculate['lb23']].config(  # TOTAL events
                text=f"- Total events (sci): {total_events_sci}"
            )
            lb[nm.Labels.NEVENTS_Calculate['lb24']].config(  # Events per thread
                text=f"- Events per thread (sci): {events_per_run_sci}"
            )
        else:
            messagebox.showerror("Missing Data", "Conversion factor is missing or invalid.")

    def calculate_mAs_from_events(self):
        """
        Given a number of simulated events, calculate and display the equivalent mAs.
        Uses the conversion factor from self.__spectrum_data.
        Displays the result in the label 'lb31'. If input is invalid or zero, defaults to 1.
        """
        entry_widget = self.__calculate_frame_elements['label_entry'][nm.LabelEntry.NEVENTS_Calculate['lbe3']]  # Entry for total events

        try:
            total_events = int(entry_widget.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of events (integer).")
            return

        if total_events <= 0:
            total_events = 1
            messagebox.showinfo("Default Value Applied", "Number of events was ≤ 0. Defaulted to 1.")

        conv_factor = self.__spectrum_data.get('conversion_factor_N_per_mAs')
        if isinstance(conv_factor, int) and conv_factor > 0:
            mAs = total_events / conv_factor

            # Update label lb31 with result
            lb = self.__calculate_frame_elements['label']
            target_label = lb[nm.Labels.NEVENTS_Calculate['lb32']]
            base_text = target_label.cget('text').split(':')[0]
            target_label.config(text=f"{base_text} {mAs:.2f} mAs from {total_events} events")
        else:
            messagebox.showerror("Missing Data", "Conversion factor is missing or invalid.")


    def close(self):
        """
        Close the Nevents_cal window.
        """
        self.__root.destroy()