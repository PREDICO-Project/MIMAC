import os
import sys


def get_GUI_root():
    """Devuelve la ruta absoluta del directorio donde se encuentra mainWindow.py"""
    # Si mainWindow.py es el punto de entrada, entonces __main__ tiene su ruta
    main_script_path = os.path.abspath(sys.argv[0])
    return os.path.dirname(main_script_path)

def get_project_path():
    """Devuelve la ruta absoluta del directorio del proyecto"""
    # Si mainWindow.py es el punto de entrada, entonces __main__ tiene su ruta
    main_script_path = os.path.abspath(sys.argv[0])
    return os.path.dirname(os.path.dirname(main_script_path))


class base_paths:
    """Define los paths base del proyecto, relativos al mainWindow.py"""
    gui_root = get_GUI_root()
    project_root = get_project_path()
    inputs = os.path.join(project_root, 'inputs')                     # Ajusta si existe
    geom_elements = os.path.join(project_root, 'geom', 'elementsInWorld')  # Ajusta si existe
    world = os.path.join(project_root, 'geom', 'worlds')                  # Ajusta si existe
    mhd = os.path.join(project_root, 'data', 'new_mhd')                   # Ajusta si existe
    original_mhd = os.path.join(project_root, 'data', 'original_mhd')             # Ajusta si existe
    materials = os.path.join(project_root, 'data', 'materials')               # Ajusta si existe
    g4phantom = os.path.join(project_root, 'data', 'g4dcm')                 # Ajusta si existe
    dcm = os.path.join(project_root, 'data', 'dcm')                       # Ajusta si existe
    spectra = os.path.join(project_root, 'spectra')                 # Ajusta si existe

class Paths:    
    """Centraliza todos los paths del proyecto para una gestión más organizada."""

    # Paths de imágenes
    class Images:
        
        LOGO = os.path.join(base_paths.gui_root, 'resources', 'images', 'logo.png')
        DirectionDist = os.path.join(base_paths.gui_root, 'resources', 'images', 'DirectionDist.png')
        Geometry = os.path.join(base_paths.gui_root, 'resources', 'images', 'Geometry.png')

    # Configuración del setup de simulación
    class SimSetup:
        """Agrupa los paths relacionados con la configuración de la simulación."""

        default_cfg = os.path.join(base_paths.gui_root, 'configs', 'default_simConfg.json')

        # Directorios de datos
        data_folder = {
            'mhd_folder': base_paths.mhd
        }

        # Archivos de configuración
        config_dict = {
            "main": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'main_confg.json'),
            "geometry": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'geometry_confg.json'),
            "world": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'world_confg.json'),
            "dicom": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'dicom_confg.json'),
            "jaws": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'jaws_confg.json'),
            "physic": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'physic_confg.json'),
            "filters": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'filters_confg.json'),
            "source": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'source_confg.json'),
            "getImage": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'getImage_confg.json'),
            "detector_geom": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'detector_geom_confg.json'),
            "scoring_IOC": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'scoringIOC_confg.json'),
            "ion_chamber": os.path.join(base_paths.gui_root, 'resources', 'json', 'INPUTScfgs', 'ioc_confg.json'),
        }

        # Destinos actuales de los archivos de entrada
        destiny_folder = {
            "debug_main": os.path.join(base_paths.project_root, "debug_main.in"),
            "main": os.path.join(base_paths.project_root, "main.in"),
            "geometry": os.path.join(base_paths.inputs, "Geometry.in"),
            "world": os.path.join(base_paths.world, "world.geom"),
            "dicom": os.path.join(base_paths.inputs, "VoxelizedPhantom.in"),
            "jaws_geom": os.path.join(base_paths.geom_elements, "Jaws.geom"),
            "physic": os.path.join(base_paths.inputs, "Physic.in"),
            "filters": os.path.join(base_paths.inputs, "Filters.in"),
            "source": os.path.join(base_paths.inputs, "Source.in"),
            "getImage": os.path.join(base_paths.inputs, "GetImage.in"),
            "detector_geom": os.path.join(base_paths.geom_elements, "detector.geom"),
            "scoring_IOC": os.path.join(base_paths.inputs, "ScoringIOC.in"),
            "scoring_MGD": os.path.join(base_paths.inputs, "ScoringMGD.in"),
            "ion_chamber": os.path.join(base_paths.geom_elements, "Ion_Chamber.geom"),
        }

        # Destinos antiguos (backup o pruebas)
        destiny_folder_old = {
            key: os.path.join(base_paths.gui_root, "inputsPruebas", os.path.basename(value))
            for key, value in destiny_folder.items()
        }
    class ImageGUI:
        #default_config = 'configs/default_image.json'
        default_config = os.path.join(base_paths.gui_root, 'configs', 'default_image.json')
    
    class Raw2G4DCM:
        default_config = os.path.join(base_paths.gui_root, 'configs', 'default_g4phantomConfg.json')
