import os
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional, Tuple, Union, Callable
from PIL import Image, ImageTk

class WIDGETFactory:
    """
    Clase para manejar la creación de widgets personalizados en Tkinter.

    Esta clase proporciona métodos estáticos para crear diversos widgets de Tkinter,
    incluyendo frames, etiquetas, entradas, botones, checkboxes, comboboxes, áreas de texto,
    y etiquetas con imágenes. Facilita la reutilización y consistencia en la interfaz de usuario.

    Métodos Estáticos:
        - create_frame: Crea un frame con estilo personalizado.
        - create_label_entry: Crea un par de etiqueta y entrada con opciones adicionales.
        - create_button: Crea un botón con texto y comandos específicos.
        - create_label: Crea una etiqueta simple.
        - create_checkbox: Crea un checkbox con texto y opciones.
        - create_label_file_combobox: Crea una etiqueta y combobox poblados con nombres de archivos.
        - create_label_with_image: Crea una etiqueta que contiene una imagen.
        - create_label_combobox: Crea una etiqueta y combobox con valores específicos.
        - create_text_area: Crea un área de texto configurable.
        - create_label_entry_with_image: Crea una etiqueta y una etiqueta con imagen asociada.
    """

    @staticmethod
    def create_frame(master: Any, text: Optional[str] = None, row: int = 0, column: int = 0,
                    padx: int = 10, pady: int = 10, sticky: str = "nsew",
                    font: Tuple[str, int] = ("Arial", 12), background: str = "#ffffff") -> ttk.LabelFrame:
        """
        Crea un frame con estilo personalizado.

        Args:
            master (Any): Widget contenedor.
            text (Optional[str], optional): Texto para el LabelFrame. Por defecto es None.
            row (int, optional): Fila en la que se colocará el frame. Por defecto es 0.
            column (int, optional): Columna en la que se colocará el frame. Por defecto es 0.
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 10.
            sticky (str, optional): Alineación del frame en la celda. Por defecto es "nsew".
            font (Tuple[str, int], optional): Fuente y tamaño del texto. Por defecto es ("Arial", 12).
            background (str, optional): Color de fondo del frame. Por defecto es "#ffffff".

        Returns:
            ttk.LabelFrame: Frame creado con las configuraciones especificadas.
        """
        # Crear un estilo personalizado
        style_name = "Custom.TLabelframe"
        style = ttk.Style()
        style.configure(style_name, font=font, background=background)

        # Crear y colocar el LabelFrame con el estilo personalizado
        frame = ttk.LabelFrame(master, text=text, style=style_name)
        frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

        return frame

    @staticmethod
    def create_label_entry(master: Any, 
                           label_text: str, 
                           row: int, 
                           column: int, 
                           padx: int = 10,
                           pady: int = 5,
                           vertical: bool = False, 
                           inactive: bool = False,
                           textvariable: Optional[tk.StringVar] = None, 
                           width_entry: int = 20,
                           validate: Optional[str] = None, 
                           validatecommand: Optional[Any] = None,
                           checkboxes: Optional[List[tk.BooleanVar]] = None,
                           activate_on_check: Union[bool, List[bool]] = True
                        ) -> Tuple[ttk.Label, ttk.Entry]:
        """
        Crea un par de widgets Etiqueta y Entrada en una ventana o frame, y asocia la activación/desactivación del Entry
        al estado de los checkboxes dados.

        Args:
            master (Any): Widget contenedor.
            label_text (str): Texto para la etiqueta.
            row (int): Fila en la que se colocarán los widgets.
            column (int): Columna en la que se colocará la etiqueta.
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 10.
            vertical (bool, optional): Si es True, coloca el Entry en la fila siguiente. Por defecto es False.
            inactive (bool, optional): Si es True, desactiva el Entry inicialmente. Por defecto es False.
            textvariable (Optional[tk.StringVar], optional): Variable de texto asociada al Entry. Por defecto es None.
            width_entry (int, optional): Ancho del Entry. Por defecto es 10.
            validate (Optional[str], optional): Tipo de validación para el Entry. Por defecto es None.
            validatecommand (Optional[Any], optional): Comando de validación para el Entry. Por defecto es None.
            checkboxes (Optional[List[tk.BooleanVar]], optional): Lista de variables asociadas a checkboxes que controlan el Entry.
                Por defecto es None.
            activate_on_check (Union[bool, List[bool]], optional): Si es True, el Entry se activa si al menos un checkbox está seleccionado.
                Si es False, el Entry se activa solo si ningún checkbox está seleccionado.
                También puede ser una lista de booleanos para controles más complejos. Por defecto es True.

        Returns:
            Tuple[ttk.Label, ttk.Entry]: Objetos de la etiqueta y entrada creados.
        """
        label = ttk.Label(master, text=label_text)
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky="w")

        entry = ttk.Entry(master, textvariable=textvariable, width=width_entry,
                          validate=validate, validatecommand=validatecommand)
        if vertical:
            entry.grid(row=row + 1, column=column, padx=padx, pady=pady, sticky="w")
        else:
            entry.grid(row=row, column=column + 1, padx=padx, pady=pady, sticky="w")

        def update_entry_style() -> None:
            """
            Actualiza el estilo del Entry según su estado.
            """
            if entry['state'] == tk.DISABLED:
                entry.config(foreground="red", font=('Helvetica', 9, 'bold'))
            else:
                entry.config(foreground="black", font=('Helvetica', 9))

        if inactive:
            entry.config(state=tk.DISABLED)
            update_entry_style()

        if checkboxes:
            # Asegurarse de que checkboxes sea siempre una lista
            if not isinstance(checkboxes, list):
                checkboxes = [checkboxes]

            # Asegurarse de que activate_on_check sea siempre una lista del mismo tamaño que checkboxes
            if not isinstance(activate_on_check, list):
                activate_on_check = [activate_on_check] * len(checkboxes)

            def actualizar_entry(*args) -> None:
                """
                Actualiza el estado del Entry basado en el estado de los checkboxes.
                """
                if len(set(activate_on_check)) == 1:
                    # Todos los valores de activate_on_check son iguales
                    if activate_on_check[0]:
                        is_active = any(cb.get() for cb in checkboxes)
                    else:
                        is_active = all(not cb.get() for cb in checkboxes)
                else:
                    # Los valores de activate_on_check son diferentes
                    is_active = all(cb.get() if aoc else not cb.get()
                                   for cb, aoc in zip(checkboxes, activate_on_check))

                entry.config(state=tk.NORMAL if is_active else tk.DISABLED)
                update_entry_style()

            for cb in checkboxes:
                cb.trace_add("write", actualizar_entry)  # Usar trace_add para llamar a actualizar_entry cuando alguna variable cambia

            actualizar_entry()  # Llamar una vez al inicio para sincronizar el estado inicial

        return label, entry

    @staticmethod
    def create_button(master: Any, button_text: str, row: int, column: int, padx: int = 10,
                    pady: int = 10, sticky: str = 'w', columnspan: int = 1,
                    state: str = "normal", command: Optional[Any] = None,
                    width: Optional[int] = None) -> ttk.Button:
        """
        Crea un botón en una ventana o frame.

        ...
        width (Optional[int], optional): Ancho del botón en caracteres. Por defecto es None.

        Returns:
            ttk.Button: Botón creado con las configuraciones especificadas.
        """
        kwargs = {"text": button_text, "state": state, "command": command}
        if width is not None:
            kwargs["width"] = width

        button = ttk.Button(master, **kwargs)
        button.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)

        return button

    @staticmethod
    def create_label(master: Any, text: str, row: int, column: int, text_size:int = 10, sticky: str = "w",
                    padx: int = 10, pady: int = 5, columnspan: int = 1, bold: bool = False,
                    colorText: str = '', text_align: str = "left", wraplength=None) -> ttk.Label:
        """
        Crea una etiqueta en una ventana o frame.

        Args:
            master (Any): Widget contenedor.
            text (str): Texto que se mostrará en la etiqueta.
            row (int): Fila en la que se colocará la etiqueta.
            column (int): Columna en la que se colocará la etiqueta.
            sticky (str, optional): Alineación de la etiqueta en la celda. Por defecto es "w".
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 5.
            columnspan (int, optional): Número de columnas que abarca la etiqueta. Por defecto es 1.
            bold (bool, optional): Si True, el texto se mostrará en negrita. Por defecto es False.
            colorText (str, optional): Color del texto de la etiqueta. Por defecto es 'Black'.
            text_align (str, optional): Alineación del texto dentro de la etiqueta ('left', 'center', 'right').

        Returns:
            ttk.Label: Etiqueta creada con las configuraciones especificadas.
        """

        # Configurar la fuente
        font = ("TkDefaultFont", text_size, "bold") if bold else ("TkDefaultFont", 10)

        # Mapear la alineación del texto
        anchor_map = {
            "left": "w",
            "center": "center",
            "right": "e"
        }

        # Obtener el valor de `anchor` según la alineación deseada
        anchor = anchor_map.get(text_align, "w")  # Por defecto 'left' -> 'w'

        # Crear la etiqueta
        if wraplength is None:
            label = ttk.Label(master, text=text, font=font, foreground=colorText, anchor=anchor)
        else:
            label = ttk.Label(master, text=text, font=font, foreground=colorText, anchor=anchor,
                              wraplength=wraplength)
        #label = ttk.Label(master, text=text, font=font, anchor=anchor)

        # Posicionar la etiqueta en la cuadrícula
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan)

        return label

    @staticmethod
    def create_checkbox(master: Any, text: str, row: int, column: int,
                        variable: Optional[tk.BooleanVar] = None, sticky: str = "w",
                        padx: int = 10, pady: int = 5, command: Optional[Any] = None) -> ttk.Checkbutton:
        """
        Crea un checkbox con su texto en una ventana o frame.

        Args:
            master (Any): Widget contenedor.
            text (str): Texto que se mostrará junto al checkbox.
            row (int): Fila en la que se colocará el checkbox.
            column (int): Columna en la que se colocará el checkbox.
            variable (Optional[tk.BooleanVar], optional): Variable de control asociada al checkbox. Por defecto es None.
            sticky (str, optional): Alineación del checkbox en la celda. Por defecto es "w".
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 5.
            command (Optional[Any], optional): Comando que se ejecutará al cambiar el estado del checkbox. Por defecto es None.

        Returns:
            ttk.Checkbutton: Checkbox creado con las configuraciones especificadas.
        """
        if not isinstance(variable, tk.BooleanVar):
            variable = tk.BooleanVar(value=bool(variable))  # Asegura que siempre sea una instancia única

        checkbox = ttk.Checkbutton(master, text=text, variable=variable, command=command)
        checkbox.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

        checkbox.invoke() 

        return checkbox

    @staticmethod
    def create_label_file_combobox(master: Any, label_text: str, directory_path: str,
                                   row: int, column: int, combobox_textvariable: Optional[tk.StringVar] = None,
                                   state: str = "readonly", file_extension: str = "all",
                                   distribution: str = 'horizontal') -> Tuple[ttk.Label, ttk.Combobox]:
        """
        Crea una etiqueta y un combobox en una ventana o frame. Los nombres de los archivos de un directorio
        especificado son usados como valores del combobox. Se puede especificar la extensión de los archivos a listar.

        Args:
            master (Any): Widget contenedor.
            label_text (str): Texto para la etiqueta.
            directory_path (str): Ruta del directorio del cual se obtendrán los nombres de los archivos para el combobox.
            row (int): Fila en la que se colocarán los widgets.
            column (int): Columna en la que se colocará la etiqueta. El combobox se colocará en la siguiente columna.
            combobox_textvariable (Optional[tk.StringVar], optional): Variable de texto asociada al combobox.
                Si es None, se crea una nueva. Por defecto es None.
            state (str, optional): Estado del combobox ('readonly' para solo lectura o 'normal' para editable).
                Por defecto es "readonly".
            file_extension (str, optional): Extensión de los archivos a listar (ej. 'txt'). 'all' para todos los archivos.
                Por defecto es "all".
            distribution (str, optional): Distribución del label/combobox, 'horizontal' o 'vertical'. Por defecto es 'horizontal'.

        Returns:
            Tuple[ttk.Label, ttk.Combobox]: Objetos de la etiqueta y combobox creados.
        """
        # Crear y colocar la etiqueta
        label = ttk.Label(master, text=label_text)
        label.grid(row=row, column=column, padx=10, pady=5, sticky="w")

        # Si no se proporciona una variable de texto, crea una nueva
        if combobox_textvariable is None:
            combobox_textvariable = tk.StringVar(master)

        # Intenta listar los nombres de archivo en el directorio especificado con la extensión dada
        try:
            if file_extension.lower() == "all":
                file_names = [f for f in os.listdir(directory_path)
                             if os.path.isfile(os.path.join(directory_path, f))]
            else:
                file_names = [f for f in os.listdir(directory_path)
                             if f.lower().endswith('.' + file_extension.lower()) and
                             os.path.isfile(os.path.join(directory_path, f))]
            file_names.insert(0, 'None')
        except FileNotFoundError:
            file_names = ['Directorio no encontrado']
        except PermissionError:
            file_names = ['Permiso denegado']
        except Exception as e:
            file_names = [f'Error: {e}']

        # Crear y colocar el combobox según la variable distribution
        if distribution.lower() == 'horizontal':
            combobox = ttk.Combobox(master, textvariable=combobox_textvariable,
                                     values=file_names, state=state)
            combobox.grid(row=row, column=column + 1, padx=10, pady=5, sticky="w")
        elif distribution.lower() == 'vertical':
            combobox = ttk.Combobox(master, textvariable=combobox_textvariable,
                                     values=file_names, state=state)
            combobox.grid(row=row + 1, column=column, padx=10, pady=5, sticky="w")
        else:
            # Por defecto, distribución horizontal si el valor es desconocido
            combobox = ttk.Combobox(master, textvariable=combobox_textvariable,
                                     values=file_names, state=state)
            combobox.grid(row=row, column=column + 1, padx=10, pady=5, sticky="w")

        return label, combobox

    @staticmethod
    def create_label_with_image(master: Any, image_path: str, row: int, column: int, rowspan: int = 1, columnspan: int = 1,
                                img_sizeX: int = 150, img_sizeY: int = 150,
                                padx: int = 10, pady: int = 10, sticky: str = "w") -> tk.Label:
        """
        Crea una etiqueta en una ventana o frame que contiene una imagen.

        Args:
            master (Any): Widget contenedor.
            image_path (str): Ruta de la imagen a mostrar.
            row (int): Fila en la que se colocará la etiqueta.
            column (int): Columna en la que se colocará la etiqueta.
            img_sizeX (int, optional): Ancho de la imagen. Por defecto es 150.
            img_sizeY (int, optional): Alto de la imagen. Por defecto es 100.
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 10.
            sticky (str, optional): Alineación de la etiqueta en la celda. Por defecto es "w".

        Returns:
            tk.Label: Etiqueta con la imagen cargada.
        """
        # Cargar la imagen
        try:
            image = Image.open(image_path)
            image = image.resize((img_sizeX, img_sizeY), Image.LANCZOS)  # Redimensionar la imagen si es necesario
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error al cargar la imagen '{image_path}': {e}")
            photo = None

        # Crear el Label y asignar la imagen
        label = tk.Label(master, image=photo, background="gray20")
        if photo:
            label.image = photo  # Guardar una referencia a la imagen para evitar que sea recolectada por el garbage collector
        label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan,padx=padx, pady=pady, sticky=sticky)

        return label

    @staticmethod
    def create_label_combobox(
        master: Any,
        label_text: str,
        names: List[str],
        row: int,
        column: int,
        horizontal: bool = True,
        sticky: str = "w",
        combobox_textvariable: Optional[tk.StringVar] = None,
        combobox_width: int = None ,
        state: str = "readonly",
        callback: Optional[Callable[[str], None]] = None  # Nuevo parámetro callback
    ) -> Tuple[ttk.Label, ttk.Combobox]:
        """
        Crea una etiqueta y un combobox en una ventana o frame.

        Args:
            master (Any): Widget contenedor.
            label_text (str): Texto para la etiqueta.
            names (List[str]): Valores para el combobox.
            row (int): Fila en la que se colocarán los widgets.
            column (int): Columna en la que se colocará la etiqueta. El combobox se colocará en la siguiente columna.
            horizontal (bool, optional): Si True, el combobox se coloca en la misma fila que la etiqueta.
                Por defecto es True.
            combobox_textvariable (Optional[tk.StringVar], optional): Variable de texto asociada al combobox.
                Si es None, se crea una nueva. Por defecto es None.
            state (str, optional): Estado del combobox ('readonly' para solo lectura o 'normal' para editable).
                Por defecto es "readonly".
            callback (Optional[Callable[[str], None]], optional): Función a ejecutar cuando cambie el valor del combobox.
                La función debe aceptar un argumento: el nuevo valor seleccionado. Por defecto es None.


        Returns:
            Tuple[ttk.Label, ttk.Combobox]: Objetos de la etiqueta y combobox creados.
        """
        # Crear y colocar la etiqueta
        label = ttk.Label(master, text=label_text)
        label.grid(row=row, column=column, padx=10, pady=5, sticky=sticky)

        # Si no se proporciona una variable de texto, crea una nueva
        if combobox_textvariable is None:
            combobox_textvariable = tk.StringVar(master)

         # Manejar caso en que `names` sea None o esté vacío
        if not names:
            names = [""]  # Valor por defecto si la lista está vacía o es None

        # Calcular el ancho del combobox basado en el contenido con un ancho mínimo estándar
        if combobox_width is None:
            min_width = 15  # Tamaño estándar mínimo
            max_width = max((len(str(item)) for item in names), default=min_width)
            final_width = max(min_width, max_width)  # Asegurar que nunca sea menor que el mínimo
        else:
            final_width = combobox_width

        # Crear y colocar el combobox
        combobox = ttk.Combobox(
            master,
            textvariable=combobox_textvariable,
            values=names,
            state=state,
            width=final_width,  # Configurar ancho dinámico con mínimo estándar
        )
        if horizontal:
            combobox.grid(row=row, column=column + 1, padx=10, pady=5, sticky=sticky)
        else:
            combobox.grid(row=row + 1, column=column, padx=10, pady=5, sticky=sticky)
        
         # Vincular el evento para ejecutar la función callback
        if callback:
            combobox.bind("<<ComboboxSelected>>", lambda event: callback(combobox.get()))

        return label, combobox

    @staticmethod
    def create_text_area(master: Any, row: int, column: int, height: int = 10,
                        width: int = 20, padx: int = 20, pady: int = 20,
                        wrap: str = tk.WORD, background: str = "gray20",
                        foreground: str = "white", font: Tuple[str, int] = ('Comic Sans', 10)) -> tk.Text:
        """
        Crea un área de texto en una ventana o frame que es no editable por defecto.

        Args:
            master (Any): Widget contenedor.
            row (int): Fila en la que se colocará el área de texto.
            column (int): Columna en la que se colocará el área de texto.
            height (int, optional): Alto del área de texto en líneas. Por defecto es 10.
            width (int, optional): Ancho del área de texto en caracteres. Por defecto es 20.
            padx (int, optional): Padding en el eje x. Por defecto es 20.
            pady (int, optional): Padding en el eje y. Por defecto es 20.
            wrap (str, optional): Tipo de envolvimiento de texto ('word' o 'char'). Por defecto es tk.WORD.
            background (str, optional): Color de fondo del área de texto. Por defecto es "white".
            foreground (str, optional): Color del texto en el área de texto. Por defecto es "black".
            font (Tuple[str, int], optional): Fuente y tamaño del texto. Por defecto es ('Comic Sans', 10).

        Returns:
            tk.Text: Área de texto creada con las configuraciones especificadas.
        """
        text_area = tk.Text(master, height=height, width=width, wrap=wrap,
                            padx=padx, pady=pady, background=background,
                            foreground=foreground, font=font, borderwidth=1)
        text_area.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
        # text_area.configure(state="disabled")  # Descomentar para hacer el área de texto no editable

        return text_area

    @staticmethod
    def create_label_entry_with_image(master: Any, label_text: str, image_path: str,
                                     row: int, column: int, img_sizeX: int = 150,
                                     img_sizeY: int = 100, padx: int = 10, pady: int = 10,
                                     sticky: str = "w") -> Tuple[ttk.Label, tk.Label]:
        """
        Crea una etiqueta y una etiqueta con una imagen en una ventana o frame.

        Args:
            master (Any): Widget contenedor.
            label_text (str): Texto para la etiqueta.
            image_path (str): Ruta de la imagen a mostrar en la etiqueta.
            row (int): Fila en la que se colocarán los widgets.
            column (int): Columna en la que se colocarán los widgets.
            img_sizeX (int, optional): Ancho de la imagen. Por defecto es 150.
            img_sizeY (int, optional): Alto de la imagen. Por defecto es 100.
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 10.
            sticky (str, optional): Alineación de los widgets en la celda. Por defecto es "w".

        Returns:
            Tuple[ttk.Label, tk.Label]: Objetos de la etiqueta y etiqueta de imagen creados.
        """
        label = ttk.Label(master, text=label_text)
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

        image_label = WIDGETFactory.create_label_with_image(master, image_path, row=row, column=column + 1,
                                                            img_sizeX=img_sizeX, img_sizeY=img_sizeY,
                                                            padx=padx, pady=pady, sticky=sticky)

        return label, image_label

    @staticmethod
    def create_label_checkbox(
        master: Any, 
        label_text: str, 
        checkbox_text: str, 
        row: int, 
        column: int,
        horizontal: bool = True, 
        padx: int = 10, 
        pady: int = 5, 
        sticky: str = "w",
        variable: Optional[tk.BooleanVar] = None,
        command: Optional[Callable[[], None]] = None
    ) -> Tuple[ttk.Label, ttk.Checkbutton]:
        """
        Crea un par de etiqueta y checkbox en una ventana o frame.

        Args:
            master (Any): Widget contenedor.
            label_text (str): Texto para la etiqueta.
            checkbox_text (str): Texto para el checkbox.
            row (int): Fila en la que se colocarán los widgets.
            column (int): Columna en la que se colocará la etiqueta.
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 5.
            sticky (str, optional): Alineación de los widgets en la celda. Por defecto es "w".
            variable (Optional[tk.BooleanVar], optional): Variable de control del checkbox. Si es None, se crea una nueva.
            command (Optional[Callable[[], None]], optional): Función a ejecutar cuando se cambia el estado del checkbox.

        Returns:
            Tuple[ttk.Label, ttk.Checkbutton]: Objetos de la etiqueta y checkbox creados.
        """
        if variable is None:
            variable = tk.BooleanVar(value=False)  # Asegurar que cada checkbox tenga su propia variable

        # Crear y configurar la etiqueta con padding ajustado
        label = ttk.Label(master, text=label_text, anchor="w")
        label.grid(row=row, column=column, padx=(padx + 5, padx), pady=pady, sticky=sticky)  # Ajuste extra de padding izquierdo

        # Ajustar estilo del Checkbutton para alineación correcta
        style = ttk.Style()
        style.configure("Custom.TCheckbutton", padding=(5, 2, 5, 2), anchor="w")  # Ajusta el padding

        # Crear y colocar el checkbox con el nuevo estilo
        checkbox = ttk.Checkbutton(master, text=checkbox_text, variable=variable, command=command, style="Custom.TCheckbutton")

        if horizontal:
            checkbox.grid(row=row, column=column + 1, padx=padx, pady=pady, sticky=sticky)
        else:
            checkbox.grid(row=row + 1, column=column, padx=padx, pady=pady, sticky=sticky)

        return label, checkbox

    @staticmethod
    def create_radiobutton(
        master: Any, 
        text: str,  
        row: int, 
        column: int,
        padx: int = 10, 
        pady: int = 5, 
        sticky: str = "w",
        state: str = "normal",
        variable: Optional[tk.StringVar] = None,
        value: str = ""
    ) -> ttk.Radiobutton:
        """
        Generates a label and a radiobutton in a window or frame.
        """
        radiobutton = ttk.Radiobutton(master, text=text, variable = variable, value=value, state=state)
        radiobutton.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        return radiobutton
    
    ''' @staticmethod
    def create_label_checkbox(
        master: Any, 
        label_text: str, 
        checkbox_text: str, 
        row: int, 
        column: int,
        horizontal: bool = True, 
        padx: int = 10, 
        pady: int = 5, 
        sticky: str = "w",
        variable: Optional[tk.BooleanVar] = None,
        command: Optional[Callable[[], None]] = None
    ) -> Tuple[ttk.Label, ttk.Checkbutton]:
        """
        Crea un par de etiqueta y checkbox en una ventana o frame.

        Args:
            master (Any): Widget contenedor.
            label_text (str): Texto para la etiqueta.
            checkbox_text (str): Texto para el checkbox.
            row (int): Fila en la que se colocarán los widgets.
            column (int): Columna en la que se colocará la etiqueta.
            padx (int, optional): Padding en el eje x. Por defecto es 10.
            pady (int, optional): Padding en el eje y. Por defecto es 5.
            sticky (str, optional): Alineación de los widgets en la celda. Por defecto es "w".
            variable (Optional[tk.BooleanVar], optional): Variable de control del checkbox. Si es None, se crea una nueva.
            command (Optional[Callable[[], None]], optional): Función a ejecutar cuando se cambia el estado del checkbox.

        Returns:
            Tuple[ttk.Label, ttk.Checkbutton]: Objetos de la etiqueta y checkbox creados.
        """
        if variable is None:
            variable = tk.BooleanVar(value=False)  # Asegurar que cada checkbox tenga su propia variable

        # Crear y colocar la etiqueta
        label = ttk.Label(master, text=label_text)
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

        # Crear y colocar el checkbox
        checkbox = ttk.Checkbutton(master, text=checkbox_text, variable=variable, command=command)
        if horizontal:
            checkbox.grid(row=row, column=column + 1, padx=padx, pady=pady, sticky=sticky)
        else:
            checkbox.grid(row=row + 1, column=column, padx=padx, pady=pady, sticky=sticky)

        return label, checkbox'''