import os
from src.tool_handler.folder_handler import FolderHandler as folder
from resources.pyresources.paths import base_paths

class Lists:

    
    class Physicandfilters:

        physics_list = [
            'GmEMPhysics', 
            'emstandard_opt4'
        ]
    
    class Source:

        particle = [
            'gamma', 
            'electron', 
        ]

        spectra = folder.folder_content2list(
            directory_path=os.path.join(base_paths.project_root, 'spectra'),
            file_extension='in'
        )

        spectra_filled_mod = [
            'interpolate', 
            'histogram'
        ]

        pos_dist = [
            'Single_point', 
            'Gaussian_disc'
        ]

        dist_shape = [
            'Constant',
            'Cone',
            'SemiCone',
            'Pyramid_Isotropic',
        ]
    
    class Detector:

        model = [
            'No',
            'MCD',
            'VD'
        ]
        material = [
            'aSe'
        ]
        output_format = [
            'MDH/RAW',
            'DCM',
            'Text'
        ]
        output_type = [
           'Charge',
           'Energy'
       ]
 
    class Geometry:

        world = folder.folder_content2list(
            directory_path=os.path.join(base_paths.project_root, 'geom','worlds'),
            file_extension='geom'
        )

        world_fill = [
            "G4_Galactic",
            "G4_AIR",
            "G4_WATER",
            "G4_WATER_VAPOR",            
        ]

        phantom = folder.folder_content2list(
            directory_path=os.path.join(base_paths.project_root, 'geom','elementsInWorld'),
            file_extension='geom'
        )

        phantom_voxelized = folder.folder_content2list(
            directory_path=os.path.join(base_paths.project_root, 'data','g4dcm'),
            file_extension='g4dcm'
        )
    
    class Scoring:

        ioc_fill = [
            "G4_AIR",
            "G4_WATER",
            "G4_lXe",
            "G4_lH2",
            "G4_lN2",
            "G4_lO2"
        ]

    class phantom:

        materials = folder.folder_content2list(
            directory_path=os.path.join(base_paths.project_root, 'data','materials'),
            file_extension='txt'
        )

    class Image:
        normalization = [
            'None',
            'Logarithmic Normalization',
            'Square Root Normalization',
            'VICTRE MCGPU Sensitivity Curve',
            'MCD Sensitivity Curve',
            'VD Sensitivity Curve',
        ]
