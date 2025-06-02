"""
Class and Methods necessary to generate the g4dcm format files.
"""

import SimpleITK as sitk
import matplotlib.pyplot as plt
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import pydicom
try:
    from pydicom._storage_sopclass_uids import DigitalMammographyXRayImageStorageForProcessing
except:
    from pydicom.uid import DigitalMammographyXRayImageStorageForProcessing
import numpy as np
np.bool = np.bool_ # coment this line for numpy versions grater than 1.23.1
from pydicom.uid import generate_uid
import shutil
from tqdm import tqdm
import tkinter as tk
from tkinter import Toplevel
import threading
from src.wg_factory.widget_fc import WIDGETFactory as wg
from resources.pyresources.paths import base_paths



class DCM2G4:

    ############################
    ####     Constructor    ####
    ############################

    def __init__(self, master):
        """
        Note on attribute declarations in this class:
            Public Attributes:
                - Defined as self.AttributeName (without underscores).
                - Directly accessible from outside the class.
                - Used for data that need to be directly accessible and modifiable, 
                and there's no harm in them being manipulated directly by other parts of the code.

            Protected Attributes:
                - Defined as self._AttributeName (with a single underscore).
                - Intended for internal use within the class and its subclasses.
                - Used for data that are not meant to be accessed directly from outside the class, 
                but are still accessible if necessary.
                - This is a softer level of protection than private, more a convention than a strict restriction.

            Private Attributes:
                - Defined as self.__AttributeName (with two underscores).
                - Strictly intended for internal use within the class.
                - Not directly accessible from outside the class, and Python uses 'name mangling' 
                to make them inaccessible.
                - Used to protect the internal state of the class from unwanted changes and to avoid 
                name conflicts with attributes in derived classes.
                - Useful for ensuring the internal state of the class is not altered in unintended ways.

        It's important to follow these conventions to maintain code clarity and ensure proper 
        encapsulation and protection of data within classes.        
        """

        # public params 
        
        # private attributes
        self._materials_filename = "materials.txt"         
        self._filein_name = "pc_1492698576"
        
        self._debug = False
        self._dcm = True
        self._raw = True
        self._reset_origin = True
        self._remove_chest_wall = True
        self._in_or_out = True
        self._cut_only_air = False
        self._free_cut = False
        self._slice_ini = 200
        self._slice_end = 220
        self._colum_ini = 50
        self._colum_end = 100
        self._row_ini = 50
        self._row_end = 100
        self._write_raw_pixelvalues = False
        self._visualize = False
        self._slice_index = 0
        self._materials_to_remove = []
        

        # protected attributes
        # Root path tree
        #self.__parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        #self.__granpa_path = os.path.abspath(os.path.join(self.__parent_path, os.pardir))
        #self.__granpa_path2 = os.path.abspath(os.path.join(self.__granpa_path, os.pardir))
        #self.__root_path = os.path.abspath(os.path.join(self.__granpa_path, os.pardir))

        self.__path_materials = base_paths.materials
        self.__path_mhd = base_paths.original_mhd
        self.__path_raw = base_paths.mhd
        self.__path_fileout = base_paths.g4phantom
        self.__path_dcm = base_paths.dcm

        self.__origin = None
        self.__voxelspacing = None
        self.__voxels = None
        self.__raw_file_name = None

        self.__data = None
        self.__material_index = None
        self.__densities = None
        self.__material_list = None

        self.__extensions = None
        
        self.__all_pixel_values = None
        self.__mapped_pixel_values = None
        self.__mapped_pixel_densities = None

        self.create_info_frame(master)

    #####################################
    ####     Properties Decorators   ####
    #####################################
        
    @property
    def materials_filename(self):
        """filename of the file with the materials information"""
        return self._materials_filename
    @materials_filename.setter
    def materials_filename(self,value):
        self._materials_filename = value 
        self.__path_materials = os.path.join(self.__path_materials, self._materials_filename)  
        
    @property
    def filein_name(self):
        """mhd/raw filename with the phantom"""
        return self._filein_name
    @filein_name.setter
    def filein_name(self,value):
        self._filein_name = value
        self.__path_mhd = os.path.join(self.__path_mhd, self._filein_name+".mhd")
        #self.__path_mhd = os.path.join(self.__path_mhd, self._filein_name)
        self.__path_fileout = os.path.join(self.__path_fileout, self._filein_name+".g4dcm") 
    
    @property
    def debug(self):
        """True/False"""
        return self._debug
    @debug.setter
    def debug(self, value):
        if not isinstance(value, bool):
            raise ValueError("debug must be a boolean value (True/False)")
        self._debug = value

    @property
    def reset_origin(self):
        """True/False"""
        return self._reset_origin
    @reset_origin.setter
    def reset_origin(self, value):
        if not isinstance(value, bool):
            raise ValueError("reset_origin must be a boolean value (True/False)")
        self._reset_origin= value

    @property
    def materials_to_remove(self):
        """List with materials ID to be removed"""
        return self._materials_to_remove
    @materials_to_remove.setter
    def materials_to_remove(self, value):
        if not isinstance(value, list):
            raise ValueError("materials_to_remove must be a list of integers")
        self._materials_to_remove= value

    @property
    def remove_chest_wall(self):
        """True/False"""
        return self._remove_chest_wall
    @remove_chest_wall.setter
    def remove_chest_wall(self, value):
        if not isinstance(value, bool):
            raise ValueError("remove_chest_wall must be a boolean value (True/False)")
        self._remove_chest_wall= value

    @property
    def in_or_out(self):
        """0: include Compression paddle, 1: Don`t include Compression paddle"""
        return self._in_or_out
    @in_or_out.setter
    def in_or_out(self, value):
        if value in [False, True]:
            self._in_or_out = value
        else:
            raise ValueError("in_or_out can only be True or False")  

    @property
    def cut_only_air(self):
        """True: remove slices with just air"""
        return self._cut_only_air
    @cut_only_air.setter
    def cut_only_air(self, value):
        if not isinstance(value, bool):
            raise ValueError("cut_only_air must be a boolean value (True/False)")
        self._cut_only_air= value 

    @property
    def free_cut(self):
        """True: user-defined crop"""
        return self._free_cut
    @free_cut.setter
    def free_cut(self, value):
        if not isinstance(value, bool):
            raise ValueError("free_cut must be a boolean value (True/False)")
        self._free_cut= value

    @property
    def slice_ini(self):
        """initial slice"""
        return self._slice_ini
    @slice_ini.setter
    def slice_ini(self, value):
        if isinstance(value, int) and value >= 0:
            self._slice_ini = value
        else:
            raise ValueError("slice_ini debe ser un entero mayor o igual a 0")

    @property
    def slice_end(self):
        """final slice"""
        return self._slice_end
    @slice_end.setter
    def slice_end(self, value):
        if isinstance(value, int) and value >= 0:
            self._slice_end = value
        else:
            raise ValueError("slice_end debe ser un entero mayor o igual a 0")

    @property
    def colum_ini(self):
        """initial column"""
        return self._colum_ini
    @colum_ini.setter
    def colum_ini(self, value):
        if isinstance(value, int) and value >= 0:
            self._colum_ini = value
        else:
            raise ValueError("colum_ini debe ser un entero mayor o igual a 0")

    @property
    def colum_end(self):
        """final column"""
        return self._colum_end
    @colum_end.setter
    def colum_end(self, value):
        if isinstance(value, int) and value >= 0:
            self._colum_end = value
        else:
            raise ValueError("colum_end debe ser un entero mayor o igual a 0")

    @property
    def row_ini(self):
        """initial row"""
        return self._row_ini
    @row_ini.setter
    def row_ini(self, value):
        if isinstance(value, int) and value >= 0:
            self._row_ini = value
        else:
            raise ValueError("row_ini debe ser un entero mayor o igual a 0")

    @property
    def row_end(self):
        """final row"""
        return self._row_end
    @row_end.setter
    def row_end(self, value):
        if isinstance(value, int) and value >= 0:
            self._row_end = value
        else:
            raise ValueError("row_end debe ser un entero mayor o igual a 0") 
    
    @property
    def write_raw_pixelvalues(self):
        return self._write_raw_pixelvalues
    @write_raw_pixelvalues.setter
    def write_raw_pixelvalues(self, value):
        if not isinstance(value, bool):
            raise ValueError("write_raw_pixelvalues must be a boolean value (True/False)")
        self._write_raw_pixelvalues= value

    @property
    def dcm(self):
        """True: returns a dcm file with the cropped phantom"""
        return self._dcm
    @dcm.setter
    def dcm(self, value):
        if not isinstance(value, bool):
            raise ValueError("dcm must be a boolean value (True/False)")
        self._dcm = value

    @property
    def raw(self):
        """True: returns a mhd/raw file with the cropped phantom"""
        return self._raw
    @raw.setter
    def raw(self, value):
        if not isinstance(value, bool):
            raise ValueError("draw must be a boolean value (True/False)")
        self._raw= value
    
    @property
    def visualize(self):
        """True: visualizes a slice for the phantom"""
        return self._visualize
    @visualize.setter
    def visualize(self, value):
        if not isinstance(value, bool):
            raise ValueError("visualize must be a boolean value (True/False)")
        self._visualize= value

    @property
    def slice_index(self):
        """Index of the visualized slice"""
        return self._slice_index
    @slice_index.setter
    def slice_index(self, value):
        if isinstance(value, int) and value >= 0:
            self._slice_index = value
        else:
            raise ValueError("slice_index debe ser un entero mayor o igual a 0")

    #####################################
    ####       Frame creating        ####
    #####################################
    

    def create_info_frame(self, master):
        self.master = master
        self.master.title("Processing Messages")

        self.top_window = Toplevel(master)
        self.top_window.title("Processing Details")

        self.top_window.geometry("+{}+{}".format(master.winfo_rootx() + 100, master.winfo_rooty() + 100))
        

        self.top_window.grid_rowconfigure(0, weight=1)  
        self.top_window.grid_columnconfigure(0, weight=1)  
        
        self.text_area = wg.create_text_area( self.top_window, 0, 0)
        self.text_area.grid(sticky="nsew")

        self.progress_label = wg.create_label(self.top_window,"Progress: ",1,0, sticky='ew')

    def add_message(self, message, progress=False):
        
        def append_message():
            self.text_area.config(state='normal')  
            if progress:
                self.progress_label.config(text=message)
            else:
                if isinstance(message, dict):
                    for key, value in message.items():
                        formatted_message = f"-{key}: {value}\n"
                        self.text_area.insert(tk.END, formatted_message)
                else:
                    self.text_area.insert(tk.END, message + "\n")
            self.text_area.config(state='disabled')  
            
            self.text_area.yview(tk.END)  
        self.master.after(0, append_message)

    def update_progress(self, text):
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)  
        self.text_area.insert(tk.END, text + '\n')
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

    def create_final_frame(self):
        def destroy_levels():
            self.top_window.destroy()
            final_window.destroy()
        final_window = Toplevel(self.master)
        
        final_window.title("Processing Completed")
        #final_window.geometry("+{}+{}".format(final_window.winfo_rootx() + 100, final_window.winfo_rooty() + 100))
        final_frame = tk.ttk.Frame(final_window)
        final_frame.grid(row=0, column=0, sticky="nsew")
        text1 = "G4DCM file Created in: {}".format(self.__path_fileout)
        self.info_label1 = wg.create_label(final_frame, text=text1, row= 0, column = 0, columnspan=4, wraplength=700, text_align="left",sticky="ew")
        self.info_label1.config(font=("Arial", 10))

        text2 = "New MHD/RAW (or DCM) file Created in: {}".format(self.__path_raw)
        self.info_label1 = wg.create_label(final_frame, text=text2, row= 1, column = 0, columnspan=4, wraplength=700, text_align="left",sticky="ew")
        self.info_label1.config(font=("Arial", 10))

        btn_end = wg.create_button(final_frame,button_text="Accept", row = 2, column=2, columnspan =1,command=destroy_levels)
        screen_width = final_window.winfo_screenwidth()
        screen_height = final_window.winfo_screenheight()
        x = (screen_width - final_window.winfo_reqwidth()) // 2
        y = (screen_height - final_window.winfo_reqheight()) // 2
        final_window.geometry(f"+{x}+{y}")
        
    #####################################
    ####       Loading Methods       ####
    #####################################

    def load_mapKeys(self):

        self.__data = []       
        print("Path materials: ", self.__path_materials)

        # Open the file and read line by line
        with open(self.__path_materials, 'r') as file:
            for line in file:
                # Skip empty lines
                if line.strip():
                    # Split the elements in the line
                    parts = line.split()

                    # Check if the line has the correct number of elements
                    if len(parts) == 4:
                        # Convert elements to the appropriate data types
                        voxel_value = int(parts[0])
                        density = float(parts[1])
                        material_name = parts[2]
                        material_index = int(parts[3])

                        # Add the data to the structure
                        self.__data.append((voxel_value, density, material_name, material_index))
        
        # Dictionaries definition
        self.__material_index = {item[0]: item[3] for item in self.__data} #Pixel value - Material index
        self.__densities = {item[0]: item[1] for item in self.__data}  # Pixel value - Material density
        self.__material_list = {item[2]: item[3] for item in self.__data}  # Material Name - Material Index
        self.__material_list = dict(sorted(self.__material_list.items(), key=lambda item: item[1]))

        # Print the read data        
       
        self.add_message("\n######## VOXEL VALUE - MATERIAL DENSITY ###################\n")
        self.add_message(self.__material_index)
        self.add_message("\n######## VOXEL VALUE - MATERIAL INDEX   ###################\n")
        self.add_message(self.__densities)
        self.add_message("\n######## MATERIAL NAME - MATERIAL INDEX ###################\n")
        self.add_message(self.__material_list)

    def load_mhd_and_raw(self):
        """Function that reads the mhd/raw file with the voxelized phantom and convert it into a numpy array."""
        print(self._materials_to_remove)
        # Check if the file exists
        try:
            itkimage = sitk.ReadImage(self.__path_mhd)
        except Exception:
            print(f"File '{self.__path_mhd}' not found.")
        
        
        # Metadata extracting from .mhd file
        try:
            self.__voxels = np.asanyarray(itkimage.GetSize()) # (Z,Y,X)
        except Exception:
            print("Error in reading Image Size data. Please check the DimSize data of the MHD file.")

        try:
            self.__voxelspacing = np.asanyarray(itkimage.GetSpacing())
        except Exception:
            print("Error in reading Voxel Spacing. Please check the ElementSpacing data of the MHD file.")
        
        if self._reset_origin:
            self.__origin=np.array([0.0,0.0,0.0])
        else:
            try:
                self.__origin = np.asanyarray(itkimage.GetOrigin())
            except :
                self.__origin=np.array([0.0,0.0,0.0])

        
        self.__all_pixel_values = sitk.GetArrayFromImage(itkimage)       
         
        print("Voxels: ", self.__voxels)
        print("Spacing: ", self.__voxelspacing)
     
        self.add_message("\n########            .mhd INFO           ###################")
        self.add_message(f"\n-NVoxels (X,Y,Z): {self.__voxels} \n-VoxelSpacing: {self.__voxelspacing}\n-Origin{self.__origin}\n")
    
    #########################################
    ####       Calculation Methods       ####
    #########################################
    
    def map_pixel_values_vectorized(self):  

        # Define the vectorized functions to map densities and indexes
        map_density = np.vectorize(lambda p_value: self.__densities.get(p_value, None))
        map_index = np.vectorize(lambda p_value: self.__material_index.get(p_value, None))

        # Apply the vectorized functions to the 3D array
        self.__mapped_pixel_densities = map_density(self.__all_pixel_values)
        self.__mapped_pixel_values= map_index(self.__all_pixel_values)

    def calc_extensions(self): # It is called inside of write_voxel_section
        
        if self.__origin is None or self.__voxelspacing is None or self.__voxels is None:
            print("Origin, voxel spacing, or voxel count data not available.")
            return

        
        try:
            origin = self.__origin
            voxelspacing = self.__voxelspacing
        except (IndexError, ValueError, TypeError):
            print("Error in processing origin data. Please check the structure of __origin.")
            return

        # Calculate extensions in each direction
        z_extension = [origin[0] - 0.5 * voxelspacing[0],
                       origin[0] + 0.5 * voxelspacing[0] + voxelspacing[0] * (self.__all_pixel_values.shape[0] - 1)]
        y_extension = [origin[1] - 0.5 * voxelspacing[1],
                       origin[1] + 0.5 * voxelspacing[1] + voxelspacing[1] * (self.__all_pixel_values.shape[1] - 1)]
        x_extension = [origin[2] - 0.5 * voxelspacing[2],
                       origin[2] + 0.5 * voxelspacing[2] + voxelspacing[2] * (self.__all_pixel_values.shape[2] - 1)]

        # Store the calculated extensions in self.__extensions
        self.__extensions = [x_extension, y_extension, z_extension]

        # Print extensions information
     
        self.add_message("\n########        PHANTOM EXTENSION       ###################")
        self.add_message(f"\n-x extensions: {x_extension}\n-y extensions: {y_extension}\n-z extensions: {z_extension}\n")
        #print("Extension: ", x_extension, y_extension, z_extension)
    
    def remove_chestWall(self):

        """Search and remove chest wall."""

        self.add_message("\n########      REMOVING CHEST WALL       ###################")

        columns = []

        for slice in self.__all_pixel_values:
            # find first column with a any voxel with a value of 50
            column = np.argmax(np.any(slice == 50, axis=0))
            columns.append(column)
        
        columns=np.array(columns)
        
        first_start, first_end, second_start, second_end=self.find_two_sequences_positions(columns)

        self.__all_pixel_values=self.__all_pixel_values[first_start:second_end+1,:,columns.max():]
        self.__voxels[2]=self.__all_pixel_values.shape[0]
        self.__voxels[0]=self.__all_pixel_values.shape[2]

        # Print Cutting indormation
        
        self.add_message("\nCHEST WALL REMOVED")
        self.add_message(f"-Star slice {first_start}")
        self.add_message(f"-End slice {second_end+1}")
        self.add_message(f"-Column start {columns.max()}")

        self.add_message(f"-New shape (Z,Y,X): {self.__all_pixel_values.shape}")

        '''if self._in_or_out == False:

            self.__all_pixel_values=self.__all_pixel_values[first_end+1:second_start,:,columns.max():]
            self.__voxels[2]=self.__all_pixel_values.shape[0]
            self.__voxels[0]=self.__all_pixel_values.shape[2]
            
            # Print Cutting indormation
            
            self.add_message("\nCOMPRESSION PADDLE NOT INCLUDED")
            self.add_message(f"-Start slice {first_end+1}")
            self.add_message(f"-End slice {second_start}")
            self.add_message(f"-Column start {columns.max()}")
            self.add_message(f"-New shape: {self.__all_pixel_values.shape}")


        elif self._in_or_out == True:
            
            self.__all_pixel_values=self.__all_pixel_values[first_start:second_end+1,:,columns.max():]
            self.__voxels[2]=self.__all_pixel_values.shape[0]
            self.__voxels[0]=self.__all_pixel_values.shape[2]

            # Print Cutting indormation
            
            self.add_message("\nCOMPRESSION PADDLE  INCLUDED")
            self.add_message(f"-Star slice {first_start}")
            self.add_message(f"-End slice {second_end+1}")
            self.add_message(f"-Column start {columns.max()}")
            self.add_message(f"-New shape: {self.__all_pixel_values.shape}")'''
      
    def find_two_sequences_positions(self,columns):
        # Initialise the variables
        first_start = first_end = second_start = second_end = None

        # Find first secuence
        for i, value in enumerate(columns):
            if value != 0:
                first_start = i
                break
        
        if first_start is not None:
            for i in range(first_start, len(columns)):
                if columns[i] == 0:
                    first_end = i - 1
                    break

        # Find second secuence
        if first_end is not None:
            for i in range(first_end + 1, len(columns)):
                if columns[i] != 0:
                    second_start = i
                    break

        if second_start is not None:
            for i in range(second_start, len(columns)):
                if columns[i] == 0:
                    second_end = i - 1
                    break
        
        
        self.add_message("\nCOMPRESSION PADDLE POSSITION")
        self.add_message(f"-First start {first_start}")
        self.add_message(f"-First end {first_end}")
        self.add_message(f"-Second start {second_start}")
        self.add_message(f"-Second end {second_end}")
        
        return first_start, first_end, second_start, second_end
    
    def crop_phantom(self):

        

        print(f'Original shape: {self.__all_pixel_values.shape}')
        # Checking if any image data is loaded
        if self.__all_pixel_values is None:
            print("No image data available. Please load the data first.")
            return

        # Convert the data image into a numpy array
        if not isinstance(self.__all_pixel_values, np.ndarray):
            self.__all_pixel_values = np.array(self.__all_pixel_values)
        
        self.add_message("\n########         PHANTOM CUTTING        ###################")

        if self._slice_ini < 0 or self._slice_end > self.__voxels[0]:
            
            self.add_message(f"\n-Slices selected to be removed ({self._slice_ini}, {self._slice_end}) are outside of VICTRE phantom dimensions.")
            self.add_message("-SLICES number will remain without changes")
        elif self._slice_ini == self._slice_end:
            
            self.add_message(f"\n-Slices selected to be removed ({self._slice_ini}, {self._slice_end}) are equals.")
            self.add_message("-SLICES number will remain without changes")
        elif self._slice_ini >= 0 or self._slice_end <= self.__voxels[0]:
            self.__all_pixel_values=self.__all_pixel_values[:,:,self._slice_ini:self._slice_end]
            # print(f"\n-Slices will be cutted from {self._slice_ini} to {self._slice_end}.")
            self.add_message(f"\n-Slices will be cutted from {self._slice_ini} to {self._slice_end}.")
        if self._colum_ini < 0 or self._colum_end > self.__voxels[2]:
            self.add_message(f"-Columns selected to be removed ({self._colum_ini}, {self._colum_end}) are outside of VICTRE phantom dimensions.")
            self.add_message("-COLUMNS number will remain without changes")
        elif self._colum_ini == self._colum_end:
            '''print(f"-Columns selected to be removed ({self._colum_ini}, {self._colum_end}) are equals.")
            print("-COLUMNS number will remain without changes")'''
            self.add_message(f"-Columns selected to be removed ({self._colum_ini}, {self._colum_end}) are equals.")
            self.add_message("-COLUMNS number will remain without changes")
        elif self._colum_ini >= 0 or self._colum_end <= self.__voxels[2]:
            self.__all_pixel_values=self.__all_pixel_values[self._colum_ini:self._colum_end,:,:]
            # print(f"-Columns will be cutted from {self._colum_ini} to {self._colum_end}.")
            self.add_message(f"-Columns will be cutted from {self._colum_ini} to {self._colum_end}.")
        if self._row_ini < 0 or self._row_end > self.__voxels[1]:
            '''print(f"-Rows selected to be removed ({self._row_ini}, {self._row_end}) are outside of VICTRE phantom dimensions.")
            print("-ROWS number will remain without changes")'''
            self.add_message(f"-Rows selected to be removed ({self._row_ini}, {self._row_end}) are outside of VICTRE phantom dimensions.")
            self.add_message("-ROWS number will remain without changes")
        elif self._row_ini == self._row_end:
            self.add_message(f"-Rows selected to be removed ({self._row_ini}, {self._row_end}) are equals.")
            self.add_message("-ROWS number will remain without changes")
        elif self._row_ini >= 0 or self._row_end <= self.__voxels[1]:
            self.__all_pixel_values=self.__all_pixel_values[:,self._row_ini:self._row_end,:]
            #print(f"-Rows will be cutted from {self._row_ini} to {self._row_end}.")
            self.add_message(f"-Rows will be cutted from {self._row_ini} to {self._row_end}.")
        
        self.__voxels[2]=self.__all_pixel_values.shape[0]
        self.__voxels[0]=self.__all_pixel_values.shape[2]
        self.__voxels[1]=self.__all_pixel_values.shape[1]

        #print(f"-New shape: {self.__all_pixel_values.shape}")
        print("Voxels:",self.__voxels)
        self.add_message(f"-New shape (Z,Y,X): {self.__all_pixel_values.shape}")

    def remove_slices_with_specific_value(self):

        
        # Checking if any image data is loaded
        if self.__all_pixel_values is None:
            print("No image data available. Please load the data first.")
            return
        
        def find_valid_range(array, values_to_remove):
            start = 0
            end = array.shape[0]

            while start < end and np.all(np.isin(array[start], values_to_remove)):
                 
                start += 1
            while end > start and np.all(np.isin(array[end - 1], values_to_remove)):
                end -= 1
            return start, end
        
        start_z, end_z = find_valid_range(self.__all_pixel_values, self._materials_to_remove)
        start_y, end_y = find_valid_range(self.__all_pixel_values.transpose(1, 0, 2), self._materials_to_remove)
        start_x, end_x = find_valid_range(self.__all_pixel_values.transpose(2, 0, 1), self._materials_to_remove)

        self.__all_pixel_values = self.__all_pixel_values[start_z:end_z, start_y:end_y, start_x:end_x]


        # Update the number of voxels after remove slices
        #self.__voxels = self.__all_pixel_values.shape
        self.__voxels[2]=self.__all_pixel_values.shape[0]
        self.__voxels[0]=self.__all_pixel_values.shape[2]
        self.__voxels[1]=self.__all_pixel_values.shape[1]

        '''print("\n########          SLICE CUTTING         ###################")
        print(f"Slices with pixel value '{value_to_remove}' have been removed. New shape: {self.__all_pixel_values.shape}")'''
        self.add_message("\n########          SLICE CUTTING         ###################")
        self.add_message(f"Slices with pixel value '{self._materials_to_remove}' have been removed. New shape: {self.__all_pixel_values.shape}")

    ###########################################
    ####       Visualization Methods       ####
    ###########################################

    def visualize_slice(self, slice_index):
        if self.__all_pixel_values is None:
            print("No image data available. Please load the data first.")
            return

        if slice_index < 0 or slice_index >= self.__all_pixel_values.shape[0]:
            print("Invalid slice index.")
            return
        slice_data = self.__mapped_pixel_values[slice_index]

        plt.imshow(slice_data, cmap='gray')
        plt.title(f"Slice {slice_index}")
        plt.axis('off')  # Opcional: quitar los ejes
        plt.show()
    
    #####################################
    ####       Writing Methods       ####
    #####################################
    
    def write_materials_section(self): 

        self.output_file.write(f"{len(self.__material_list)}\n")    
      
        # Escribir cada material único con su índice
        for material_name, material_index in self.__material_list.items():
            material_name_quoted = '"' + material_name + '"'
            self.output_file.write(f"{material_index} {material_name_quoted}\n")

    def write_voxel_section(self):
       
        self.output_file.write(f"{self.__voxels[0]} {self.__voxels[1]} {self.__voxels[2]}\n")
        self.calc_extensions()
        x_extension_str = ' '.join(map(str, self.__extensions[0]))
        y_extension_str = ' '.join(map(str, self.__extensions[1]))
        z_extension_str = ' '.join(map(str, self.__extensions[2]))
        self.output_file.write(f"{x_extension_str}\n")
        self.output_file.write(f"{y_extension_str}\n")
        self.output_file.write(f"{z_extension_str}\n")

    def write_raw_pixel_values(self):
        
        if self.__all_pixel_values is None:
            print("No pixel values available to write.")
            return

        with tqdm(total=len(self.__all_pixel_values), desc="Writing Pixel Values") as pbar:
            for image in self.__all_pixel_values:
                np.savetxt(self.output_file, image, fmt='%d')
                pbar.update(1) 
    
    def write_mapped_pixel_values(self):
        if self.__mapped_pixel_values is None:
            self.add_message("No mapped pixel values available to write.")
            return
        self.add_message("\n########      WRITING PIXEL VALUES      ###################")

        progress_description = "Writing Mapped Pixel Values"
        total_images = len(self.__mapped_pixel_values)

        for i, image in enumerate(self.__mapped_pixel_values):
            np.savetxt(self.output_file, image, fmt='%d')
            progress_message = f"{progress_description}: {i + 1}/{total_images}"
            self.add_message(progress_message, progress=True)  # Ensure overwrite_last is True
        
        self.add_message("\nWriting completed")

    def write_mapped_pixel_density(self):
        if self.__mapped_pixel_densities is None:
            print("No mapped density values available to write.")
            return
        self.add_message("\n########      WRITING PIXEL DENSITY      ###################")

        progress_description = "-Writing Mapped Pixel Densitiy"
        total_images = len(self.__mapped_pixel_densities)

        for i, image in enumerate(tqdm(self.__mapped_pixel_densities, desc=progress_description)):
            # Aplanar la lista de listas en una sola lista
            flat_list = [value for row in image for value in row]

            # Write the values in segments of 8 elements
            for j in range(0, len(flat_list), 8):
                segment = flat_list[j:j+8]
                segment_str = ' '.join(map(str, segment))
                self.output_file.write(segment_str + '\n')

            progress_message = f"{progress_description}: {i + 1}/{total_images}"
            self.add_message(progress_message, progress=True)
        
        self.add_message("\n-Writing completed")

        self.create_final_frame()

    def finalize_file(self):
        self.output_file.close()

    ####################################
    ####       Output Methods       ####
    ####################################
    
    def dcm_create(self):

        if not os.path.exists(self.__path_dcm):
            os.makedirs(self.__path_dcm, exist_ok=True)

        if os.listdir(self.__path_dcm):
            # If not empty, clean the directory
            shutil.rmtree(self.__path_dcm)
            os.makedirs(self.__path_dcm)

        total_slices = len(self.__all_pixel_values)
        progress_description = "Creating DICOM files"

        self.add_message("\n########      WRITING DCM FILES      ###################")

        # Crear el conjunto de datos DICOM para cada corte en la imagen 3D
        for i in range(total_slices):
            slice_array = self.__all_pixel_values[i][:,:]

            # Metadata
            fileMeta = pydicom.Dataset()
            fileMeta.MediaStorageSOPClassUID = DigitalMammographyXRayImageStorageForProcessing
            fileMeta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
            fileMeta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

            # Dataset
            ds = pydicom.Dataset()
            ds.file_meta = fileMeta
      
            ds.is_little_endian = True
            ds.is_implicit_VR = True

            # Configure the required attributes
            ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
            ds.SOPInstanceUID = generate_uid()
            ds.Modality = 'DBT'
            ds.SeriesInstanceUID = generate_uid()
            ds.StudyInstanceUID = generate_uid()
            ds.PatientName = "PatientName"  

            # Configure the specific attributes of the image
            ds.Rows = slice_array.shape[0]
            ds.Columns = slice_array.shape[1]
            ds.ImagePositionPatient = [self.__origin[0], self.__origin[1], self.__origin[2] + i * self.__voxelspacing[2]]
            ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
            ds.PixelSpacing = [self.__voxelspacing[0], self.__voxelspacing[1]]
            ds.SliceThickness = self.__voxelspacing[2]
            ds.SamplesPerPixel = 1
            ds.PhotometricInterpretation = 'MONOCHROME2'
            ds.PixelRepresentation = 0
            ds.BitsAllocated = 8
            ds.BitsStored = 8
            ds.HighBit = 7
            ds.RescaleIntercept = 0
            ds.RescaleSlope = 1
            ds.PixelData = slice_array.tobytes()

            # Save the DICOM file into 'dcm' subfolder
            ds.save_as(self.__path_dcm+f"/corte_{i}.dcm")
            
            # Update the progress
            progress_message = f"{progress_description}: {i + 1}/{total_slices}"
            self.add_message(progress_message, progress=True)

        self.add_message("\n-DICOM file creation completed.\n")
  
    def raw_create(self):
        if self.__all_pixel_values is None:
            print("No image data available. Please load the data first.")
            return
        
        if not os.path.exists(self.__path_raw):
            os.makedirs(self.__path_raw, exist_ok=True)

        output_mhd_filename = self._filein_name+".mhd"
        output_mhd_path = os.path.join(self.__path_raw, output_mhd_filename)
        img = sitk.GetImageFromArray(self.__all_pixel_values)
        img.SetSpacing(self.__voxelspacing)
        sitk.WriteImage(img, output_mhd_path)

        print(f"RAW and MHD files created: {output_mhd_path}")

    def create_phantom_file(self):
        
        self.output_file = open(self.__path_fileout, 'w')

        # Loading data
            
        self.load_mapKeys()
        self.load_mhd_and_raw()

        # Data manipulation

        if self._free_cut:
            self.crop_phantom()

        if self._remove_chest_wall:
            self.remove_chestWall()

        self.remove_slices_with_specific_value()
                    
        self.map_pixel_values_vectorized()

        # Visualization Data
        if self._visualize:
            self.visualize_slice(self._slice_index)
        
        # Writing information
        self.write_materials_section()
        self.write_voxel_section()
        if self._write_raw_pixelvalues:
            self.write_raw_pixel_values()
        self.write_mapped_pixel_values()
        self.write_mapped_pixel_density()
        
        # Generating optional output files
        if self._dcm:
            self.dcm_create()
        if self._raw:
            self.raw_create()

        self.finalize_file()

    def start_processing(self):
            
            processing_thread = threading.Thread(target=self.create_phantom_file)
            processing_thread.start()
