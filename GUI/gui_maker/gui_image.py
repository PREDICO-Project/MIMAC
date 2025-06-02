import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import SimpleITK as sitk
from PIL import Image, ImageTk
from resources.pyresources.names import Names as nm
from resources.pyresources.configs import Cfgs as cfg
from resources.pyresources.paths import Paths as paths
from resources.pyresources.lists import Lists as lst
from src.wg_factory.cplWidget_fc import COMPLEXWIDGETFactory as cwgf
from src.gui_handler.window_handler import WINDOWHandler as wh
import numpy as np
from tqdm import tqdm
from scipy.signal import convolve2d
import pydicom
try:
    from pydicom._storage_sopclass_uids import DigitalMammographyXRayImageStorageForProcessing
except:
    from pydicom.uid import DigitalMammographyXRayImageStorageForProcessing


class image_gui():

    ###############
    # Constructor #
    ###############

    def __init__(self, root:tk.Tk, callback_volver: callable ) -> None:

        self.__root = root  # Guardar la referencia al root pasado 
        self.__root.title(nm.Windows.IMAGE) 
        self.__callback_volver = callback_volver  # Guardar la referencia del callback para "Volver"

        #Inicializa variables
        self.__ini_vars()
        self.__ini_guiElements_cfg()

        # Main window configuration
        self.__setup_main_window()
        
        # Panel control setup
        self.__setup_control_panel()

        # Initialize states
        
        self.__ini_guiElements_states()
        self.__ini_guiElements_defaultValues()
      
        # Visualize frame setup

        # Actions
        self.__ini_guiElements_Actions()        

        #Centramos la ventana
        self.__root.update_idletasks()
        #self.__root.geometry("")  # Hace que la ventana se ajuste automáticamente
        wh.maximizar_ventana(self.__root)

        self.__root.mainloop()
    
    ##########################
    # Initialization methods #
    # Private methods        #
    ##########################

    def __ini_vars(self) -> None:

        # Control_panel cfg And elements
        self.__pc1_elements = None
        self.__pc1_elements_cfg = None
        self.__pc2_elements = None
        self.__pc2_elements_cfg = None
        self.__pc3_elements = None
        self.__pc3_elements_cfg = None
        self.__vis_elements =None
        self.__vis_elements_cfg = None

        self.__pc4_elements = None
        self.__pc4_elements_cfg = None


        # Execution variables
        self.__file_path = None
        self.__image = None
        self.__array = None

        # Tkinter variables
        self.__magnitude = tk.StringVar()
        self.__mean_noise = tk.DoubleVar()
        self.__Swank_factor = tk.DoubleVar()
        self.__kernel_size = tk.IntVar()
        self.__kernel_sigma = tk.DoubleVar()
        self.__norm_method  = tk.StringVar()
        self.__apply_kernel = tk.StringVar()

        # Json default values
        json_path = paths.ImageGUI.default_config

        # Other variables
        self.__count = 0    

        with open(json_path) as f:
            d = json.load(f)
            self.__magnitude.set(d['main_parameters']['Magnitude'])
            self.__mean_noise.set(d['main_parameters']['MeanElectronicNoise'])
            self.__Swank_factor.set(d['main_parameters']['SwankFactor'])
            self.__kernel_size.set(d['main_parameters']['KernelSize'])
            self.__kernel_sigma.set(d['main_parameters']['KernelSigma'])
            self.__norm_method.set(d['main_parameters']['NormMethod'])
            self.__apply_kernel.set(d['main_parameters']['ApplyKernel'])

    def __ini_guiElements_cfg(self) -> None:
        """
        Initializes the configuration for GUI elements by assigning the respective
        configuration settings from the `cfg.ImageWindow` module to instance variables.
        This method sets up the following configurations:
        - `__pc1_elements_cfg`: Configuration for the first control panel (pc1).
        - `__pc2_elements_cfg`: Configuration for the second control panel (pc2).
        - `__pc3_elements_cfg`: Configuration for the third control panel (pc3).
        - `__vis_elements_cfg`: Configuration for visualization settings.
        - `__pc4_elements_cfg`: Configuration for the summary view.
        Returns:
            None
        """
        
        self.__pc1_elements_cfg = cfg.ImageWindow.pc_cfg
        self.__pc2_elements_cfg = cfg.ImageWindow.pc2_cfg
        self.__pc3_elements_cfg = cfg.ImageWindow.pc3_cfg
        self.__vis_elements_cfg = cfg.ImageWindow.vis_cfg
        self.__pc4_elements_cfg = cfg.ImageWindow.summary_cfg

    def __ini_guiElements_states(self) -> None:
        """
        Initializes the states of various GUI elements to 'disabled'.
        This method configures the state of buttons, label-entry fields, checkboxes, 
        label-comboboxes, and radio buttons across different panels (pc1, pc2, pc3) 
        to be disabled. It ensures that these elements are not interactive until 
        explicitly enabled elsewhere in the application.
        
        Returns:
            None
        """

        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt3']].config(state='disabled')
        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt5']].config(state='disabled')

        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe1']].config(state='disabled')
       
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe2']].config(state='disabled')
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe3']].config(state='disabled')
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe4']].config(state='disabled')
        self.__pc2_elements["check_box_label"][nm.CheckBoxes.IMAGE_CP['cb1']].config(state='disabled')
        self.__pc2_elements['label_combobox'][nm.LabelCombobox.IMAGE_CP['lcb1']].config(state='disabled', width = 25)
        self.__pc2_elements["button"][nm.Buttons.IMAGE_CP['bt7']].config(state='disabled')

        self.__pc3_elements['radiobutton'][nm.Radiobuttons.IMAGE_CP['rbt1']].config(state='disabled')
        self.__pc3_elements['radiobutton'][nm.Radiobuttons.IMAGE_CP['rbt2']].config(state='disabled')

    def __ini_guiElements_Actions(self) -> None:
        """
        Initializes the actions (commands) for GUI elements in the control panel.
        This method configures the command callbacks for various buttons in the GUI.
        Each button is associated with a specific action or functionality.
        Actions configured:
        - 'bt6': Calls the `go_back` method to navigate back.
        - 'bt1': Calls the `__load_file` method to load a file.
        - 'bt5': Calls the `__save_image` method to save the current image.
        - 'bt2': Calls the `__load_folder` method to load a folder.
        - 'bt7': Calls the `__apply_changes` method to apply changes.
        Returns:
            None
        """

        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt6']].config(command=self.go_back)
        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt1']].config(command=self.__load_file)
        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt5']].config(command=self.__save_image)
        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt2']].config(command=self.__load_folder)
        self.__pc2_elements['button'][nm.Buttons.IMAGE_CP['bt7']].config(command=self.__apply_changes)    
       
    def __ini_guiElements_defaultValues(self) -> None:
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe1']].config(textvariable=self.__mean_noise)
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe2']].config(textvariable = self.__Swank_factor)
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe3']].config(textvariable = self.__kernel_size)
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe4']].config(textvariable = self.__kernel_sigma)
        self.__pc2_elements["check_box_label"][nm.CheckBoxes.IMAGE_CP['cb1']].config(textvariable = self.__apply_kernel,variable=self.__apply_kernel, onvalue = nm.common.checkBoxText[0], offvalue = nm.common.checkBoxText[1])
        self.__pc2_elements['label_combobox'][nm.LabelCombobox.IMAGE_CP['lcb1']].config(textvariable = self.__norm_method, values = lst.Image.normalization)
        
        self.__pc3_elements['radiobutton'][nm.Radiobuttons.IMAGE_CP['rbt1']].config(variable=self.__magnitude, value = 'Energy')
        self.__pc3_elements['radiobutton'][nm.Radiobuttons.IMAGE_CP['rbt2']].config(variable=self.__magnitude, value = 'Charge')

        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb21']].config(text = nm.Labels.ImSUMMARY_F['lb21'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb22']].config(text = nm.Labels.ImSUMMARY_F['lb22'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb31']].config(text = nm.Labels.ImSUMMARY_F['lb31'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb32']].config(text = nm.Labels.ImSUMMARY_F['lb32'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb41']].config(text = nm.Labels.ImSUMMARY_F['lb41'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb42']].config(text = nm.Labels.ImSUMMARY_F['lb42'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb43']].config(text = nm.Labels.ImSUMMARY_F['lb43'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb44']].config(text = nm.Labels.ImSUMMARY_F['lb44'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb51']].config(text = nm.Labels.ImSUMMARY_F['lb51'] +str(None))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb61']].config(text = nm.Labels.ImSUMMARY_F['lb61'] +str(None))

    ######################
    # GUI filled methods #
    # Private methods    #
    ######################

    def __setup_main_window(self) -> None:
        """
        Creamos el contenedor principal principal dentro del root (Ventana principal).        
        """       
        # main_frame
        self.__image_frame = ttk.Frame(self.__root, style='TFrame')  
        self.__image_frame.pack(fill=tk.BOTH, expand=True)  

        self.__root.update_idletasks()
    
    def __setup_control_panel(self) -> None:
        """
        Crea y posiciona el panel de botones en la parte superior izquierda.
        """
        panel_control_frame1 = ttk.Frame(self.__image_frame, style='TFrame')
        panel_control_frame1.grid(row=0, column=0, sticky="nsew", padx=5, pady=0, rowspan=2)
        
        panel_control_frame2 = ttk.Frame(self.__image_frame, style='TFrame')
        panel_control_frame2.grid(row=1, column=1,sticky="ns", columnspan=1, rowspan=1)
    
        panel_control_frame3 = ttk.Frame(self.__image_frame, style='TFrame')
        panel_control_frame3.grid(row=0, column=1,sticky='nsew',padx=5, pady=0, rowspan=1)

        #panel_control_frame3.grid_rowconfigure(0, weight=0)  
        #panel_control_frame3.grid_rowconfigure(1, weight=0)  

        panel_control_frame4 = ttk.Frame(self.__image_frame, style='TFrame')
        panel_control_frame4.grid(row=0, column=3,sticky='nsew',columnspan=1,padx=5, pady=0, rowspan=4)

        canvas_frame = ttk.Frame(self.__image_frame, style='TFrame', width = 500, height=700)
        canvas_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5, columnspan=1, rowspan=4)
        canvas_frame.grid_propagate(False)

        self.__image_frame.grid_rowconfigure(0, weight=0, minsize=1)
        self.__image_frame.grid_rowconfigure(1, weight=2)
        self.__image_frame.grid_columnconfigure(0, weight=0)
        self.__image_frame.grid_columnconfigure(1, weight=0)
        self.__image_frame.grid_columnconfigure(2, weight=0)
        self.__image_frame.grid_columnconfigure(3, weight=1)
        #canvas_frame.grid_rowconfigure(1, weight=1)  
        #canvas_frame.grid_columnconfigure(0, weight=1) 
        

        # Crear los botones dentro del contenedor
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

        self.__pc3_elements = cwgf.populate_control_panel(
            root = panel_control_frame3, 
            list_cfg = self.__pc3_elements_cfg, 
            horizontal = False
        )

        self.__vis_elements = cwgf.populate_elemnts_panels_dev(
            root = canvas_frame, 
            grid = [1,1],
            panel_configs = self.__vis_elements_cfg
        )

        self.__pc4_elements = cwgf.populate_control_panel(
            root = panel_control_frame4, 
            list_cfg = self.__pc4_elements_cfg, 
            horizontal = False
        )
        #self.__vis_elements["Image"]["canvas"].config(width=500, height=1000)
        
        self.__root.update_idletasks()
    
    #############################
    # Visual management methods #
    # Private methods           #
    #############################

    def __load_file(self) -> None:
        """
        Method to load a file (or files from folder).
        """

        filename = filedialog.askopenfilename(filetypes=(("MHD/RAW files", "*.mhd"), ("Text files", "*.out"), ("Text files", "*.txt")))

        if (len(filename) == 0):
            self.energy = None
            self.__update_canvas(self.__vis_elements["Image"]["canvas"], self.energy)
        else:
            self.__process_energy(filename)
            self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt3']].config(state='disabled')
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb21']].config(text = nm.Labels.ImSUMMARY_F['lb21'] +str(1))

    def __load_folder(self) -> None:
        """
        Method to load a directory.
        """

        filename = filedialog.askdirectory()
        if (len(filename) == 0):
            self.energy = None
            self.__update_canvas(self.__vis_elements["Image"]["canvas"], self.energy)
        else:
            self.__process_energy(filename)
            self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt3']].config(state='normal') 
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb21']].config(text = nm.Labels.ImSUMMARY_F['lb21'] +str(self.__count))
    
    def __process_energy(self, filename: str) -> None:
        """
        Method to process the energy file.
        """

        self.orig_energies = self.__load_energy(filename) # orig_energy never changes
        self.__signal = self.orig_energies # We need another variable in case of doing changes in the noise, normalization, etc

        self.__activate_widgets()

        self.__update_canvas(self.__vis_elements["Image"]["canvas"],  self.orig_energies)

    def __load_energy(self, filename: str) -> np.ndarray:
        """
        Method to load the energy file.
        """

        total_energy = None
        try:            
            
            if os.path.isfile(filename):
                # Try if the file is a *.out file
                try:
                    energy = np.loadtxt(filename, delimiter=" ", dtype=np.float32)
                # Except if the file is a *.mhd file
                except:
                    energy = sitk.GetArrayFromImage(sitk.ReadImage(filename))
                total_energy = energy if total_energy is None else total_energy + energy
                
            elif os.path.isdir(filename):
                #Find *.out or *mhd files in file_path
                for files in tqdm(os.listdir(filename), desc = "Loading energy files"):
                    
                    if files.endswith('.out') or files.endswith('.mhd') and not files.startswith('sum'):
                        self.__count += 1
                        #print(files)
                        # Try if the file is a *.out file
                        try:
                            energy = np.loadtxt(os.path.join(filename, files), delimiter=" ", dtype=np.float32)
                        # Except if the file is a *.mhd file
                        except:
                            energy = sitk.GetArrayFromImage(sitk.ReadImage(os.path.join(filename, files)))
                        total_energy = energy if total_energy is None else total_energy + energy

        except Exception as e:
            print(f"Error loading energy file: {e}")
            return None

        return total_energy
    
    def __apply_changes(self) -> None:
        """
        Method to apply changes to the image.
        """

        # Get the values from the GUI
        magnitude =  str(self.__magnitude.get())
        noise = float(self.__mean_noise.get())
        swank_factor = float(self.__Swank_factor.get())
        apply_kernel = self._check_checkbox_value(self.__apply_kernel)
        kernel_size = int(self.__kernel_size.get())
        kernel_sigma = float(self.__kernel_sigma.get())
        norm_method = str(self.__norm_method.get())  

        if magnitude == 'Charge':
            self.__signal = self.__energy_to_charge(self.orig_energies)
        elif magnitude == 'Energy':
            self.__signal = self.orig_energies
        # Apply the kernel if selected
        if apply_kernel:
            self.__signal = self.__kernel(self.__signal, kernel_size, kernel_sigma)
        
        # Add noise to the image
        self.__signal = self.__add_noise(self.__signal, noise, swank_factor)

        # Normalize the image
        norm_method = self.__norm_string_to_int(norm_method) 
        self.__signal = self.__normalize(self.__signal, norm_method, noise)

        self.__update_canvas(self.__vis_elements["Image"]["canvas"], self.__signal)
        self.__update_summary()

    def __energy_to_charge(self, energy: np.ndarray) -> np.ndarray:
        """
        Method to convert energy to charge.
        """
        return energy / 50.
    
    def __kernel(self, image: np.ndarray, kernel_size: int, sigma: float) -> np.ndarray:
        """
        Method to apply a kernel to the image.
        """
        # Define the kernel size
        kernel_radius = kernel_size // 2
        
        # Create a grid of (x,y) coordinates
        x, y = np.meshgrid(np.arange(-kernel_radius, kernel_radius+1), 
                        np.arange(-kernel_radius, kernel_radius+1))
        
        # Compute the Gaussian kernel
        kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        
        # Normalize the kernel so that its sum is 1
        kernel /= kernel.sum()
        # Kernel to list
        kernel = kernel.tolist()
        # kernel to be seen in the label
        self.__kernel_label = "\n" + "\n".join(" ".join(f"{x:.1e}" for x in row) for row in kernel)
        # Convolution of the image with the kernel
        image = convolve2d(image, kernel, mode = 'same')

        return image
    
    def __add_noise(self, image: np.ndarray, noise: float, swank_factor: float) -> np.ndarray:
        """
        Method to add noise to the image.
        """
    
        mean = image + noise
        std_dev_2 = mean*np.sqrt(1 / swank_factor -1) + np.sqrt(noise)

        image_noisy = np.random.normal(mean, np.sqrt(std_dev_2), mean.shape)
    
        return image_noisy
    
    def __normalize(self, image: np.ndarray, method: int, noise:float) -> np.ndarray:
        """
        Method to normalize the image.
        """
        if method == 0:  # No normalization
            norm_image = image

        elif method == 1:  # Logarithmic Normalization
            norm_image = np.log1p(image)

        elif method == 2:  # Square Root Normalization
            norm_image = np.sqrt(image)
             
        elif method == 3:  # VICTRE MCGPU Sensitivity Curve
           
            norm_image = 8 * (50 + (image  - noise) * 0.000239)  

        elif method == 4: # MCD Sensitivity Curve
            norm_image = 5.9e-4 * (image - noise) + 48.62
           
        elif method == 5: # VD Sensitivity Curve
            norm_image = 4.2e-4 * (image - noise) + 49.07
            
        return norm_image
    
    
    def __save_MHD(self, filename: str, image: np.ndarray) -> None:
        """
        Method to save the image as a MHD file.
        
        """
        try:
            # Convert the image to SimpleITK format
            sitk_image = sitk.GetImageFromArray(image)
            sitk_image.SetSpacing((0.085, 0.085)) # in m
            # Set the metadata
            sitk.WriteImage(sitk_image, filename)
        except Exception as e:
            print(f"Error saving MHD file: {e}")

    def __save_TIFF(self, filename: str, image: np.ndarray) -> None:
        """
        Method to save the image as a TIFF file.
        
        """
        try:
            # Convert the image to PIL format
            image = Image.fromarray(image)
            # Save the image
            image.save(filename)
        except Exception as e:
            print(f"Error saving TIFF file: {e}")

    def __save_DCM(self, filename: str, image: np.ndarray) -> None:
        """
        Method to save the image as a DCM file.
        
        """
        try:
            data_16bits = image.astype(np.uint16)
            #metadata
            fileMeta = pydicom.Dataset()
            # https://pydicom.github.io/pynetdicom/dev/service_classes/storage_service_class.html#storage-sops
            fileMeta.MediaStorageSOPClassUID = DigitalMammographyXRayImageStorageForProcessing
            fileMeta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
            fileMeta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

            # dataset
            ds = pydicom.Dataset()
            ds.file_meta = fileMeta

            # Some Metadata
            ds.PatientID = "12345"  # Ejemplo, reemplazar con el ID real
            ds.PatientName = "12345"  # Usando el mismo como ID del paciente
            ds.PatientComments = "Breast type info"
            ds.PatientState = "Signal present"
            
            # Clinical Trial Data
            ds.ClinicalTrialProtocolName = "VICTRE"
            ds.ClinicalTrialSiteName = "UCM - PROJECT"

            # Other metadata
            ds.ImageLaterality = "R"
            ds.ImagerPixelSpacing = [0.085, 0.085] # in mm
            
            ds.Manufacturer = "VICTRE"
            ds.OrganExposed = "BREAST"
            ds.PatientSex = "F"
            ds.PixelIntensityRelationship = "LIN"
            ds.PixelIntensityRelationshipSign = 1
            ds.PresentationIntentType = "FOR PROCESSING"
            ds.PresentationLUTShape = "IDENTITY"
            ds.StudyDescription = "Simulated Digital Mammography"
            ds.Modality = "MG"
            ds.StudyInstanceUID = pydicom.uid.generate_uid()  # Generate an unique ID

            # Serie Information
            
            ds.BodyPartExamined = "BREAST"
            ds.SeriesInstanceUID = pydicom.uid.generate_uid()  # Generate an unique ID

            # Simulated Equipment Information
            ds.InstitutionName = "UCM - H12Oct"
            ds.SoftwareVersions = "GAMOS - UCM V4.0"

            # Image Information
            ds.ImageType = ["ORIGINAL", "PRIMARY"]
            ds.ImageComments = "85 x 85 micron pixel size; float 32 to uint16 bit conversion"
            ds.ImagesInAcquisition = 1
            ds.LossyImageCompression = "00"
            ds.ConversionType = "SYN"
            ds.Rows = int(image.shape[0])
            ds.Columns = int(image.shape[1])
            ds.BitsAllocated = 16
            ds.PixelRepresentation = 0
            ds.PixelData = data_16bits.tobytes()

            # Detector
            ds.DetectorType = "DIRECT"
            ds.DetectorConfiguration = "AREA"
            ds.DetectorDescription = "a-Se, 200 micron"
            ds.DetectorActiveShape = "RECTANGLE"

            # Information about X-ray source
            ds.KVP = "28"
            #ds.ExposureInmAs = 58.6
            ds.AnodeTargetMaterial = "TUNGSTEN"
            ds.FilterType = "FLAT"
            ds.FilterMaterial = "RHODIUM"
            ds.FilterThicknessMinimum = "0.050"

            # Information about mammography
            ds.PositionerType = "MAMMOGRAPHIC"
            #ds.DerivationDescription = self.__norm_name

            #dicom Name
            file_out_dcm=filename

            # save
        
            ds.save_as(filename, write_like_original=False)
        except Exception as e:
            print(f"Error saving DCM file: {e}")


    def __save_image(self) -> None:
        """
        Method to save the image.
        """
        files = [('All Files', '*.*'), 
                ('DICOM File', '*.dcm'),
                ('Tif File', '*.tif'),
                ('MHD/RAW File', '*.mhd')]
        
        file = filedialog.asksaveasfilename(filetypes = files, defaultextension = '.mhd')
        format = file.split('.')[-1]
            #file = asksaveasfilename()
        if not file: 
            return
        try:
            if format == 'mhd':
                self.__save_MHD(file, self.__signal)
            elif format == 'tif':
                self.__save_TIFF(file, self.__signal)
            elif format == 'dcm':
                self.__save_DCM(file, self.__signal)
            else:
                print("Unsupported format")
        except Exception as e:
            print(f"Error saving image: {e}")

    def __activate_widgets(self) -> None:

        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt3']].config(state='normal')
        self.__pc1_elements['button'][nm.Buttons.IMAGE_CP['bt5']].config(state='normal')

        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe1']].config(state='normal')
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe2']].config(state='normal')
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe3']].config(state='normal')
        self.__pc2_elements["label_entry"][nm.LabelEntry.IMAGE_CP['lbe4']].config(state='normal')
        self.__pc2_elements["check_box_label"][nm.CheckBoxes.IMAGE_CP['cb1']].config(state='normal')
        self.__pc2_elements['label_combobox'][nm.LabelCombobox.IMAGE_CP['lcb1']].config(state='normal')
        self.__pc2_elements["button"][nm.Buttons.IMAGE_CP['bt7']].config(state='normal')
        
        self.__pc3_elements['radiobutton'][nm.Radiobuttons.IMAGE_CP['rbt1']].config(state='normal')
        self.__pc3_elements['radiobutton'][nm.Radiobuttons.IMAGE_CP['rbt2']].config(state='normal')

    def __update_canvas(self, canvas: tk.Canvas, image: np.ndarray) -> None:
        canvas.delete("all")

        width, height = canvas.winfo_width(), canvas.winfo_height()
        
        if image is None:
            canvas.delete("all")
            return

        #image = Image.fromarray(np.uint8(255-self.energies/np.max(self.energies)*255))
        norm_image =  image/np.max(image)
        
        image = Image.fromarray(np.uint8(255-norm_image*255))
        
        rel_height_width_image = image.size[1]/image.size[0]
        if rel_height_width_image < 1:
            orig_width = width
            width = int(height / rel_height_width_image)
            xcoord = orig_width//2
            ycoord = height//2
        else:
            orig_height = height
            height = int(width * rel_height_width_image)
            #xcoord = width//2
            xcoord = width//2
            ycoord = orig_height//2
        #print(int(width*rel_height_width_image))
        resized_image = image.resize((width, height), Image.LANCZOS)  

        photo = ImageTk.PhotoImage(resized_image)
        canvas.create_image(xcoord, ycoord, image=photo)
        #canvas.create_image(width//2, height//2, anchor='center', image=photo)
        canvas.image = photo

    def __string_to_bool(self, value: str) -> bool:
        """
        Convert a string to a boolean value.
        """
        return value.lower() in ("yes", "true", "t", "1")
    
    def _check_checkbox_value(self, variable: tk.StringVar) -> bool:
        """
        Method to check the value of a checkbox.
        """
        if variable.get() == nm.common.checkBoxText[0]:
            return True
        elif variable.get() == nm.common.checkBoxText[1]:
            return False
        else:
            raise ValueError("Invalid checkbox value")
    
    def __norm_string_to_int(self, value: str) -> int:
        """
        Convert a string to an integer.
        """
        if value == 'None':
            return 0
        elif value == 'Logarithmic Normalization':
            return 1
        elif value == 'Square Root Normalization':
            return 2
        elif value == 'VICTRE MCGPU Sensitivity Curve':
            return 3
        elif value == 'MCD Sensitivity Curve':
            return 4
        elif value == 'VD Sensitivity Curve':
            return 5
        else:
            raise ValueError(f"Unknown normalization method: {value}")
        
    def __update_summary(self) -> None:
        """
        Method to update the summary.
        """
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb22']].config(text = nm.Labels.ImSUMMARY_F['lb22'] +str(self.__magnitude.get()))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb31']].config(text = nm.Labels.ImSUMMARY_F['lb31'] +str(self.__mean_noise.get()))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb32']].config(text = nm.Labels.ImSUMMARY_F['lb32'] +str(self.__Swank_factor.get()))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb41']].config(text = nm.Labels.ImSUMMARY_F['lb41'] +str(self.__apply_kernel.get()))
        
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb51']].config(text = nm.Labels.ImSUMMARY_F['lb51'] +str(self.__norm_method.get()))
        self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb61']].config(text = nm.Labels.ImSUMMARY_F['lb61'] +'MHD/RAW')

        if self._check_checkbox_value(self.__apply_kernel) == False:
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb42']].config(text = nm.Labels.ImSUMMARY_F['lb42'] +str(None))
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb43']].config(text = nm.Labels.ImSUMMARY_F['lb43'] +str(None))
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb44']].config(text = nm.Labels.ImSUMMARY_F['lb44'] +str(None))
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb44']].config(width=30, anchor='nw', justify='left')
        else:
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb42']].config(text = nm.Labels.ImSUMMARY_F['lb42'] +str(self.__kernel_size.get())+ ' X '+str(self.__kernel_size.get()))
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb43']].config(text = nm.Labels.ImSUMMARY_F['lb43'] +str(self.__kernel_sigma.get()))
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb44']].config(text = nm.Labels.ImSUMMARY_F['lb44'] +str(self.__kernel_label))
            self.__pc4_elements['label'][nm.Labels.ImSUMMARY_F['lb44']].config(width=30, anchor='nw', justify='left')

 
    def go_back(self) -> None:
        """
        Method to go bakc to the main window.
        """
        for widget in self.__root.winfo_children():
            widget.destroy()  # Destruir todo el contenido actual
        
        # Alternativa: Destruir el `main_frame` completamente y recrearlo
        self.__image_frame.destroy()
        self.__callback_volver()  # Llamar al callback para reconstruir la interfaz principal