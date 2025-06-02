import os
import sys

class FolderHandler:

    @staticmethod
    def folder_content2list(directory_path:str, file_extension:str = 'all') -> list:
        
        try:
            if file_extension == "all":
                file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            else:
                file_names = [f for f in os.listdir(directory_path) if f.endswith('.' + file_extension) and os.path.isfile(os.path.join(directory_path, f))]
            file_names.insert(0,'None')
        except FileNotFoundError:
            file_names = ['Directorio no encontrado']
        except PermissionError:
            file_names = ['Permiso denegado']
        
        return file_names