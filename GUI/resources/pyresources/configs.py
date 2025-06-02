from resources.pyresources.names import Names as nm
from resources.pyresources.paths import Paths as path


class ColorSetup:
        
        title_labels = '#1E90FF'
        subtitle_labels = '#FF6347'

class SizesSetup:

        # Fonts
        title_labels = 12
        subtitle_labels = 11

        # Images
        logo_sizeX = 200
        logo_sizeY = 80

        # Buttons
        button_width = 25

        # Combobox
        combobox_width = 25

class Cfgs:

    class NoteBookTabs:
        
        setupNotebook = [
            {"tab_title": "Main File"},
            {"tab_title": "Geometry"},
            {"tab_title": "Physic & Filters"},
            {"tab_title": "Source"},
            {"tab_title": "Detector"},
            {"tab_title": "Scoring"},
        ]
    
    class MainWindow:
        
        main_cfg = [
            {"label": nm.Labels.MAIN_CP['lb1'], "sticky":"we", "bold":True, "text_size":14, "text_align":"center", "colorText": ColorSetup.title_labels},
            {"separator": True},
            {"button": nm.Buttons.MAIN_CP['bt1'], "state":"normal","padx":15},
            {"separator": True},
            {"button": nm.Buttons.MAIN_CP['bt3'], "state":"normal", "padx":15},
            {"separator": True},
            {"button": nm.Buttons.MAIN_CP['bt2'], "state":"normal", "padx":15},
            {"separator": True},
            {"space": True},
            {"image":path.Images.LOGO, "sticky":"", "img_sizeX": SizesSetup.logo_sizeX, "img_sizeY": SizesSetup.logo_sizeY},          
        ]
    
    class SetupWindow:
        
        main_window_cfg = [
            {"type": "frame", "title": "panel_control_frame", "width": 250},
            {"type": "frame", "title": "summary_frame", "width": 300},
            {"type": "frame", "title": "notebook_frame", "minsize": 840},            
        ]
        pc_cfg = [
            {"space": True},
            {"button":nm.Buttons.SIM_SETUP_CP['bt1'], "state":"normal", "sticky":"", "width": SizesSetup.button_width},
            {"button":nm.Buttons.SIM_SETUP_CP['bt2'], "state":"normal", "sticky":"", "width": SizesSetup.button_width},
            {"button":nm.Buttons.SIM_SETUP_CP['bt3'], "state":"normal", "sticky":"", "width": SizesSetup.button_width},
            {"separator": True},
            #{"label":nm.Labels.SIM_SETUP_CP['lb2'], "sticky":"we", "bold":False, "text_align":"center"},
            {"label_combobox": nm.LabelCombobox.SIM_SETUP_CP['lcb1'],"horizontal": False, "sticky":"", "combobox_width": SizesSetup.combobox_width},
            {"button":nm.Buttons.SIM_SETUP_CP['bt6'], "state":"normal", "sticky":"", "width": SizesSetup.button_width},
            {"separator": True},
            {"button":nm.Buttons.SIM_SETUP_CP['bt4'], "state":"normal", "sticky":"", "width": SizesSetup.button_width},
            #{"button":nm.Buttons.SIM_SETUP_CP['bt7'], "state":"normal"},
            {"separator": True},
            {"button":nm.Buttons.SIM_SETUP_CP['bt5'], "state":"normal", "sticky":"", "width": SizesSetup.button_width},
            {"space": True},
            {"image":path.Images.LOGO, "sticky":"", "img_sizeX": SizesSetup.logo_sizeX, "img_sizeY": SizesSetup.logo_sizeY},
            {"separator": True},
            {"label":nm.Labels.SIM_SETUP_CP['lb1'], "sticky":"we", "bold":False, "text_align":"right"},
        ]
        summary_cfg = [
            {"label":nm.Labels.SUMMARY_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"separator": True},
            {"label":nm.Labels.SUMMARY_F['lb2'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.SUMMARY_F['lb21'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb3'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.SUMMARY_F['lb31'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb32'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb33'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb36'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb35'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb34'], "sticky":"we", "bold":False, "text_align":"left"},            
            {"label":nm.Labels.SUMMARY_F['lb4'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.SUMMARY_F['lb41'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb42'], "sticky":"we", "bold":False, "text_align":"left", 'show':False},
            {"label":nm.Labels.SUMMARY_F['lb43'], "sticky":"we", "bold":False, "text_align":"left", 'show':False},
            {"label":nm.Labels.SUMMARY_F['lb44'], "sticky":"we", "bold":False, "text_align":"left", 'show':False},
            {"label":nm.Labels.SUMMARY_F['lb45'], "sticky":"we", "bold":False, "text_align":"left", 'show':False},
            {"label":nm.Labels.SUMMARY_F['lb5'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.SUMMARY_F['lb51'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb52'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb53'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb54'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb6'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.SUMMARY_F['lb61'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.SUMMARY_F['lb62'], "sticky":"we", "bold":False, "text_align":"left"},
            {"separator": True},
            {"label":nm.Labels.SUMMARY_F['lb7'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels}
        ]
        main_file = [                    
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb1'], "check_box_text":nm.common.checkBoxText, "check":True},
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb2'], "check_box_text":nm.common.checkBoxText, "check":True},
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb3'], "check_box_text":nm.common.checkBoxText, "check":True},
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb4'], "check_box_text":nm.common.checkBoxText, "check":True},
            #{"space": True, "column":2},  
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb5'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb6'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            #{"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb7'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            {"label":nm.Labels.MAIN_FILE_F['lb2'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb8'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label_entry": nm.LabelEntry.MAIN_FILE_F['lbe1'], "vertical": False},
            {"label_entry": nm.LabelEntry.MAIN_FILE_F['lbe2'], "vertical": False},            
            {"label":nm.Labels.MAIN_FILE_F['lb3'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb10'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"check_box_label":nm.CheckBoxes.MAIN_FILE_F['cb9'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label_entry": nm.LabelEntry.MAIN_FILE_F['lbe3'],  "vertical": False},
            {"label":nm.Labels.MAIN_FILE_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels}
        ]
        geometry = [
            #Columna 1
            {"label":nm.Labels.GEOMETRY_F['lb2'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label_combobox": nm.LabelCombobox.GEOMETRY_F['lcb3'], "names":None, "horizontal": True, "action":None},
            {"label_combobox": nm.LabelCombobox.GEOMETRY_F['lcb4'], "names":None, "horizontal": True, "action":None},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe1'], "vertical": False},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe2'], "vertical": False},
            {"label":nm.Labels.GEOMETRY_F['lb7'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label":nm.Labels.GEOMETRY_F['lb3'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"check_box_label":nm.CheckBoxes.GEOMETRY_F['cb1'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label_combobox": nm.LabelCombobox.GEOMETRY_F['lcb2'], "names":None, "horizontal": True, "action":None},
            {"label":nm.Labels.GEOMETRY_F['lb6'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label_combobox": nm.LabelCombobox.GEOMETRY_F['lcb1'], "names":None, "horizontal": True, "action":None},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe3'], "vertical": False},
            {"image":path.Images.Geometry,  "columnspan": 4, "img_sizeX": 500, "img_sizeY": 400},            
            #Columna 2
            {"label":nm.Labels.GEOMETRY_F['lb4'], "sticky":"we", "bold":True, "text_align":"left", "column":2, "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"check_box_label":nm.CheckBoxes.GEOMETRY_F['cb2'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            {"check_box_label":nm.CheckBoxes.GEOMETRY_F['cb3'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe4'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe5'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe6'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe7'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe8'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe9'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.GEOMETRY_F['lbe10'], "vertical": False, "column":2},
            #{"label":nm.Labels.GEOMETRY_F['lb5'], "sticky":"we", "bold":True, "text_align":"left", "column":2, "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            #{"check_box_label":nm.CheckBoxes.GEOMETRY_F['cb4'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
        ]          
        physicANDfilters = [
            #Physic
            {"label":nm.Labels.PHYSICANDFILTERS_F['lb7'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label_combobox": nm.LabelCombobox.PHYSICANDFILTERS_F['lcb1'], "names":None, "horizontal": True, "action":None}, 
            {"label_entry": nm.LabelEntry.PHYSICANDFILTERS_F['lbe1'], "vertical": False},
            #Filters
            {"label":nm.Labels.PHYSICANDFILTERS_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label":nm.Labels.PHYSICANDFILTERS_F['lb2'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.PHYSICANDFILTERS_F['lb3'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.PHYSICANDFILTERS_F['lb4'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.PHYSICANDFILTERS_F['lb5'], "sticky":"we", "bold":False, "text_align":"left"},
            #{"label":nm.Labels.PHYSICANDFILTERS_F['lb6'], "sticky":"we", "bold":False, "text_align":"left"},
            {"check_box_label":nm.CheckBoxes.PHYSICANDFILTERS_F['cb1'], "check_box_text":nm.common.checkBoxText, "check":True, "column":1},
            {"check_box_label":nm.CheckBoxes.PHYSICANDFILTERS_F['cb2'], "check_box_text":nm.common.checkBoxText, "check":True, "column":1},
            {"check_box_label":nm.CheckBoxes.PHYSICANDFILTERS_F['cb3'], "check_box_text":nm.common.checkBoxText, "check":True, "column":1},
            {"check_box_label":nm.CheckBoxes.PHYSICANDFILTERS_F['cb4'], "check_box_text":nm.common.checkBoxText, "check":True, "column":1},
            #{"check_box_label":nm.CheckBoxes.PHYSICANDFILTERS_F['cb5'], "check_box_text":nm.common.checkBoxText, "check":True, "column":1}
        ]   
        source = [
            #Columna 1
            {"label":nm.Labels.SOURCE_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label_combobox": nm.LabelCombobox.SOURCE_F['lcb1'], "names":None, "horizontal": True, "action":None},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe1'], "vertical": False},
            {"label_combobox": nm.LabelCombobox.SOURCE_F['lcb2'], "names":None, "horizontal": True, "action":None},
            {"label_combobox": nm.LabelCombobox.SOURCE_F['lcb3'], "names":None, "horizontal": True, "action":None},
            {"label_combobox": nm.LabelCombobox.SOURCE_F['lcb4'], "names":None, "horizontal": True, "action":None},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe2'], "vertical": False},
            {"label_combobox": nm.LabelCombobox.SOURCE_F['lcb5'], "names":None, "horizontal": True, "action":None},
            {"image":path.Images.DirectionDist,  "columnspan": 4, "img_sizeX": 700, "img_sizeY": 500},
            #Columna 2
            {"space": True, "column":2},
            {"check_box_label":nm.CheckBoxes.SOURCE_F['cb1'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe3'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe4'], "vertical": False, "column":2},
            {"check_box_label":nm.CheckBoxes.SOURCE_F['cb2'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe5'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe6'], "vertical": False, "column":2},
            {"label_entry": nm.LabelEntry.SOURCE_F['lbe7'], "vertical": False, "column":2},             
        ]
        detector = [
            #Columna 1
            {"label":nm.Labels.DETECTOR_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label_combobox": nm.LabelCombobox.DETECTOR_F['lcb1'], "names":None, "horizontal": True, "action":None},
            {"label_combobox": nm.LabelCombobox.DETECTOR_F['lcb2'], "names":None, "horizontal": True, "action":None},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe2'], "vertical": False},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe5'], "vertical": False},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe6'], "vertical": False},
            {"check_box_label":nm.CheckBoxes.DETECTOR_F['cb2'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe3'], "vertical": False},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe4'], "vertical": False},
            {"label":nm.Labels.DETECTOR_F['lb2'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"check_box_label":nm.CheckBoxes.DETECTOR_F['cb1'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe8'], "vertical": False},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe9'], "vertical": False},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe10'], "vertical": False},
            #Columna 2
            {"label":nm.Labels.DETECTOR_F['lb4'], "sticky":"we", "bold":True, "text_align":"left", "column":2, "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe13'], "vertical": False, "column":2},
            {"label":nm.Labels.DETECTOR_F['lb3'], "sticky":"we", "bold":True, "text_align":"left", "column":2, "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label_combobox": nm.LabelCombobox.DETECTOR_F['lcb3'], "names":None, "horizontal": True, "action":None, "column":2,},
            {"label_combobox": nm.LabelCombobox.DETECTOR_F['lcb4'], "names":None, "horizontal": True, "action":None, "column":2,},
            {"label_entry": nm.LabelEntry.DETECTOR_F['lbe11'], "vertical": False, "column":2},
        ]
        scoring = [
            #Columna 1
            {"label":nm.Labels.SCORING_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"label":nm.Labels.SCORING_F['lb11'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"check_box_label":nm.CheckBoxes.SCORING_F['cb4'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label":nm.Labels.SCORING_F['lb2'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label_combobox": nm.LabelCombobox.SCORING_F['lcb1'], "names":None, "horizontal": True, "action":None},
            {"label_entry": nm.LabelEntry.SCORING_F['lbe1'], "vertical": False},
            {"label_entry": nm.LabelEntry.SCORING_F['lbe2'], "vertical": False},
            {"label_entry": nm.LabelEntry.SCORING_F['lbe3'], "vertical": False},
            {"label_entry": nm.LabelEntry.SCORING_F['lbe5'], "vertical": False},
            {"label_entry": nm.LabelEntry.SCORING_F['lbe6'], "vertical": False},
            {"label_entry": nm.LabelEntry.SCORING_F['lbe7'], "vertical": False},
            {"label":nm.Labels.SCORING_F['lb4'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels}, 
            {"check_box_label":nm.CheckBoxes.SCORING_F['cb1'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"check_box_label":nm.CheckBoxes.SCORING_F['cb2'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label":nm.Labels.SCORING_F['lb5'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels}, 
            {"label_entry": nm.LabelEntry.SCORING_F['lbe4'], "vertical": False},
            #Columna 2        
            #{"label":nm.Labels.SCORING_F['lb3'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "column":2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            #{"label":nm.Labels.SCORING_F['lb33'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "column":2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},   
            #{"check_box_label":nm.CheckBoxes.SCORING_F['cb3'], "check_box_text":nm.common.checkBoxText, "check":True, "column":2},
        ] 
    
    class Raw2g4_phatom:
        pc1_cfg = [
            #Columna de Botones
            #{"label":nm.Labels.PHANTOM_CP['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 4, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"button":nm.Buttons.PHANTOM_CP['bt1'], "state":"normal"},
            {"separator": True},            
            {"button":nm.Buttons.PHANTOM_CP['bt3'], "state":"normal"},           
            {"button":nm.Buttons.PHANTOM_CP['bt6'], "state":"normal"},
            {"separator": True},
            {"button":nm.Buttons.PHANTOM_CP['bt4'], "state":"normal"},
            {"button":nm.Buttons.PHANTOM_CP['bt2'], "state":"normal"},
            {"separator": True},
            {"button":nm.Buttons.PHANTOM_CP['bt5'], "state":"normal"},
            {"space": True},
            {"image":path.Images.LOGO, "sticky":"", "img_sizeX": SizesSetup.logo_sizeX, "img_sizeY": SizesSetup.logo_sizeY},
            {"separator": True},
            {"label":nm.Labels.SIM_SETUP_CP['lb1'], "sticky":"we", "bold":False, "text_align":"right"},
        ]
        pc2_cfg = [
            {"label":nm.Labels.PHANTOM_CP['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            #{"space": True},
            {"label":nm.Labels.PHANTOM_CP['lb2'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.PHANTOM_CP['lb3'], "sticky":"we", "bold":False, "text_align":"left", "column":1, "row":1},
            {"label_combobox": nm.LabelCombobox.PHANTOM_CP['lcb1'], "names":None, "horizontal": True, "action":None},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb1'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"separator": True, "mergecolumns": 2},
             {"label":nm.Labels.PHANTOM_CP['lb4'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb2'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb3'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb4'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"separator": True, "mergecolumns": 2},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb5'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"label_entry": nm.LabelEntry.PHANTOM_CP['lbe1'], "vertical": False, "width_entry": 10},
            {"label_entry": nm.LabelEntry.PHANTOM_CP['lbe2'], "vertical": False, "width_entry": 10},
            {"label_entry": nm.LabelEntry.PHANTOM_CP['lbe3'], "vertical": False, "width_entry": 10},
            {"label_entry": nm.LabelEntry.PHANTOM_CP['lbe4'], "vertical": False, "width_entry": 10},
            {"label_entry": nm.LabelEntry.PHANTOM_CP['lbe5'], "vertical": False, "width_entry": 10},
            {"label_entry": nm.LabelEntry.PHANTOM_CP['lbe6'], "vertical": False, "width_entry": 10},
            {"separator": True, "mergecolumns": 2},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb6'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb7'], "check_box_text":nm.common.checkBoxText, "check":True},
            {"separator": True, "mergecolumns": 2},
            {"treeview":nm.Treeview.PHANTOM_CP['tv1'], "width": 300, "height": 400, "mergecolumns": 2},
           ]
        pc3_cfg = [
             #{"check_box_label":nm.CheckBoxes.PHANTOM_CP['cb8'], "check_box_text":nm.common.checkBoxText, "check":True},
             {"button":nm.Buttons.PHANTOM_CP['bt7'], "state":"normal", "column":2},
        ]
        vis_cfg = [
                {"title": "Axial view", "type": "scrollable_canvas", "width": 550, "height": 450},
                {"title": "Coronal view", "type": "scrollable_canvas", "width": 550, "height": 450},
                {"title": "Sagittal view", "type": "scrollable_canvas", "width": 550, "height": 450},
                {"title": "Materials", "type": "canvas", "width": 550, "height": 450}
        ]

    class ImageWindow:
        pc_cfg = [
            #Columna de Botones
            {"button":nm.Buttons.IMAGE_CP['bt1'], "state":"normal"},
            {"separator": True},
            {"button":nm.Buttons.IMAGE_CP['bt2'], "state":"normal"},
            {"separator": True},
            {"button":nm.Buttons.IMAGE_CP['bt3'], "state":"disable"},           
            {"separator": True},
            {"button":nm.Buttons.IMAGE_CP['bt5'], "state":"disable"},
            {"space": True},
            {"button":nm.Buttons.IMAGE_CP['bt6'], "state":"normal"},
            {"image":path.Images.LOGO, "sticky":"", "img_sizeX": SizesSetup.logo_sizeX, "img_sizeY": SizesSetup.logo_sizeY},
            {"separator": True},
            {"label":nm.Labels.SIM_SETUP_CP['lb1'], "sticky":"we", "bold":False, "text_align":"right"},
        ]

        pc2_cfg = [
            {"label_entry": nm.LabelEntry.IMAGE_CP['lbe1'], "vertical": False},
            {"label_entry": nm.LabelEntry.IMAGE_CP['lbe2'], "vertical": False},
            {"separator": True},
            {"check_box_label":nm.CheckBoxes.IMAGE_CP['cb1'], "check_box_text":nm.common.checkBoxText, "check":True},           
            {"label_entry": nm.LabelEntry.IMAGE_CP['lbe3'], "vertical": False},
            {"label_entry": nm.LabelEntry.IMAGE_CP['lbe4'], "vertical": False},
            {"separator": True},
            {"label_combobox": nm.LabelCombobox.IMAGE_CP['lcb1'], "names":None, "horizontal": True, "action":None},
            {"space": True},
            {"button":nm.Buttons.IMAGE_CP['bt7'], "state":"normal"},
        ]

        pc3_cfg = [
            {"label":nm.Labels.IMAGE_CP['lb1'], "sticky":"we", "bold":False, "text_align":"left"},
            {"radiobutton":nm.Radiobuttons.IMAGE_CP['rbt1'], "state":"disable", "value":'Energy', 'variable':None},
            {"radiobutton":nm.Radiobuttons.IMAGE_CP['rbt2'], "state":"disable", "value":'Charge', 'variable':None, 'row':1,'column': 2},
            {"separator": True},
        ]

        vis_cfg = [
            {"type": "canvas", "title": "Image"},
        ]

        summary_cfg = [
            {"label":nm.Labels.ImSUMMARY_F['lb1'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},
            {"separator": True},
            {"label":nm.Labels.ImSUMMARY_F['lb2'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.ImSUMMARY_F['lb21'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb22'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb3'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.ImSUMMARY_F['lb31'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb32'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb4'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.ImSUMMARY_F['lb41'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb42'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb43'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb44'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb5'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.ImSUMMARY_F['lb51'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb6'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.ImSUMMARY_F['lb61'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.ImSUMMARY_F['lb7'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
        ]
    
    class Nevents:
        
        main_window_cfg = [
            {"type": "frame", "title": "panel_control_frame", "width": 210},
            {"type": "frame", "title": "spectrum_frame", "width": 300},
            {"type": "frame", "title": "calculate_frame", "width": 380},            
        ]
        pc_cfg = [
            {"label_combobox": nm.LabelCombobox.NEVENTS_CP['lcb1'], "names":None, "horizontal": False, "action":None, "combobox_width": 25},      
            {"separator": True},
            {"button":nm.Buttons.NEVENTS_CP['bt1'], "state":"normal"},
            {"image":path.Images.LOGO, "sticky":"", "img_sizeX": SizesSetup.logo_sizeX, "img_sizeY": SizesSetup.logo_sizeY},
        ]
        spectrum_cfg = [
            {"label":nm.Labels.NEVENTS_Spectrum['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},   
            {"label":nm.Labels.NEVENTS_Spectrum['lb2'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.NEVENTS_Spectrum['lb21'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb22'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb23'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb24'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb25'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb26'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb3'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels},
            {"label":nm.Labels.NEVENTS_Spectrum['lb31'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb32'], "sticky":"we", "bold":False, "text_align":"left"},
            {"label":nm.Labels.NEVENTS_Spectrum['lb33'], "sticky":"we", "bold":False, "text_align":"left"}
        ]
        calculate_cfg = [
            {"label":nm.Labels.NEVENTS_Calculate['lb1'], "sticky":"we", "bold":True, "text_align":"left", "mergecolumns": 2, "colorText":ColorSetup.title_labels, "text_size":SizesSetup.title_labels},   
            {"label":nm.Labels.NEVENTS_Calculate['lb2'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels, "mergecolumns": 2},
            {"label_entry": nm.LabelEntry.NEVENTS_Calculate['lbe1'], "vertical": False},
            {"label_entry": nm.LabelEntry.NEVENTS_Calculate['lbe2'], "vertical": False},
            {"button":nm.Buttons.NEVENTS_Calculate['bt1'], "state":"normal"},
            {"label":nm.Labels.NEVENTS_Calculate['lb21'], "sticky":"we", "bold":False, "text_align":"left", "mergecolumns": 2},
            {"label":nm.Labels.NEVENTS_Calculate['lb22'], "sticky":"we", "bold":False, "text_align":"left", "mergecolumns": 2},
            {"label":nm.Labels.NEVENTS_Calculate['lb23'], "sticky":"we", "bold":False, "text_align":"left", "mergecolumns": 2},
            {"label":nm.Labels.NEVENTS_Calculate['lb24'], "sticky":"we", "bold":False, "text_align":"left", "mergecolumns": 2},
            {"separator": True, "mergecolumns": 2},
            {"label":nm.Labels.NEVENTS_Calculate['lb3'], "sticky":"we", "bold":True, "text_align":"left", "colorText":ColorSetup.subtitle_labels, "text_size":SizesSetup.subtitle_labels, "mergecolumns": 2},
            {"label_entry": nm.LabelEntry.NEVENTS_Calculate['lbe3'], "vertical": False},
            {"button":nm.Buttons.NEVENTS_Calculate['bt2'], "state":"normal"},
            {"label":nm.Labels.NEVENTS_Calculate['lb31'], "sticky":"we", "bold":False, "text_align":"left", "mergecolumns": 2},
            {"label":nm.Labels.NEVENTS_Calculate['lb32'], "sticky":"we", "bold":False, "text_align":"left", "mergecolumns": 2}
        ]

class Rules:
        ejepmlo_de_uso = [
               # ─────────────────────────────────────────────────────────────
                # EJEMPLO 1: Desactiva varios campos si una checkbox está desmarcada
                # ─────────────────────────────────────────────────────────────
                {
                    "trigger": "geometry_cb2",     # Nombre interno de la variable (en __tk_vars)
                    "expected": False,             # Valor que activa la regla (si se desmarca en este caso)
                    "action": "disable",           # Acción: "disable" desactiva los widgets
                    "targets": [                   # Variables afectadas por la acción
                        "geometry_lbe4",
                        "geometry_lbe5",
                        "geometry_lbe6",
                        "geometry_lbe7"
                    ]
                },

                # ─────────────────────────────────────────────────────────────
                # EJEMPLO 2: Fija el valor de un campo si una opción está activada
                # ─────────────────────────────────────────────────────────────
                {
                    "trigger": "source_cb2",       # Cuando la checkbox 'AutoSizeSource' está activada
                    "expected": True,
                    "action": "set",               # Acción "set" → fija un valor específico
                    "targets": ["source_lbe5"],    # Campo a modificar
                    "value": 0.0                   # Valor que se fijará si se cumple la condición
                },

                # ─────────────────────────────────────────────────────────────
                # EJEMPLO 3: Activa un campo si una checkbox está marcada
                # ─────────────────────────────────────────────────────────────
                {
                    "trigger": "source_cb1",       # Checkbox "AlignSource"
                    "expected": True,
                    "action": "normal",            # "normal" reactiva (enable)
                    "targets": ["source_lbe3", "source_lbe4"]
                },
                # ─────────────────────────────────────────────────────────────
                # EJEMPLO 4: Desactiva/Activa un checkbox en función del valor de un campo
                # ─────────────────────────────────────────────────────────────
                {
                    "trigger": "detector_lcb1",     # <- Es un LabelCombobox (DetectorModel)
                    "expected": "MCD",              # <- Esperas que el valor sea 'MCD'
                    "action": "disable",            # <- Acción a aplicar
                    "targets": ["detector_cb1"]      # <- Por ejemplo, desactivar un CheckBox
                }

        ]
        setup_gui_rules = [
             
            # ─────────────────────────────────────────────────────────────
            # MAIN RULES
            # ─────────────────────────────────────────────────────────────
            {
            "trigger": "main_cb8",
            "expected": True,
            "action": "disable",
            "targets": ["main_lbe1", "main_lbe2"] 
            },
            # ─────────────────────────────────────────────────────────────
            # GEOMETRY RULES       
            # ─────────────────────────────────────────────────────────────
            {
                "trigger": "geometry_cb2",
                "expected": True,
                "action": "disable",
                "targets": ["geometry_lbe4", "geometry_lbe5", "geometry_lbe6", "geometry_lbe7"]
            },
            {
                "trigger": "geometry_cb1",
                "expected": False,
                "action": "disable",
                "targets": ["geometry_lcb2"]
            },
            {
                "trigger": "geometry_cb1",
                "expected": True,
                "action":"disable",
                "targets": ["geometry_lcb1","geometry_lbe3"]
            },
            {
                "trigger": "geometry_cb2",
                "expected": False,
                "action":"disable",
                "targets": ["geometry_cb3","geometry_lbe4","geometry_lbe5","geometry_lbe6","geometry_lbe7","geometry_lbe8","geometry_lbe9","geometry_lbe10"]
            },
            {
                "trigger": "geometry_cb3",
                "expected": False,
                "action":"disable",
                "targets": ["geometry_lbe4","geometry_lbe5","geometry_lbe6","geometry_lbe7","geometry_lbe8","geometry_lbe9","geometry_lbe10"]
            },
            # ─────────────────────────────────────────────────────────────
            # SOURCE RULES
            # ─────────────────────────────────────────────────────────────
            {
                "trigger": "source_cb1",
                "expected": True,
                "action": "disable",
                "targets": ["source_lbe3", "source_lbe4"]
            },
            {
                "trigger": "source_cb2",
                "expected": True,
                "action": "disable",
                "targets": ["source_lbe5", "source_lbe6", "source_lbe7"]
            },
            # ─────────────────────────────────────────────────────────────
            # DETECTOR RULES    
            # ─────────────────────────────────────────────────────────────
            {
                "trigger": "detector_cb1",
                "expected": False,
                "action": "disable",
                "targets": ["detector_lbe8", "detector_lbe9", "detector_lbe10"]
            },
            {
                "trigger": "detector_cb2",
                "expected": True,
                "action": "disable",
                "targets": ["detector_lbe3", "detector_lbe4"]
            },
            {
                "trigger": "geometry_cb1",
                "expected": False,
                "action":"set",
                "targets": ["detector_cb2"],
                "value": "No"
            },
            {
                "trigger": "geometry_cb1",
                "expected": False,
                "action": "disable",
                "targets": ["detector_cb2"]
            },
            {
                "trigger": "detector_lcb1",
                "expected": "No",
                "action": "disable",
                "targets":  ["detector_lcb2",
                            "detector_lcb3",
                            "detector_lcb4", 
                            "detector_lbe2",
                            "detector_lbe3",
                            "detector_lbe4",
                            "detector_lbe5",
                            "detector_lbe6",
                            "detector_lbe8",
                            "detector_lbe9",
                            "detector_lbe10",
                            "detector_lbe11",
                            "detector_lbe13",
                            "detector_cb1",
                            "detector_cb1"
                            ]
            },
            # ───────────────────────────────────────────────────────────
            # SCORING RULES
            # ────────────────────────────────────────────────────────────
            {
                "trigger": "scoring_cb4",
                "expected": False,
                "action": "disable",
                "targets": [
                        "scoring_lcb1",
                        "scoring_lbe1", 
                        "scoring_lbe2", 
                        "scoring_lbe3", 
                        "scoring_lbe5", 
                        "scoring_lbe6", 
                        "scoring_lbe7",
                        "scoring_lbe4",
                        "scoring_cb1",
                        "scoring_cb2",
                        ]
            },
            {
                "trigger": "scoring_cb1",
                "expected": True,
                "action": "set",
                "targets": ["scoring_cb2"],
                "value": "No"
            },
            {
                "trigger": "scoring_cb1",
                "expected": False,
                "action": "set",
                "targets": ["scoring_cb2"],
                "value": "Yes"
            },
            {
                "trigger": "scoring_cb2",
                "expected": True,
                "action": "set",
                "targets": ["scoring_cb1"],
                "value": "No"
            },
            {
                "trigger": "scoring_cb2",
                "expected": False,
                "action": "set",
                "targets": ["scoring_cb1"],
                "value": "Yes"
            }

        ]
        
        setup_gui_rules_forAfter = [
            # ───────────────────────────────────────────────────────────
            # SCORING RULES
            # ────────────────────────────────────────────────────────────
            {
                "trigger": "geometry_cb1",
                "expected": False,
                "action": "disable",
                "targets": ["scoring_cb3"]
            }
             
        ]
        phantom_gui_rules = [
            {
                "trigger": "phantom_cb5",
                "expected": False,
                "action": "disable",
                "targets": [
                    "phantom_lbe1", "phantom_lbe2", "phantom_lbe3",
                    "phantom_lbe4", "phantom_lbe5", "phantom_lbe6"
                ]
            },
        ]
         
