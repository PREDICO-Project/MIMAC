import json
import os
from tkinter import messagebox


class PANELCONTROLHandler():

    @staticmethod
    def load_panelControl_cfg(file_path: str) -> list:
        try:
            # Convertir la ruta a formato compatible con el sistema
            file_path = os.path.normpath(file_path)

            # Cargar configuración desde JSON
            with open(file_path, "r", encoding="utf-8") as f:
                controlPanel_cfg = json.load(f)
                return controlPanel_cfg

        except FileNotFoundError:
            messagebox.showerror(
                title='Error',
                message=f'No se ha encontrado la cfg: {file_path}'
            )
        except json.JSONDecodeError:
            messagebox.showerror(
                title='Error',
                message=f'Error en el formato JSON de la cfg: {file_path}'
            )
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message=f'Ocurrió un error al cargar la cfg: {file_path}\n{str(e)}'
            )

        return []
        