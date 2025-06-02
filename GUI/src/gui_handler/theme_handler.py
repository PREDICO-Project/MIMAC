import tkinter as tk
from tkinter import ttk
from typing import Any


class THEMEHandler:
    """
    Clase para manejar la configuración de temas (modo oscuro y claro) en la interfaz de usuario utilizando ttk.Style.

    Esta clase proporciona métodos estáticos para configurar estilos personalizados en la interfaz de usuario de Tkinter,
    facilitando la alternancia entre modos oscuros y claros.

    Version:
        1.0.0

    Last Modified:
        2024-04-27

    Métodos Estáticos:
        - configure_dark_mode: Configura estilos para el modo oscuro.
        - configure_light_mode: Configura estilos para el modo claro.
    """

    @staticmethod
    def configure_dark_mode() -> None:
        """
        Configura los estilos de la interfaz para el modo oscuro utilizando ttk.Style.

        Configura colores de fondo, texto, fuentes y otros parámetros para widgets como Text, Label, Entry, Checkbutton, Button, Notebook y Frame.

        Version:
            1.0.0

        Last Modified:
            2024-04-27
        """
        font_type = 'Segoe UI'
        font_size = 10
        combobox_hover_background = "gray25"  # Color de fondo para hover en modo oscuro
        combobox_hover_foreground = "black"    # Color de texto durante hover

        style = ttk.Style()

        # Configuración de estilo para widgets
        style.configure("TText", background="gray12", foreground="white",
                        font=(font_type, font_size), borderwidth=1)
        style.configure("TLabel", background="gray20", foreground="white",
                        font=(font_type, font_size))
        style.configure("Custom.TLabelframe", background="gray20",
                        foreground="white", bordercolor="gray20")
        style.configure("TLabelframe.Label", background="gray20", foreground="white")
        style.configure("TEntry", background="gray35", foreground="black",
                font=(font_type, font_size))
        style.map("TEntry",
                fieldbackground=[
                    ("disabled", "gray30")
                ],
                foreground=[
                    ("disabled", "gray70")
                ],
                background=[
                    ("disabled", "gray30")
                ])

        style.configure("TCheckbutton", background="gray20", foreground="white",
                        indicatorcolor='red', font=(font_type, font_size))
        style.map('TCheckbutton',
          indicatorcolor=[
              ('pressed', 'white'),
              ('selected', 'green'),
              ('active', 'red'),
              ('invalid', 'red'),
              ('disabled', 'gray40')  # añadido aquí sin pisar lo anterior
          ],
          background=[
              ('disabled', 'gray20')
          ],
          foreground=[
              ('disabled', 'gray50')
          ])

        style.configure("TButton", background="gray35", foreground="white",
                        font=(font_type, font_size))

        # Configuración para ttk.Notebook (contenedor de pestañas)
        style.configure("TNotebook", background="gray20", borderwidth=0)
        style.configure("TNotebook.Tab", background="gray35", foreground="white",
                        padding=[5, 2], font=(font_type, font_size))
        style.map("TNotebook.Tab", background=[("selected", "gray20")],
                  expand=[("selected", [1, 1, 1, 0])])

        # Configurando el color de fondo de la ventana principal
        style.configure("TFrame", background="gray20")

        # Configuración de hover para TButton
        style.map("TButton", background=[("active", combobox_hover_background)])

        # Configuración de hover específica para TCombobox
        '''style.map("TCombobox",
                  fieldbackground=[("active", combobox_hover_background)],
                  foreground=[("active", combobox_hover_foreground)],
                  background=[("active", combobox_hover_background)])'''
        style.map("TCombobox",
          fieldbackground=[
              ("active", combobox_hover_background),
              ("disabled", "gray30")  # color de fondo cuando está deshabilitado
          ],
          foreground=[
              ("active", combobox_hover_foreground),
              ("disabled", "gray70")  # color de texto cuando está deshabilitado
          ],
          background=[
              ("active", combobox_hover_background),
              ("disabled", "gray30")
          ])
        
        style.configure("Treeview",
                background="gray15",
                foreground="white",
                fieldbackground="gray15",
                font=(font_type, font_size),
                rowheight=20,
                bordercolor="gray25")

        style.map("Treeview",
                background=[("selected", "gray30")],
                foreground=[("selected", "white")])

        style.configure("Treeview.Heading",
                        background="gray25",
                        foreground="white",
                        font=(font_type, font_size, "bold"))
        
        style.configure("TRadiobutton", background="gray20", foreground="white", font=(font_type, font_size), borderwidth=1)
        
        style.map("TRadiobutton",
                  background=[("active", combobox_hover_background)],
                  indicatorcolor=[('selected', '#00FF00')])



    @staticmethod
    def configure_light_mode() -> None:
        """
        Configura los estilos de la interfaz para el modo claro utilizando ttk.Style.

        Configura colores de fondo, texto, fuentes y otros parámetros para widgets como Text, Label, Entry, Checkbutton, Button, Notebook y Frame.

        Version:
            1.0.0

        Last Modified:
            2024-04-27
        """
        font_type = 'Comic Sans'
        font_size = 10
        style = ttk.Style()

        # Configuración de estilo para widgets
        style.configure("TText", background="white", foreground="black",
                        font=(font_type, font_size), borderwidth=1)
        style.configure("TLabel", background="#ffffff", foreground="#000000",
                        font=(font_type, font_size))
        style.configure("TEntry", background="#ffffff", foreground="#000000",
                        font=(font_type, font_size))
        style.configure("Custom.TLabelframe", background="white",
                        foreground="black", bordercolor="gray20")
        style.configure("TLabelframe.Label", background="white", foreground="black")
        style.configure("TEntry", background="white", foreground="black",
                        font=(font_type, font_size))
        style.map("TEntry",
          fieldbackground=[
              ("disabled", "#dddddd")
          ],
          foreground=[
              ("disabled", "#888888")
          ],
          background=[
              ("disabled", "#dddddd")
          ])

        style.configure("TCheckbutton", background="white", foreground="black",
                        indicatorcolor='red', font=(font_type, font_size))
        style.map('TCheckbutton',
          indicatorcolor=[
              ('pressed', 'white'),
              ('selected', 'green'),
              ('active', 'red'),
              ('invalid', 'red'),
              ('disabled', 'gray70')  # nuevo estado añadido
          ],
          background=[
              ('disabled', 'white')  # igual que el fondo de frame
          ],
          foreground=[
              ('disabled', 'gray60')  # texto atenuado
          ])

        style.configure("TButton", background="#ffffff", foreground="#000000",
                        font=(font_type, font_size))

        # Configuración para ttk.Notebook (contenedor de pestañas)
        style.configure("TNotebook", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", background="white", foreground="black",
                        padding=[5, 2], font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected", "gray50")],
                  expand=[("selected", [1, 1, 1, 0])])

        # Configurando el color de fondo de la ventana principal
        style.configure("TFrame", background="#ffffff")

        style.map("TCombobox",
          fieldbackground=[
              ("disabled", "#dddddd")
          ],
          foreground=[
              ("disabled", "#888888")
          ],
          background=[
              ("disabled", "#dddddd")
          ])
