import glob
import os
import math as m
import SimpleITK as sitk
import json
from resources.pyresources.paths import Paths
from resources.pyresources.paths import base_paths

class SimSetup():

    #Constructor
    def __init__(self):
        
        self._sim_params = {}

        self._pixel_size = None
        self._Npixels = None
        self._detector_size = None
        self._origin = None
    
    @property
    def sim_params(self):
        """Getter para sim_params."""
        return self._sim_params

    @sim_params.setter
    def sim_params(self, value):
        """Setter para sim_params.
        
        Args:
            value (dict): Nuevo valor para sim_params. Debería ser un diccionario.
        """
        if not isinstance(value, dict):
            raise ValueError("sim_params debe ser un diccionario.")
        # Aquí puedes añadir más validaciones según tus necesidades
        self._sim_params = value
        
    ######################
    # Workflow Functions #
    ######################

    # Load Simulation parameter from cfg file
    def load_SimConfg_from_json(self, simConfig_file_path):
        with open(simConfig_file_path, 'r') as f:
            config = json.load(f)

        # Lista de claves que NO deben ser convertidas aunque sean "Yes"/"No"
        exclude_from_bool_conversion = {
            "DetectorModel"
        }

        def convert_value(key, val):
            if isinstance(val, str) and key not in exclude_from_bool_conversion:
                lower_val = val.lower()
                if lower_val == "yes":
                    return True
                elif lower_val == "no":
                    return False
            return val

        self._sim_params = {}

        # Recorremos cada sección del JSON
        for section, params in config.items():
            if isinstance(params, dict):
                for key, value in params.items():
                    params[key] = convert_value(key, value)
                self._sim_params.update(params)
            else:
                self._sim_params[section] = convert_value(section, params)

        return self._sim_params
 
    # Converta Boolean values from gui interface to Yes/No
    def convert_bool_in_dict(self):
        # Recorremos cada clave y valor en el diccionario
        for clave, valor in self._sim_params.items():
            # Si el valor es True, lo convertimos a 'Yes'
            if valor is True:
                self._sim_params[clave] = 'Yes'
            # Si el valor es False, lo convertimos a 'No'
            elif valor is False:
                self._sim_params[clave] = 'No'
        return self._sim_params
    
    # Calaculate secondary parameters from setup params
    def calculate_secondary_params(self):
        """
        Calcula los parámetros secundarios de la simulación basándose en los valores de configuración
        y los almacena en un diccionario centralizado.
        Si está marcado autosize, se hacen los cálculos; si no, se usan los parámetros proporcionados.
        """
        params = self._sim_params  # Alias para facilitar lectura
        calculated = {}  # Diccionario donde se almacenan los resultados

        #######################
        # DETECTOR PARAMETERS #
        #######################
        NPixelX    = float(params.get("NPixelX", 0))
        NPixelY    = float(params.get("NPixelY", 0))
        PixelSizeX = float(params.get("PixelSizeX", 0))
        PixelSizeY = float(params.get("PixelSizeY", 0))
        DetectorDepth = float(params.get("DetectorDepth", 0))
        
        calculated["NPixelX"] = NPixelX
        calculated["NPixelY"] = NPixelY
        calculated["PixelSizeX"] = PixelSizeX
        calculated["PixelSizeY"] = PixelSizeY
        calculated["DetectorDepth"] = DetectorDepth
        calculated["DetectorSize"] = [
            NPixelX * PixelSizeX,
            NPixelY * PixelSizeY,
            DetectorDepth
        ]
       
        # Origen del detector por defecto
        calculated["Origin"] = [0, 0, 0]

        # Convertir SDD y SJD a float (con manejo de error y valores por defecto)
        try:
            sdd_value = float(params.get("SDD", 1))
        except ValueError:
            sdd_value = 1.0

        try:
            SJD = float(params.get("SJD", 0))
        except ValueError:
            SJD = 0.0

        ################################
        # VOXELIZED PHANTOM PARAMETERS #
        ################################
        if params.get("DICOMGeom") == "Yes":

            voxel_phantom = params.get("VoxelPhantom", "")
            
            if voxel_phantom:
                phantom_name = ".".join(voxel_phantom.split('.')[:-1])
                #phantom_name = voxel_phantom
                phantom_path = Paths.SimSetup.data_folder['mhd_folder']  # Se asume que esta variable contiene la ruta correcta

                phantom = os.path.join(phantom_path,phantom_name+'.mhd')

                try:
                    phantom = sitk.ReadImage(phantom)
                    spacing = phantom.GetSpacing()
                    size = phantom.GetSize()

                    ImDimZ = size[2] * spacing[2]
                    SOD = sdd_value - ImDimZ
                    if sdd_value - ImDimZ != 0:
                        Augmentation = sdd_value / (sdd_value - ImDimZ)
                    else:
                        Augmentation = 0
                    ImDimX = size[0] * spacing[0] * Augmentation
                    ImDimY = size[1] * spacing[1] * Augmentation

                    # Evitar división por cero
                    if PixelSizeX == 0:
                        PixelSizeX = 1
                    if PixelSizeY == 0:
                        PixelSizeY = 1

                    if params.get("AutoSizeDetector") == "Yes":
                        
                        calculated["NPixelX"] = m.ceil(ImDimX / PixelSizeX)
                        calculated["NPixelY"] = m.ceil(ImDimY / PixelSizeY)

                    calculated["DetectorSize"] = [
                        calculated["NPixelX"] * PixelSizeX,
                        calculated["NPixelY"] * PixelSizeY,
                        DetectorDepth
                    ]
                    calculated["Origin"] = [-0.5 * (calculated["DetectorSize"][0] - 1),
                                            -0.5 * (calculated["DetectorSize"][1] - 1),
                                            SOD]
                except Exception as e:
                    print("Error al leer el archivo phantom:", e)

        #####################
        # SOURCE PARAMETERS #
        #####################
        if params.get("AutoSizeSource") == "Yes":
            DetectorSizeX, DetectorSizeY = calculated["DetectorSize"][:2]
            if sdd_value == 0:
                sdd_value = 1  # Evitar división por cero
            tan_value = m.sqrt(DetectorSizeX**2 + (DetectorSizeY * 0.5) ** 2) / sdd_value
            calculated["ConeAngle"] = m.degrees(m.atan(tan_value))
        else:
            calculated["ConeAngle"] = float(params.get("ConeAngle", 0.0))
        
        ###################
        # JAWS PARAMETERS #
        ###################
        DetectorSizeX, DetectorSizeY = calculated["DetectorSize"][:2]
        calculated["JyLD"] = SJD / sdd_value * DetectorSizeX
        calculated["JxLD"] = SJD / sdd_value * DetectorSizeY
        calculated["JawsDepth"] = float(params.get("JawsDepth", 5.0))
        calculated["DeltaZJaws"] = float(params.get("DeltaZJaws", 2.0))
        calculated["SJD"] = float(params.get("SJD", 100.0))
        
        if params.get("AutoSizeJaws") == "Yes":
            calculated["JAx1"] = SJD / sdd_value * DetectorSizeX - 0.5 * DetectorSizeX
            calculated["JAx2"] = 0.5 * DetectorSizeX
            calculated["JAy1"]  = SJD / (sdd_value * 2) * DetectorSizeY
            calculated["JAy2"]  = SJD / (sdd_value * 2) * DetectorSizeY
            calculated["JawShortDimension"] = 3 * calculated["JyLD"]
            calculated["JawOverlap"] = 0.3 * calculated["JAx2"]
        else:
            # Se usan los parámetros existentes o se asignan valores predeterminados en caso de no estar definidos
            calculated["JAx1"] = float(params.get("X1JawAperture", 0.0))
            calculated["JAx2"] = float(params.get("X2JawAperture", 0.0))
            calculated["JAy1"]  = float(params.get("Y1JawAperture", 0.0))
            calculated["JAy2"]  = float(params.get("Y2JawAperture", 0.0))
            calculated["JawShortDimension"] = float(params.get("JawShortDimension", 0.0))
            calculated["JawOverlap"] = float(params.get("JawOverlap", 0.0))
            
        ##########################
        # ION-CHAMBER PARAMETERS #
        ##########################
        calculated["dfCW"] = -0.5 * calculated["DetectorSize"][0] + float(params.get("IOCDistanceFromCW", 0))

        # Guardar los valores calculados en el objeto
        self._calculated_params = calculated

    # Delete files for extension
    @staticmethod
    def eliminar_archivos(path, extension):
        """
        Elimina todos los archivos con una extensión específica en el directorio dado.

        :param path: Ruta del directorio donde se buscarán los archivos.
        :param extension: Extensión de los archivos a eliminar (ejemplo: '.txt', '.log').
        """
        if not os.path.exists(path):
            print(f"El directorio '{path}' no existe.")
            return
        
        archivos_a_borrar = glob.glob(os.path.join(path, f"*{extension}"))

        if not archivos_a_borrar:
            print(f"No se encontraron archivos con la extensión '{extension}' en '{path}'.")
            return

        for archivo in archivos_a_borrar:
            try:
                os.remove(archivo)
                print(f"Archivo eliminado: {archivo}")
            except Exception as e:
                print(f"Error eliminando {archivo}: {e}")
    
    #####################
    # Deprecated method #
    #####################
        
    # Write a report file on the parameters used in the simulation.
    def write_sim_params(self):
        with open("sim_conditions.txt", 'w') as f:  
            for key, value in self._sim_params.items():  
                f.write('%s:%s\n' % (key, value))
    
    # Print most relevant params
    def print_some_sim_params(self):

        if self._sim_params['DetectorModel'] == 'None':
            print(f" - Detector Model: {self._sim_params['DetectorModel']}")
        else:
            print(f" - Detector Model: {self._sim_params['DetectorModel']}")
            print(f" - Source-detector distance: {self._sim_params['SDD']}")
            print(f" - Pixel size (x,y): ({self._pixel_size[0]},{self._pixel_size[1]})")
            print(f" - Pixel number (Nx,Ny): ({self._Npixels[0]},{self._Npixels[1]})")
            print(f" - Detector size (x,y,depth): ({self._detector_size[0]},{self._detector_size[1]},{self._detector_size[2]})\n")
            print(f" - Use Anti-Scatter grid: {self._sim_params['UseAntiScatterGrid']}")

        print(f"----------------------------------\n")
        
        print(f" - Spectra: {self._sim_params['Spectra']}")
        print(f" - Use Voxelized phantom: {self._sim_params['DICOMGeom']}")
        print(f" - Phantom used: {self._sim_params['Phantom']}")
        print(f" - Jaws: {self._sim_params['UseJaws']}")
        print(f" - Source distribution: {self._sim_params['Distribution']}\n")
        print(f"----------------------------------\n")
        print(f" - Events: {self._sim_params['NEvents']:.0e}\n")

    ########################
    # Setup Main Functions #
    ########################

    # MAIN FILE SETUP
    def main_setup(self):

        # Cargar configuración desde el archivo JSON
        with open(Paths.SimSetup.config_dict['main'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['main'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]["main_file_setup"]) + "\n\n")

            # Geometry
            f.write("\n".join(config["sections"]["geometry"]["Yes"]) + "\n\n")
            '''if self.sim_params["GeometryFile"] == "Yes":
                f.write("\n".join(config["sections"]["geometry"]["Yes"]) + "\n\n")
            elif self.sim_params["GeometryFile"] == "No":
                f.write("\n".join(config["sections"]["geometry"]["No"]) + "\n\n")'''
                
            # Physic
            f.write("\n".join(config["sections"]["physic"]["Yes"]) + "\n\n")
            '''if self.sim_params["PhysicFile"] == "Yes":
                f.write("\n".join(config["sections"]["physic"]["Yes"]) + "\n\n")
            elif self.sim_params["PhysicFile"] == "No":
                f.write("\n".join(config["sections"]["physic"]["No"]) + "\n\n")'''

            # Source
            f.write("\n".join(config["sections"]["source"]["Yes"]) + "\n\n")
            '''if self.sim_params["SourceFile"] == "Yes":
                f.write("\n".join(config["sections"]["source"]["Yes"]) + "\n\n")
            elif self.sim_params["SourceFile"] == "No":
                f.write("\n".join(config["sections"]["source"]["No"]) + "\n\n")'''

            # Filters
            f.write("\n".join(config["sections"]["filters"]["Yes"]) + "\n\n")
            '''if self.sim_params["FiltersFile"] == "Yes":
                f.write("\n".join(config["sections"]["filters"]["Yes"]) + "\n\n")
            elif self.sim_params["FiltersFile"] == "No":
                f.write("\n".join(config["sections"]["filters"]["No"]) + "\n\n")'''

            # Detector
            #f.write("\n".join(config["sections"]["detector"]["Yes"]) + "\n\n")
            if self.sim_params["DetectorModel"] == "No":
                f.write("\n".join(config["sections"]["detector"]["No"]) + "\n\n")
            else:
                f.write("\n".join(config["sections"]["detector"]["Yes"]) + "\n\n")
            
            # Scoring
            if self.sim_params["UseIOC"] == "Yes":
                f.write("\n".join(config["sections"]["scoringIOC"]["Yes"]) + "\n\n")
            elif self.sim_params["UseIOC"] == "No":
                f.write("\n".join(config["sections"]["scoringIOC"]["No"]) + "\n\n")
            '''if self.sim_params["MGD"] == "Yes":
                f.write("\n".join(config["sections"]["scoringMGD"]["Yes"]) + "\n\n")
            elif self.sim_params["MGD"] == "No":
                f.write("\n".join(config["sections"]["scoringMGD"]["No"]) + "\n\n")'''

            # Verbosity
            f.write("\n".join(config["sections"]["verbosity"]) + "\n\n")
            
            # Visualization
            if self.sim_params["VisFile"] == "Yes":
                f.write("\n".join(config["sections"]["vis"]["Yes"]) + "\n\n")
            elif self.sim_params["VisFile"] == "No":
                f.write("\n".join(config["sections"]["vis"]["No"]) + "\n\n")
                        
            # Seeds
            if self.sim_params["RandomSeed"] == "Yes":
                f.write("\n".join(config["sections"]["randomSeeds"]["Yes"]) + "\n\n")
            elif self.sim_params["RandomSeed"] == "No":
                seeds = "\n".join(line.format(
                Seed1=self.sim_params["Seed1"],
                Seed2=self.sim_params["Seed2"]
                ) for line in config["sections"]["randomSeeds"]["No"])
                f.write(seeds + "\n\n")            

            # Número de eventos
            run_events = config["sections"]["nEvents"]
            f.write("\n".join(line.format(NEvents=int(self.sim_params["NEvents"])) for line in run_events))
    
    # GEOMETRY SETUP
    def geometry_setup(self):
        
        # Generating Geometry.in file

        # Cargar configuración desde el archivo JSON
        with open(Paths.SimSetup.config_dict['geometry'], 'r') as file:
            config = json.load(file)
        
        with open(Paths.SimSetup.destiny_folder['geometry'], 'w') as f:
                # Escribir encabezado
                f.write("\n".join(config["header"]) + "\n")
                
                geometry ="\n".join(line.format(
                WorldFile=self.sim_params["WorldFile"]
                ) for line in config["voxelized_phantom"][self._sim_params["DICOMGeom"]])
                
                # Escribirmos la geometría
                f.write(geometry + "\n\n")
        
        # Configuring World, jaws and DICOM files
        self.world_setup()
        if self._sim_params["DICOMGeom"] == "Yes": self.DICOM_setup()
        if self._sim_params["UseJaws"] == "Yes": self.jaws_setup()
    
    # PHYSIC SETUP
    def physic_setup(self):
        
        # Cargar configuración desde el archivo JSON
        with open(Paths.SimSetup.config_dict['physic'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['physic'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n\n")

            # Escribir configuración de la lista de físicas
            physics_list = config["physics_lists"].get(self.sim_params["PhysicList"], [])
            if physics_list:
                f.write("\n".join(physics_list) + "\n\n")
            else:
                f.write("# No valid physics list provided.\n\n")
            
            # Estructura de las jaws
            for key, lines in config["other_params"].items():
                for line in lines:
                    f.write(line.format(
                        Range=self._sim_params["Range"]
                        ) + "\n")
                f.write("\n")
            
    # FILTER SETUP
    def filters_setup(self):
        # Cargar configuración desde el archivo JSON
        with open(Paths.SimSetup.config_dict['filters'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['filters'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n\n")

            # Escribir filtros principales
            f.write("\n".join(config["filters"]) + "\n\n")

            # Kill photons at the jaws
            kill_jaws = config["kill_photons_jaws"][self.sim_params["UseJaws"]]
            f.write("\n".join(kill_jaws) + "\n\n")

            # Kill photons at detector's end
            ''' detector_end_key = "MCD" if self.sim_params["DetectorModel"] == "MCD" else "Other"
            #detector_end_key = if self._sim_params.get("DetectorModel","Other") == MCD: "MCD" else: "Other"
            detector_end = config["kill_photons_detector_end"][detector_end_key]
            f.write("\n".join(detector_end) + "\n\n")'''

            # Aplicar filtros
            f.write("\n".join(config["apply_filters"]) + "\n\n")

            # Filter 1
            apply_f1 = config["apply_filter1"][self.sim_params["ApplyF1"]]
            f.write("\n".join(apply_f1) + "\n\n")

            # Filter 2
            apply_f2 = config["apply_filter2"][self.sim_params["ApplyF2"]]
            f.write("\n".join(apply_f2) + "\n\n")

            # Filter 3
            apply_f3 = config["apply_filter3"][self.sim_params["ApplyF3"]]
            f.write("\n".join(apply_f3) + "\n\n")

            # Filter 4
            apply_f4 = config["apply_filter4"][self.sim_params["ApplyF4"]]
            f.write("\n".join(apply_f4) + "\n\n")

            # Filter 5
            '''realistic_key = "RealisticYes" if self.sim_params["ApplyF5"] == "Yes" and self.sim_params["DetectorModel"] == "MCD" else "RealisticNo"
            apply_f5 = config["apply_filter5"][realistic_key]
            f.write("\n".join(apply_f5) + "\n\n") '''
    
    # SOURCE SETUP
    def source_setup(self):
        """
        Configura el archivo de fuente (source.in) basado en los parámetros de la simulación.
        """

        # Asegurar que los parámetros secundarios están actualizados
        self.calculate_secondary_params()

        with open(Paths.SimSetup.config_dict['source'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['source'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n")

            # Escribir inicialización
            f.write(config["initialization"].format(
                Particle=self._sim_params["Particle"],
                Energy=self._sim_params["Energy"]
            ) + "\n\n")

            # Escribir espectros
            f.write(config["spectra"]["header"] + "\n")
            f.write(config["spectra"]["None" if self._sim_params["Spectra"] == "None" else "default"].format(
                Spectra=self._sim_params["Spectra"]
            ) + "\n\n")

            # Escribir distribución de posición
            f.write(config["position_distribution"]["header"] + "\n")
            pos_key = f"{self._sim_params['PosDistribution']}_{self._sim_params['AlignSource']}"
            if pos_key in config["position_distribution"]:
                f.write(config["position_distribution"][pos_key].format(
                    DetectorSizeX=-0.5 * self._calculated_params["DetectorSize"][0],
                    SourcePosX=self._sim_params.get("SourcePosX", 0.),
                    SourcePosY=self._sim_params.get("SourcePosY", 0.),
                    FocusSize=self._sim_params["FocusSize"]
                ) + "\n\n")

            # Escribir forma de distribución
            f.write(config["distribution_shape"]["header"] + "\n")
            dist_key = f"{self._sim_params['Distribution']}_{self._sim_params['AutoSizeSource']}" \
                if self._sim_params["Distribution"] in ["Pyramid_Isotropic", "Cone", "SemiCone"] \
                else self._sim_params["Distribution"]

            if dist_key in config["distribution_shape"]:
                f.write(config["distribution_shape"][dist_key].format(
                    SDD= self._sim_params["SDD"],
                    DetectorSizeX=self._calculated_params["DetectorSize"][0],
                    DetectorSizeY=self._calculated_params["DetectorSize"][1],
                    PyramidX=self._sim_params.get("PyramidX", 0.),
                    PyramidY=self._sim_params.get("PyramidY", 0.),
                    ConeAngle=self._sim_params.get("ConeAngle", 0.),
                    CalculatedTheta=self._calculated_params["ConeAngle"]
                ) + "\n\n")
    
    # GetImage SETUP   
    def getImage_setup(self):
        """
        Configura el archivo sensitiveDetectors.in basado en los parámetros calculados.
        """

        # Asegurar que los parámetros secundarios están actualizados
        #self.calculate_secondary_params()

        with open(Paths.SimSetup.config_dict['getImage'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['getImage'], 'w') as f:
            # Escribir el encabezado
            f.write("\n".join(config["header"]) + "\n\n")

            # Escribir cada sección con los valores ya calculados
            detector_key = self._sim_params.get("DetectorModel", "None")

            for line in config["detector"][detector_key]:
                f.write(line.format(
                    NpixelsX=self._calculated_params["NPixelX"],
                    NpixelsY=self._calculated_params["NPixelY"],
                    detectorSizeX=self._calculated_params["DetectorSize"][0],
                    detectorSizeY=self._calculated_params["DetectorSize"][1],
                    detectorSizeZ=self._calculated_params["DetectorDepth"]                    
                ) + "\n")

            f.write("\n")  # Agregar un salto de línea extra después de toda la sección si quieres
                        
            #Escribimos el resto de los parámetros
            for section, lines in config["parameters"].items():
                for line in lines:
                    f.write(line.format(
                        NpixelsX=self._calculated_params["NPixelX"],
                        NpixelsY=self._calculated_params["NPixelY"],
                        pixelSizeX=self._calculated_params["PixelSizeX"],
                        pixelSizeY=self._calculated_params["PixelSizeY"],
                        detectorSizeX=self._calculated_params["DetectorSize"][0],
                        detectorSizeY=self._calculated_params["DetectorSize"][1],
                        detectorSizeZ=self._calculated_params["DetectorDepth"],
                        material=self._sim_params["Material"],
                        UseAntiScatterGrid=self._sim_params["UseAntiScatterGrid"],
                        GridRatio=self._sim_params["GridRatio"],
                        zStop=self._sim_params["SDD"] - self._sim_params["DetectorDepth"] / 2 - 1,
                        GridFrequency=self._sim_params["GridFrequency"],
                        GridStripThickness=self._sim_params["GridStripThickness"],
                        PairCreationEnergy=self._sim_params["Weh"],                       
                        gap=-0.5 * self._calculated_params["DetectorSize"][0],
                        DetectorModel=self._sim_params["DetectorModel"],
                        OutputType=self._sim_params["OutputType"],
                        OutputFilename=self._sim_params["OutputFilename"],
                        OutputFormat=self._sim_params["OutputFormat"]
                    ) + "\n")
                f.write("\n")
        
        self.detector_geom_setup()            
    
    # SCORING SETUP
    def scoringIOC_setup(self):
       
        with open(Paths.SimSetup.config_dict['scoring_IOC'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['scoring_IOC'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n\n")

            # Crear detector multifuncional
            f.write("\n".join(config["mf_detector"]) + "\n")

            # Agregar scorers según configuración
            if self.sim_params.get('kerma', "No") == "Yes":
                f.write("\n".join(config["scorers"]["kerma"]) + "\n")

            if self.sim_params.get('Dose', "No") == "Yes":
                f.write("\n".join(config["scorers"]["dose"]) + "\n")

            # Escribir configuración de errores de scorers
            f.write("\n".join(config["scorer_errors"]) + "\n")

            # Configurar impresión de resultados
            if self.sim_params.get('kerma', "No") == "Yes":
                lines = "\n".join(line.format(ScoringFileName=self._sim_params["ScoringFileName"]) for line in config["scorer_print"]["kerma"])
                f.write(lines + "\n")

            if self.sim_params.get('Dose', "No") == "Yes":
                lines = "\n".join(line.format(ScoringFileName=self._sim_params["ScoringFileName"]) for line in config["scorer_print"]["dose"])
                f.write(lines + "\n")

        
        self.IOC_setup()
    
    #############################
    # Setup Secondary Functions #
    #############################
    
    # WORLD SETUP
    def world_setup(self):
        if self._sim_params['WorldFile'] == 'world.geom':

            # Load the structured JSON template
            with open(Paths.SimSetup.config_dict['world'], 'r') as file:
                config = json.load(file)

            with open(Paths.SimSetup.destiny_folder['world'], 'w') as f:

                # 1. Header
                f.write("\n".join(config["header"]) + "\n\n")

                # 2. Materials
                f.write(config["materials"]["title"] + "\n\n")
                for line in config["materials"]["lines"]:
                    f.write(line + "\n")
                f.write("\n")

                # 3. Parameters
                f.write(config["parameters"]["title"] + "\n\n")
                for line in config["parameters"]["lines"]:
                    if line.strip().startswith("#"):
                        f.write(line + "\n")
                    else:
                        f.write(line.format(
                            SOD=self._sim_params["SOD"],
                            SDD=self._sim_params["SDD"],
                            WorldSizeBD=self._sim_params["WorldSizeBD"]
                        ) + "\n\n")
                f.write("\n")

                # 4. World definition
                f.write(config["world_definition"]["title"] + "\n\n")
                for line in config["world_definition"]["lines"]:
                    if line.strip().startswith("#"):
                        f.write(line + "\n")
                    else:
                        f.write(line.format(
                            WorldFilled=self._sim_params["WorldFilled"]
                        ) + "\n\n")
                f.write("\n")

                # 5. Elements in the world
                f.write(config["elements"]["title"] + "\n\n")
                f.write(config["elements"]["intro"] + "\n")
                for comment in config["elements"]["comments"]:
                    f.write(comment + "\n")
                f.write("\n")

                # Jaws
                f.write("# Jaws (collimators)\n")
                f.write(config["jaws"][self._sim_params["UseJaws"]] + "\n\n")

                # Ionization Chamber
                f.write("# Ionization Chamber\n")
                f.write(config["ioc"][self._sim_params["UseIOC"]] + "\n\n")

                # Phantom
                phantom_key = "DICOM" if self._sim_params["DICOMGeom"] == "Yes" else self._sim_params["GeomtryPhantom"]
                phantom_config = config["phantom"].get(phantom_key, config["phantom"]["default"])
                if phantom_config:
                    f.write("# Phantom geometry\n")
                    f.write(phantom_config.format(Phantom=self._sim_params["GeomtryPhantom"]) + "\n\n")

                # Detector
                f.write("# Physical Detector\n")
                if self._sim_params["DetectorModel"] == "MCD":
                    f.write(config["detector"]['Yes'] + "\n")
                elif self._sim_params["DetectorModel"] == "VD":
                    f.write(config["detector"]['No'] + "\n")
    
    #  VOXELIZED PHANTOM SETUP    
    def DICOM_setup(self):
        """
        Configura el archivo dicom_geom.in basado en los parámetros calculados.
        """
        # Asegurar que los parámetros secundarios están actualizados
        #self.calculate_secondary_params()

        with open(Paths.SimSetup.config_dict['dicom'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['dicom'], 'w') as f:
            f.write("\n".join(config["header"]) + "\n")
            
            for line in config["parameters"]:
                if line.strip().startswith("#"):
                    # Si es un comentario, lo escribimos sin modificar
                    f.write(line + "\n")
                else:
                    # Obtenemos los valores de origen con un valor por defecto
                    origin = self._calculated_params.get("Origin", [0, 0, 0])
                    # Verificamos que 'origin' es una lista o tupla de al menos 3 elementos
                    if not isinstance(origin, (list, tuple)) or len(origin) < 3:
                        origin = [0, 0, 0]
                    
                    f.write(line.format(
                        VoxelPhantom=self._sim_params.get("VoxelPhantom", "None"),
                        WorldFile=self._sim_params.get("WorldFile","None"),
                        OriginX=origin[0],
                        OriginY=origin[1],
                        OriginZ=origin[2]
                    ) + "\n")
    
    # JAWS SETUP
    def jaws_setup(self):
        """
        Configura el archivo jaws_geom.in basado en los parámetros calculados.
        """

        # Asegurar que los parámetros secundarios están actualizados
        #self.calculate_secondary_params()

        with open(Paths.SimSetup.config_dict['jaws'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['jaws_geom'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n")

            # Matriz de rotación
            f.write("\n".join(config["rotation_matrix"]) + "\n\n")

            # Configuración de las aperturas de las jaws
            jaw_size_key = "Yes" if self._sim_params['AutoSizeJaws'] == 'Yes' else "No"
            for line in config["jaw_apertures"]:
                f.write(line.format(
                    JAy1=self._sim_params["Y1JawAperture"],
                    JAy2=self._sim_params["Y2JawAperture"],
                    JAx1=self._sim_params["X1JawAperture"],
                    JAx2=self._sim_params["X2JawAperture"]
                ) + "\n")

            f.write("\n")

            # Dimensiones de las jaws
            for line in config["jaw_dimensions"]:
                f.write(line.format(
                    JyLD=self._calculated_params["JyLD"],
                    JxLD=self._calculated_params["JxLD"],
                    JawShortDimension=self._calculated_params["JawShortDimension"],
                    JawOverlap=self._calculated_params["JawOverlap"],
                    JawsDepth=self._calculated_params["JawsDepth"]
                ) + "\n")

            f.write("\n")

            # Parámetros geométricos
            for line in config["geometry_params"]:
                f.write(line.format(
                    DeltaZJaws=self._calculated_params["DeltaZJaws"],
                    SJD=self._calculated_params["SJD"]
                ) + "\n")

            f.write("\n")

            # Estructura de las jaws
            for key, lines in config["jaws_structure"].items():
                for line in lines:
                    f.write(line + "\n")
                f.write("\n")
    
    # Detector setup    
    def detector_geom_setup(self):
        # Cargar configuración desde el archivo JSON
        with open(Paths.SimSetup.config_dict['detector_geom'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['detector_geom'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n\n")

            # Matriz de rotación
            f.write("\n".join(config["rotation_matrix"]) + "\n\n")

            # Parámetros
            parameters = "\n".join(line.format(
                NPixelX=self._calculated_params["NPixelX"],
                NPixelY=self._calculated_params["NPixelY"],
                PixelSizeX=self._calculated_params["PixelSizeX"],
                PixelSizeY=self._calculated_params["PixelSizeY"],
                DetectorDepth=self._calculated_params["DetectorDepth"]
            ) for line in config["parameters"])
            f.write(parameters + "\n\n")

            # Definición del volumen
            f.write("\n".join(config["volume_definition"]) + "\n\n")

            # Estructura del detector
            detector_structure = "\n".join(line.format(
                Material=self.sim_params["Material"]
            ) for line in config["detector_structure"])
            f.write(detector_structure + "\n\n")

            # Detector Mark
            f.write("\n".join(config["detector_mark"]) + "\n\n")
 
    # Ion-Chamber Setup
    def IOC_setup(self):
        """
        Configura el archivo ion_chamber_geom.in basado en los parámetros calculados.
        """

        # Asegurar que los parámetros secundarios están actualizados
        self.calculate_secondary_params()

        with open(Paths.SimSetup.config_dict['ion_chamber'], 'r') as file:
            config = json.load(file)

        with open(Paths.SimSetup.destiny_folder['ion_chamber'], 'w') as f:
            # Escribir encabezado
            f.write("\n".join(config["header"]) + "\n\n")

            # Rotación
            f.write("\n".join(config["rotation_matrix"]) + "\n")

            # Dimensiones de la cámara de ionización
            for line in config["dimensions"]:
                f.write(line.format(
                    IOCx=self._sim_params["IOCx"],
                    IOCy=self._sim_params["IOCy"],
                    IOCz=self._sim_params["IOCz"]
                ) + "\n")

            # Posición de la cámara de ionización
            for line in config["position"]:
                f.write(line.format(
                    IOCDistanceFromS=self._sim_params["IOCDistanceFromS"],
                    dfCW=self._calculated_params["dfCW"],
                    IOCLRPosition=self._sim_params["IOCLRPosition"]
                ) + "\n")

            # Definición del volumen
            for line in config["volume_definition"]:
                f.write(line.format(
                    IOCMaterial=self._sim_params["IOCMaterial"]
                ) + "\n")

    ############# 
    # Run SETUP #
    #############
    
    def run_setup(self):
              
        # SECONDARY PARAMS CALCULATION 
        self.calculate_secondary_params()

        # RUN SETUP
        self.main_setup()
        self.geometry_setup()
        self.physic_setup()
        self.filters_setup()
        self.source_setup()
        self.getImage_setup()
        self.scoringIOC_setup()

        # DELETE FILES
        if self._sim_params['DeleteVisFiles'] == 'Yes':
            self.eliminar_archivos(base_paths.project_root, '.wrl')
    
    def run_debug_file(self):
        """
        Genera el archivo 'main_debug_setup.in' concatenando los contenidos de los archivos .in generados.
        """
        main_in_content = []

        # Incluir encabezado principal
        main_in_content.append("#-----------------#")
        main_in_content.append("# DEBUG MAIN FILE #")
        main_in_content.append("#-----------------#")
        main_in_content.append("")

        
        # Leer el contenido de geometry.in y escribirlo en el archivo principal
        with open(Paths.SimSetup.destiny_folder['geometry'], 'r') as f:
            main_in_content.append(f.read())
        # Leer el contenido de physic.in y escribirlo en el archivo principal
        with open(Paths.SimSetup.destiny_folder['physic'], 'r') as f:
            main_in_content.append(f.read())
        # Leer el contenido de filters.in y escribirlo en el archivo principal
        with open(Paths.SimSetup.destiny_folder['filters'], 'r') as f:
            main_in_content.append(f.read())
        # Leer el contenido de filters.in y escribirlo en el archivo principal
        with open(Paths.SimSetup.destiny_folder['source'], 'r') as f:
            main_in_content.append(f.read())
        # Leer el contenido de getImage.in y escribirlo en el archivo principal
        with open(Paths.SimSetup.destiny_folder['getImage'], 'r') as f:
                main_in_content.append(f.read())
        # Leer el contenido de scoring.in
        with open(Paths.SimSetup.destiny_folder['scoring_IOC'], 'r') as f:
            main_in_content.append(f.read())

        # Escribir el archivo final 'main_debug_setup.in'
        with open(Paths.SimSetup.destiny_folder['debug_main'], 'w') as f:
            f.write("\n".join(main_in_content))

        print("Archivo 'debug_main.in' generado correctamente.")
        

#Run Class
if __name__ == '__main__':  
     
    run = SimSetup()
 
    