
class Names:

    class common:
        checkBoxText = ['Yes', 'No']
    
    class Windows:
        MAIN = 'MIMAC v1.0.0'
        SIM_SETUP = 'Setup simulation'
        g4dcm = 'phantom from [raw/mhd-nrrd] format to g4dcm format'
        IMAGE = 'Image generation'
    
    class Buttons:
        MAIN_CP = {
            'bt1': 'Setup simulation',
            'bt2': 'Image generation',
            'bt3': 'GAMOS voxelized phantom',
        }        
        SIM_SETUP_CP = {
            'bt1': 'Apply cfg',
            'bt2': 'Load cfg',
            'bt3': 'Save cfg',
            'bt4': 'N.Envents Calc.',
            'bt5': '<- Back',
            'bt6': 'Open file',
            'bt7': 'Generate Main debug file',       
        }
        PHANTOM_CP = {
            'bt1': 'Open mhd/raw',
            'bt2': 'Generate g4dcm phantom',
            'bt3': 'Show Crop planes',
            'bt6': 'Hide Crop planes',
            'bt4': 'View phantom',
            'bt5': '<- Back',
            'bt7': 'Auto W/L' 
        }
        IMAGE_CP = {
            'bt1': 'Load File',
            'bt2': 'Load Files from Folder',
            'bt3': 'Save Sum File',
            'bt5': 'Save Image',
            'bt6': '<- Back',
            'bt7': 'Apply'
        }
        NEVENTS_CP = {
            'bt1': 'Close'
        }
        NEVENTS_Calculate = {
            'bt1': 'Calculate events',
            'bt2': 'Calculate load'
        }
    
    class Labels:
        MAIN_CP = {
            'lb1': 'MIMAC v1.0.0',
        }
        SIM_SETUP_CP = {
            'lb1': 'MIMAC',
            'lb2': 'Shows simulation inputs files'
        }
        SUMMARY_F = {
            'lb1': 'Simulation summary',
            # MAIN PARAMETERS
            'lb2': 'Main Parameters',
            'lb21': 'Number of events:',
            # GEOMETRY PARAMETERS
            'lb3': 'Geometry Parameters',
            'lb31': 'World file:',
            'lb32': 'Voxelized phantom:',
            'lb33': 'Phantom file:',
            'lb35': 'Source-Detector distance:',
            'lb34': 'Physical detector:',
            'lb36': 'Source-Object distance:',
            # PHYSICS PARAMETERS
            'lb4': 'Physics Parameters',
            'lb41': 'Physics list:',
            'lb42': 'Filter 1 - Kill all electrons',
            'lb43': 'Filter 2 - Kill secondary tracks',
            'lb44': 'Filter 3 - Kill scattered photons',
            'lb45': 'Filter 4 - Kill photons at the jaws',
            # SOURCE PARAMETERS
            'lb5': 'Source Parameters',
            'lb51': 'Spectrum file:',
            'lb52': 'Source distribution:',
            'lb53': 'Align source automatically:',
            'lb54': 'Auto-size source:',
            # DETECTOR PARAMETERS
            'lb6': 'Detector Parameters',
            'lb61': 'Detector model:',
            'lb62': 'Anti-scatter grid:',
            # CONFGURATION APPLYING
            'lb7': 'Configuration applied:'
        }  
        MAIN_FILE_F = {
            'lb1': 'Info',
            'lb2': 'Simulation seed',
            'lb3': 'Other parameters'
        }
        PHYSICANDFILTERS_F = {
            'lb1': 'Filters setup',
            'lb2': 'Filter 1 - Kill all electrons',
            'lb3': 'Filter 2 - Kill secondary tracks',
            'lb4': 'Filter 3 - Kill scattered photons',
            'lb5': 'Filter 4 - Kill photons at the jaws',
            #'lb6': 'Filter 5 - Kill photons at the detector END',
            'lb7': 'Physic setup'
        }
        SOURCE_F = {
            'lb1': 'Source setup'
        }
        DETECTOR_F = {
            'lb1': 'General parameters',
            'lb2': 'Anti-scatter grid',
            'lb3': 'Output',
            'lb4': 'Signal generation'
        }
        GEOMETRY_F = {
            'lb1': '__ GEOMETRY SETUP __',
            'lb2': 'World definition',
            'lb3': '- Voxelized phantom',
            'lb4': 'Jaws setup',
            #'lb5': 'Include detector',
            'lb6': '- Non-voxelized phantom',
            'lb7': 'Phantom setup',
        }
        SCORING_F = {
            'lb1': 'Scoring setup',
            'lb11': '- Over ionization chamber',
            'lb2': '- Ion Chamber setup',
            'lb3': 'Scoring-II setup',
            'lb33': '- Over voxelized phantom',
            'lb4': '- Magnitude of scoring',
            'lb5': '- Output',
        }
        PHANTOM_CP = {
            'lb1': 'g4dcm phantom options',
            'lb2': 'Phantom name:',
            'lb3': '---',
            'lb4': "VICTRE's phantom options",
        }

        IMAGE_CP = {
            'lb1': 'Loaded File Magnitude'
        }

        ImSUMMARY_F = {
            'lb1': 'Image summary',
            'lb2': 'Main Parameters',
            'lb21': 'Number of files loaded: ',
            'lb22': 'Magnitude of the loaded files: ',
            'lb3': 'Noise Parameters',
            'lb31': 'Mean Electronic Noise (pairs e-h): ',
            'lb32': 'Swank Factor: ',
            'lb4': 'Smoothing Kernel Parameters',
            'lb41': 'Kernel Applied: ',
            'lb42': 'Kernel Shape (N x N): ',
            'lb43': 'Kernel Sigma: ',
            'lb44': 'Kernel Array: ',
            'lb5': 'Normalization Parameters',
            'lb51': 'Normalization Method: ',
            'lb6': 'Final Image Parameters: ',
            'lb61': 'Default Format: ', 
            'lb7': 'Press "Apply" to modify all parameters \nand the final image formation',           
        }

        NEVENTS_CP = {
            'lb1': 'Number of events calculate'
        }

        NEVENTS_Spectrum = {
            'lb1': 'Spectrum',
            'lb2': '- Spectrum characteristics',
            'lb21': '- kVp:',
            'lb22': '- Spectrum file:',
            'lb23': '- Anode material:',
            'lb24': '- Filter material:',
            'lb25': '- Filter thickness (mm):',
            'lb26': '- Mean energy (keV):',
            'lb3': '- Kerma',
            'lb31': '- Kerma_sp (uGy/mAs):',
            'lb32': '- Kerma_sim (Gy/N):',
            'lb33': '- Conversion_factor (N/mAs):',
        }

        NEVENTS_Calculate = {
            'lb1': 'Calculate',
            'lb2': '- Events per load (mAs)',
            'lb21': 'Number of events:',
            'lb22': '- [events]',
            'lb23': '- [Total.events(sci)]',
            'lb24': '- [Events_per_run(sci)]',
            'lb3': '- Tube load (mAs)',
            'lb31': 'Tube load (mAs):',
            'lb32': '- [load(mAs)]',           
        }

    class LabelCombobox:
        MAIN_FILE_F = {
            'lcb1': 'Physic list:'
        }
        SIM_SETUP_CP = {
            'lcb1': 'Select input file:'    
        }
        SOURCE_F = {
            'lcb1': 'Particle:',
            'lcb2': 'Spectrum:',
            'lcb3': 'Spectrum filled mod:',
            'lcb4': 'Position distribution:',
            'lcb5': 'Direction distribution:'
        }
        DETECTOR_F = {
            'lcb1': 'Detector model:',
            'lcb2': 'Detector Material:',
            'lcb3': 'Output file format:',
            'lcb4': 'Output type:'
        }
        GEOMETRY_F = {
            'lcb1': 'Select non-voxelized phantom',
            'lcb2': 'Select voxelized phantom',
            'lcb3': 'Select world',
            'lcb4': 'World fill material'
        }
        SCORING_F = {
            'lcb1': 'IOC filled material:'
        }
        PHYSICANDFILTERS_F = {
            'lcb1': 'Physic list'    
        }
        PHANTOM_CP = {
            'lcb1': 'Materials:'
        }
        IMAGE_CP = {
            'lcb1': 'Normalization method:',
        }
        NEVENTS_CP = {
            'lcb1': 'Select spectra:',
        }          

    class LabelEntry:
        MAIN_FILE_F = {
            'lbe1': 'Seed 1:',
            'lbe2': 'Seed 2:',
            'lbe3': 'Number of events:'
        }
        SOURCE_F = {
            'lbe1': 'Energy (Mev):',
            'lbe2': 'Focal spot size (mm):',
            'lbe3': 'Source position, x (mm):',
            'lbe4': 'Source position, y (mm):',
            'lbe5': 'Cone angle (deg):',
            'lbe6': 'Pyramid, x (mm):',
            'lbe7': 'Pyramid, y (mm):'
        }
        DETECTOR_F = {
            'lbe2': 'Detector deep (mm):',
            'lbe3': 'Number of pixels (x):',
            'lbe4': 'Number of pixels (y):',
            'lbe5': 'Pixel size x (mm):',
            'lbe6': 'Pixel size y (mm):',
            'lbe8': 'Grid ratio:',
            'lbe9': 'Grid frecuency:',
            'lbe10': 'Grid strip thickness:',
            'lbe11': 'Output file name (without extension):',
            'lbe13': 'Electron-hole energy creation (eV):',
        }
        GEOMETRY_F = {
            'lbe1': 'Source detector distance, SDD (mm):',
            'lbe2': "World's size beyond detector:",
            'lbe3': 'Source object distance, SOD (mm):',
            'lbe4': 'Jaw dim Y1 (mm):',
            'lbe5': 'Jaw dim Y2 (mm):',
            'lbe6': 'Jaw dim X1 (mm):',
            'lbe7': 'Jaw dim X2 (mm):',
            'lbe8': 'Jaw dim Z (mm):',
            'lbe9': 'Gap betwwen jaws (mm):',
            'lbe10': 'Source jaws distance, SJD (mm):'
        }
        SCORING_F = {
            'lbe1': 'IOC x-dim (mm):',
            'lbe2': 'IOC y-dim (mm):',
            'lbe3': 'IOC z-dim (mm):',
            'lbe4': 'Output file name (without extension):',
            'lbe5': 'Distance from chest wall (mm):',
            'lbe6': 'Distance from source (mm):',
            'lbe7': 'Left-Right position (mm):'
        }
        PHYSICANDFILTERS_F = {
            'lbe1': 'Maximum range (mm):'
        }
        PHANTOM_CP = {
            'lbe1': 'x ini (coronal):',
            'lbe2': 'x end (coronal):',
            'lbe3': 'z ini (axial):',
            'lbe4': 'z end (axial):',
            'lbe5': 'y ini (sagital):',
            'lbe6': 'y end (sagital):'
        }
        IMAGE_CP = {
            'lbe1': 'Mean Electronic Noise (pairs e-h)',
            'lbe2': 'Swank Factor',
            'lbe3': 'Kernel Shape (N x N)',
            'lbe4': 'Kernel Sigma'
        }
        NEVENTS_Calculate = {
            'lbe1': 'Number of runs:',
            'lbe2': 'Tube load (mAs):',
            'lbe3': 'Number of events:',
        }
    
    class CheckBoxes:
        MAIN_FILE_F = {
            'cb1': 'Geometry',
            'cb2': 'Physic',
            'cb3': 'Source',
            'cb4': 'Filters',
            'cb5': 'Get image',
            'cb6': 'Ana & Histos',
            'cb7': 'Scoring',
            'cb8': 'Set randomly',
            'cb9': 'Visualization file (.wrl)',
            'cb10': 'Delete previous visualization file'

        }
        PHYSICANDFILTERS_F = {
            'cb1': 'Apply Filter 1:',
            'cb2': 'Apply Filter 2:',
            'cb3': 'Apply Filter 3:',
            'cb4': 'Apply Filter 4:',
            #'cb5': 'Apply Filter 5:'
        }
        SOURCE_F = {
            'cb1': 'Auto-align source:',
            'cb2': 'Auto-size source:'
        }
        DETECTOR_F = {
            'cb1': 'Use anti-scatter grid',
            'cb2': 'Auto-size detector:',
        }
        GEOMETRY_F = {
            'cb1': 'Use voxelized phantom:',
            'cb2': 'Use jaws:',
            'cb3': 'Auto-size jaws:',
            #'cb4': 'Use physical detector:'
        }
        SCORING_F = {
            'cb1': 'kerma:',
            'cb2': 'Dose:',
            'cb3': 'MGD (mean glandular dose):',
            'cb4': 'Include Ionization Chamber:',
        }
        PHANTOM_CP = {
            'cb1': 'Reset origin:',
            'cb2': 'Remove chest wall:',
            'cb3': 'Include compresion paddle:',
            'cb4': 'Remove air:',
            'cb5': 'Free crop:',
            'cb6': 'Create DCM files:',
            'cb7': 'Create mhd/raw file:',
            'cb8': 'Sincronize planes:',
        }
        IMAGE_CP = {
            'cb1': 'Apply Smoothing Kernel',
        }

    class Radiobuttons:
        IMAGE_CP = {
            'rbt1': 'Energy (eV)',
            'rbt2': 'Charge (pairs e-h)',
        }
    
    class Canvas:
        IMAGE_CP = {
            'cv1': 'Image',
        }
    
    class Treeview:
        PHANTOM_CP = {
            'tv1': 'Image information',
        }