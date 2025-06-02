from typing import Any, Dict, List
import pandas as pd
from tkinter import ttk
from datetime import datetime
#from src.tool_handler.notebook_handler import NOTEBOOKHandler as notebook

class TreeViewHandler:
    
    @staticmethod
    def clear_treeview(treeview):
        """
        Limpia un Treeview específico.
        :param treeview: El widget Treeview a limpiar.
        """
        treeview.delete(*treeview.get_children())

    @staticmethod
    def fill_treeview(treeview, data, highlight_column=None, titles=None, clearData=False):
        """
        Llena un Treeview con datos. Puede aceptar diccionarios, DataFrames, listas o un string único.
        
        :param treeview: El Treeview a llenar.
        :param data: Los datos a insertar (puede ser un dict, DataFrame, lista o un str único).
        :param highlight_column: Nombre de la columna para resaltar filas (opcional, solo para DataFrames).
        :param titles: Lista con los títulos de columnas (opcional, solo para diccionarios y DataFrames).
        :param clearData: Si es True, limpia el Treeview antes de llenarlo.
        """

        def formatear_dato(dato):
            """Formatea los datos antes de insertarlos en el Treeview."""
            if isinstance(dato, datetime):
                if pd.isna(dato):
                    return "NaT"
                return dato.strftime('%Y-%m-%d') if dato.time() == datetime.min.time() else dato.strftime('%H:%M')
            
            elif isinstance(dato, float):
                return f"{dato:.3f}"
            
            elif isinstance(dato, int):  # Si es entero, lo devuelve sin modificar
                return dato
            
            elif isinstance(dato, str):
                try:
                    hora_parseada = datetime.strptime(dato, '%H:%M:%S')
                    return hora_parseada.strftime('%H:%M')
                except ValueError:
                    return dato

            return str(dato)  # Para otros tipos de datos, los convierte en string

        # Limpiar el Treeview si es necesario
        if clearData:
            TreeViewHandler.clear_treeview(treeview=treeview)

        # --- Manejo de cadenas individuales ---
        if isinstance(data, str):
            data = [data]  # Convertir en lista con un solo elemento para que siga el flujo normal

        # --- Manejo de Diccionarios ---
        if isinstance(data, dict):
            treeview["columns"] = ["Valor"]
            treeview.heading("#0", text=titles[0] if titles else "")
            treeview.column("#0", width=100, anchor="w")    
            treeview.heading("Valor", text=titles[1] if titles else "")
            treeview.column("Valor", width=350, anchor="w")
        
            style = ttk.Style()
            style.configure("Treeview", font=("Arial", 12))
            style.configure("Treeview.Item", font=("Arial", 12, "bold"))

            for key, value in data.items():
                treeview.insert("", "end", text=key, values=(formatear_dato(value),))

        # --- Manejo de DataFrames ---
        elif isinstance(data, pd.DataFrame):
            treeview.configure(show="headings")  # Oculta la primera columna y muestra encabezados
            treeview["columns"] = list(data.columns)

            for col in data.columns:
                treeview.heading(col, text=col)
                treeview.column(col, width=150, anchor="center")

            for _, row in data.iterrows():
                formatted_row = [formatear_dato(cell) for cell in row]
                tags = ('resaltado',) if highlight_column and row[highlight_column] is False else ()
                treeview.insert("", "end", values=formatted_row, tags=tags)

            treeview.tag_configure('resaltado', background='lightcoral')

        # --- Manejo de Listas ---
        elif isinstance(data, list):
            treeview.configure(show="tree")  # Oculta los encabezados de columna
            treeview["columns"] = ["Valor"]
            treeview.heading("#0", text="")
            treeview.column("#0", width=0)  # Ocultar la primera columna
            treeview.heading("Valor", text="")
            treeview.column("Valor", width=350, anchor="w")

            # 🔤 Aplicar estilo con fuente más grande solo en listas
            style = ttk.Style()
            style.configure("Treeview", font=("Arial", 11))

            for item in data:
                treeview.insert("", "end", values=(formatear_dato(item),))


        else:
            raise ValueError("El tipo de datos debe ser dict, DataFrame, lista o string único.")

    @staticmethod
    def specialfill_treeview(treeview, df, highlight_column):
        """
        Muestra un DataFrame en el Treeview con posibilidad de resaltar filas en función de una columna y editar celdas específicas.
        
        :param treeview: El Treeview donde se mostrarán los datos.
        :param df: El DataFrame que se desea mostrar.
        :param highlight_column: Columna que se usará para resaltar filas si su valor es False.
        """
        TreeViewHandler.clear_treeview(treeview)
        treeview["columns"] = list(df.columns)
        treeview["show"] = "headings"

        # Configurar encabezados y columnas
        for column in df.columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=150, anchor="center")

        # Insertar datos en el Treeview, vinculando el iid al índice del DataFrame
        for index, row in df.iterrows():
            # Resaltar solo si el valor en highlight_column es exactamente False
            tags = ('resaltado',) if row[highlight_column] is False else ()
            treeview.insert("", "end", iid=index, values=list(row), tags=tags)

        # Configurar estilos
        treeview.tag_configure('resaltado', background='lightcoral')

        # Función para editar celdas específicas
        def edit_cell(event):
            # Identificar fila y columna del clic
            row_id = treeview.identify_row(event.y)
            column = treeview.identify_column(event.x)

            if not row_id or not column:
                return

            # Obtener el nombre de la columna
            col_index = int(column[1:]) - 1
            col_name = treeview["columns"][col_index]

            # Limitar la edición a columnas específicas (opcional)
            if col_name in ['Referencia', 'Informar']:
                # Obtener coordenadas de la celda seleccionada
                x, y, width, height = treeview.bbox(row_id, column)

                # Obtener el valor actual
                current_value = treeview.set(row_id, column)

                # Crear Combobox para edición
                combobox = ttk.Combobox(treeview, values=["True", "False"], state="readonly")
                combobox.place(x=x, y=y, width=width, height=height)
                combobox.set(current_value)

                # Función para actualizar el Treeview y el DataFrame
                def on_select(event):
                    new_value = combobox.get()
                    treeview.set(row_id, column, new_value)

                    # Actualizar el DataFrame original
                    df.at[int(row_id), col_name] = True if new_value == "True" else False

                    # Debug: Verificar cambios reflejados
                    print(f"Actualizado df[{int(row_id)}, {col_name}] = {df.at[int(row_id), col_name]}")

                    combobox.destroy()

                combobox.bind("<<ComboboxSelected>>", on_select)
                combobox.focus()

        # Vincular la función de edición al evento de doble clic
        treeview.bind("<Double-1>", edit_cell)
    
    @staticmethod
    def resaltar_fila(treeview, columna, valor):
        """
        Resalta una fila en verde en un Treeview según el valor en una columna específica.

        Args:
            treeview (ttk.Treeview): El widget Treeview en el que se busca la fila.
            columna (str): El identificador de la columna a buscar (debe coincidir con el nombre de la clave en los datos).
            valor (str): El valor a buscar en la columna especificada.
        """
        # Iterar sobre todos los elementos del Treeview
        for item in treeview.get_children():
            item_values = treeview.item(item, 'values')  # Obtener los valores de la fila
            try:
                # Buscar el índice de la columna
                col_index = treeview["columns"].index(columna)
                # Comparar el valor
                if item_values[col_index] == valor:
                    # Resaltar la fila en verde
                    treeview.tag_configure('highlight', background='lightgreen')
                    treeview.item(item, tags=('highlight',))
                    break
            except ValueError:
                print(f"La columna '{columna}' no existe en el Treeview.")
                break
    
    '''@staticmethod
    def mostrar_en_treeview(
        notebook_elements: Dict[str, Dict[str, ttk.Treeview]],
        notebook_config: List[Dict[str, Any]],
        tab_index: int,
        treeview_index: int,
        data2show: pd.DataFrame
        )-> None:

        """
        Muestra los datos de un data frame pasado por argumento, en un treeview contenido en la configuración
        de un notebook

        parametros:
        :notebook_elements (dict[str,dict[str,treeview]]): diccionario que continene los treeview contenidos en el treeview
        :notebook_config (list(dict(str,any))): lista de diccionarios que contienen la configuración que define el notebook
        :tab_index (int): Indice de la tab del notebook desde donde queremos acceder al treeview (0 primera tab, 1 la seguinda, ....)
        :treeview_index (int): Indice del treeview que queremos recuperar (0 primero, 1 segundo....)
        :data2show (pd.dataframe): Dataframe con los datos para mostrar en el treeview
        """
        
        treeview = notebook.get_treeview(
            notebook_cfg=notebook_config,
            notebook_elements=notebook_elements,
            tab_index=tab_index,
            treeview_index=treeview_index,
        )

        TreeViewHandler.fill_treeview(
            treeview=treeview,
            data=data2show,
            clearData=True
        )'''




   