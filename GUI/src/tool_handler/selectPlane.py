import tkinter as tk

class SelectPlane:
    def __init__(self, canvas, orientation='horizontal', entry1=None, entry2=None, image_dims=(512, 512), enable_var=None):
        self.canvas = canvas
        self.orientation = orientation
        self.entry1 = entry1
        self.entry2 = entry2
        self.image_dims = image_dims
        self.enable_var = enable_var

        self.canvas_width = self.canvas.winfo_reqwidth()
        self.canvas_height = self.canvas.winfo_reqheight()

        self.canvas_offsetX = self.canvas.image_offset[0]
        self.canvas_offsetY = self.canvas.image_offset[1]

        self.image_w = self.canvas.image_dim[0]
        self.image_h = self.canvas.image_dim[1]

        self.orig_image_w = self.canvas.orig_image_dim[0]
        self.orig_image_h = self.canvas.orig_image_dim[1]

        #print('Offset: ', self.canvas.image_offset)
        #print('image dims: ', self.canvas.image_dim)
        #print('Orig image dims: ', self.canvas.orig_image_dim)
        #print('Values: ', (int(((0 - self.canvas_offsetY )/ self.image_h) * self.orig_image_h),int(((self.canvas_offsetX + self.image_w - self.canvas_offsetY )/ self.image_h) * self.orig_image_h)))
        
        self.line1 = None
        self.line2 = None

        # Proporciones relativas para posicionar las líneas
        self.proportion1 = 1/3
        self.proportion2 = 2/3

        self.initialize_lines()
        self.update_entries()

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_move)
        self.canvas.bind("<Motion>", self.update_cursor)

        self.active_line = None

    def initialize_lines(self):
        if self.line1:
            self.canvas.delete(self.line1)
        if self.line2:
            self.canvas.delete(self.line2)

        if self.orientation == 'horizontal':
            self.y1 = int(self.canvas_offsetY + self.image_h * self.proportion1)
            self.y2 = int(self.canvas_offsetY + self.image_h * self.proportion2)
            self.line1 = self.canvas.create_line(self.canvas_offsetX, self.y1, self.canvas_offsetX + self.image_w, self.y1, fill="blue", width=1.5)
            self.line2 = self.canvas.create_line(self.canvas_offsetX, self.y2, self.canvas_offsetX + self.image_w, self.y2, fill="red", width=1.5)
        else:
            self.x1 = int(self.canvas_offsetX + self.image_w * self.proportion1)
            self.x2 = int(self.canvas_offsetX + self.image_w * self.proportion2)
            self.line1 = self.canvas.create_line(self.x1, self.canvas_offsetY, self.x1, self.canvas_offsetY + self.image_h, fill="blue", width=1.5)
            self.line2 = self.canvas.create_line(self.x2, self.canvas_offsetY, self.x2, self.canvas_offsetY + self.image_h, fill="red", width=1.5)
        
    def on_canvas_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.initialize_lines()

    def start_move(self, event):

        if self.orientation == 'horizontal':
            distance_to_line1 = abs(event.y - self.y1)
            distance_to_line2 = abs(event.y - self.y2)
            if distance_to_line1 < 10:
                self.active_line = self.line1
            elif distance_to_line2 < 10:
                self.active_line = self.line2
        else:
            distance_to_line1 = abs(event.x - self.x1)
            distance_to_line2 = abs(event.x - self.x2)
            if distance_to_line1 < 10:
                self.active_line = self.line1
            elif distance_to_line2 < 10:
                self.active_line = self.line2

    def move_line(self, event):
        if not self.active_line:
            return
             
        if self.orientation == 'horizontal':
            y_min =  self.canvas_offsetY
            y_max = self.canvas_offsetY + self.image_h 
            new_y = min(max(event.y, y_min), y_max)
            

            if self.active_line == self.line1 and new_y <= self.y2 - 2: 
                self.canvas.coords(self.line1, self.canvas_offsetX, new_y, self.canvas_offsetX + self.image_w, new_y)
                self.y1 = new_y
            elif self.active_line == self.line2 and new_y >= self.y1 + 2: 
                self.canvas.coords(self.line2, self.canvas_offsetX, new_y, self.canvas_offsetX + self.image_w, new_y)
                self.y2 = new_y
        else:
            x_min =  self.canvas_offsetX
            x_max = self.canvas_offsetX + self.image_w
            new_x = min(max(event.x, x_min), x_max)

            if self.active_line == self.line1 and new_x <= self.x2 - 2: 
                self.canvas.coords(self.line1, new_x, self.canvas_offsetY, new_x, self.canvas_offsetY + self.image_h)
                self.x1 = new_x
            elif self.active_line == self.line2 and new_x >= self.x1 + 2: 
                self.canvas.coords(self.line2, new_x, self.canvas_offsetY, new_x, self.canvas_offsetY + self.image_h)
                self.x2 = new_x
        self.update_entries()

    def end_move(self, event):
        self.active_line = None
        self.update_entries()

    def update_entries(self):
        if self.enable_var and self.enable_var.get() != "Yes":
            return  # ← solo actualiza si está activo
    
        if self.orientation == 'horizontal':
            row1 = int(((self.y1 - self.canvas_offsetY )/ self.image_h) * self.orig_image_h)
            row2 = int(((self.y2 - self.canvas_offsetY )/ self.image_h) * self.orig_image_h)
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, str(row1))
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, str(row2))
        else:
            col1 = int(((self.x1 - self.canvas_offsetX )/ self.image_w) * self.orig_image_w)
            col2 = int(((self.x2 - self.canvas_offsetX )/ self.image_w) * self.orig_image_w)
            #col1 = int(self.x1)
            #col2 = int(self.x2)
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, str(col1))
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, str(col2))

    def redraw_lines(self):
        # Redibuja la imagen actual antes de las líneas
        if hasattr(self.canvas, "_photo") and hasattr(self.canvas, "_img_id"):
            # Volvemos a aplicar la imagen actual (previene líneas perdidas)
            self.canvas.itemconfig(self.canvas._img_id, image=self.canvas._photo)

        # Elimina líneas anteriores si existen
        if self.line1:
            self.canvas.delete(self.line1)
        if self.line2:
            self.canvas.delete(self.line2)

        # Redibuja líneas según orientación
        if self.orientation == 'horizontal':

            self.line1 = self.canvas.create_line(self.canvas_offsetX, self.y1, self.canvas_offsetX + self.image_w, self.y1, fill="blue", width=1.5)
            self.line2 = self.canvas.create_line(self.canvas_offsetX, self.y2, self.canvas_offsetX + self.image_w, self.y2, fill="red", width=1.5)
        else:
            self.line1 = self.canvas.create_line(self.x1, self.canvas_offsetY, self.x1, self.canvas_offsetY + self.image_h, fill="blue", width=1.5)
            self.line2 = self.canvas.create_line(self.x2, self.canvas_offsetY, self.x2, self.canvas_offsetY + self.image_h, fill="red", width=1.5)

        self.update_entries()

    def displace_from_entry(self, entry1_val, entry2_val, origin=None):

        if self.enable_var and self.enable_var.get() != "Yes":
            return
        
        def resaltar_corregido(entry_widget, valor_corregido):
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, str(valor_corregido))
            entry_widget.config(foreground='red')
            entry_widget.after(2000, lambda: entry_widget.config(foreground='black'))

        if self.orientation == 'horizontal':
            px1 = int(entry1_val / self.image_dims[1] * self.canvas_height)
            px2 = int(entry2_val / self.image_dims[1] * self.canvas_height)

            if px1 >= px2:
                if origin == self.entry1:
                    px1 = px2 - 1
                    val_corr = int(px1 / self.canvas_height * self.image_dims[1])
                    resaltar_corregido(self.entry1, val_corr)
                elif origin == self.entry2:
                    px2 = px1 + 1
                    val_corr = int(px2 / self.canvas_height * self.image_dims[1])
                    resaltar_corregido(self.entry2, val_corr)

            self.canvas.coords(self.line1, 0, px1, self.canvas_width, px1)
            self.canvas.coords(self.line2, 0, px2, self.canvas_width, px2)
            self.y1, self.y2 = px1, px2

        else:  # vertical
            px1 = int(entry1_val / self.image_dims[0] * self.canvas_width)
            px2 = int(entry2_val / self.image_dims[0] * self.canvas_width)

            if px1 >= px2:
                if origin == self.entry1:
                    px1 = px2 - 1
                    val_corr = int(px1 / self.canvas_width * self.image_dims[0])
                    resaltar_corregido(self.entry1, val_corr)
                elif origin == self.entry2:
                    px2 = px1 + 1
                    val_corr = int(px2 / self.canvas_width * self.image_dims[0])
                    resaltar_corregido(self.entry2, val_corr)

            self.canvas.coords(self.line1, px1, 0, px1, self.canvas_height)
            self.canvas.coords(self.line2, px2, 0, px2, self.canvas_height)
            self.x1, self.x2 = px1, px2

    def update_cursor(self, event):
        cursor_changed = False
        tolerance = 5  # píxeles de sensibilidad

        if self.orientation == 'horizontal':
            if abs(event.y - self.y1) < tolerance or abs(event.y - self.y2) < tolerance:
                self.canvas.config(cursor="sb_v_double_arrow")
                cursor_changed = True
        else:
            if abs(event.x - self.x1) < tolerance or abs(event.x - self.x2) < tolerance:
                self.canvas.config(cursor="sb_h_double_arrow")
                cursor_changed = True

        if not cursor_changed:
            self.canvas.config(cursor="arrow")

    def eliminar(self):
        if hasattr(self, "line1") and self.line1:
            self.canvas.delete(self.line1)
        if hasattr(self, "line2") and self.line2:
            self.canvas.delete(self.line2)

    def update_lines_from_entry(self, origin=None):
        try:
            val1 = int(self.entry1.get())
            val2 = int(self.entry2.get())
        except ValueError:
            return

        self.displace_from_entry(val1, val2, origin=origin)
    
    '''def actualizar_lineas_desde_entry(self):
        try:
            val1 = int(self.entry1.get())
            val2 = int(self.entry2.get())
        except ValueError:
            return  # Si no hay números válidos, salimos

        if self.orientation == "vertical":
            self.canvas.coords(self.line1, val1, 0, val1, self.canvas.winfo_height())
            self.canvas.coords(self.line2, val2, 0, val2, self.canvas.winfo_height())
        else:
            self.canvas.coords(self.line1, 0, val1, self.canvas.winfo_width(), val1)
            self.canvas.coords(self.line2, 0, val2, self.canvas.winfo_width(), val2)
'''

