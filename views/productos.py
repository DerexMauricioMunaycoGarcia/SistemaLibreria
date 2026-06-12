import customtkinter as ctk
from tkinter import ttk
from Database.conexion import conectar


class VentanaProductos:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Productos")
        self.ventana.geometry("980x640")
        self.ventana.minsize(800, 520)
        self.ventana.configure(fg_color="#110822")
        self.ventana.lift()
        self.ventana.focus_force()
        self.ventana.after(100, self.ventana.lift)

        ctk.set_appearance_mode("dark")
        self._build_ui()
        self.cargar_productos()

    # ── Layout principal ──────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Sidebar izquierdo ─────────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self.ventana, width=260,
                                    fg_color="#1e1040", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        head = ctk.CTkFrame(self.sidebar, fg_color="#2a1a58", corner_radius=0)
        head.pack(fill="x")

        ic = ctk.CTkCanvas(head, width=36, height=36,
                           bg="#2a1a58", highlightthickness=0)
        ic.pack(side="left", padx=(16, 8), pady=14)
        for i, (y, w, c) in enumerate([
            (4,28,"#8b5cf6"),(11,25,"#9d6ff7"),
            (18,25,"#a87ef8"),(25,22,"#b28ef9"),(32,19,"#bd9dfa")
        ]):
            ic.create_rectangle(4, y, 4+w, y+6, fill=c, outline="")
        ic.create_rectangle(2, 2, 7, 36, fill="#7c3aed", outline="")

        tf = ctk.CTkFrame(head, fg_color="transparent")
        tf.pack(side="left", pady=14)
        ctk.CTkLabel(tf, text="Productos",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#ede4ff").pack(anchor="w")
        ctk.CTkLabel(tf, text="Gestión de inventario",
                     font=ctk.CTkFont(size=10),
                     text_color="#5a4880").pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color="#2e1f60").pack(fill="x", pady=(0, 8))

        form = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        form.pack(fill="x", padx=16, pady=4)

        entry_opts = dict(
            height=36, corner_radius=8,
            fg_color="#2a1a58", border_color="#5a3fa0",
            border_width=1, text_color="#ede4ff",
            placeholder_text_color="#5a4880",
            font=ctk.CTkFont(size=12),
        )

        ctk.CTkLabel(form, text="Nombre del producto",
                     font=ctk.CTkFont(size=11),
                     text_color="#8878aa").pack(anchor="w", pady=(8, 2))
        self.txt_nombre = ctk.CTkEntry(form, placeholder_text="Ej: Libro Python",
                                       **entry_opts)
        self.txt_nombre.pack(fill="x")

        ctk.CTkLabel(form, text="Precio (S/.)",
                     font=ctk.CTkFont(size=11),
                     text_color="#8878aa").pack(anchor="w", pady=(10, 2))
        self.txt_precio = ctk.CTkEntry(form, placeholder_text="Ej: 35.00",
                                       **entry_opts)
        self.txt_precio.pack(fill="x")

        ctk.CTkLabel(form, text="Stock (unidades)",
                     font=ctk.CTkFont(size=11),
                     text_color="#8878aa").pack(anchor="w", pady=(10, 2))
        self.txt_stock = ctk.CTkEntry(form, placeholder_text="Ej: 20",
                                      **entry_opts)
        self.txt_stock.pack(fill="x")

        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color="#2e1f60").pack(fill="x", pady=16)

        btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16)

        btn_opts = dict(height=38, corner_radius=9,
                        font=ctk.CTkFont(size=12, weight="bold"))

        ctk.CTkButton(btn_frame, text="＋  Guardar producto",
                      fg_color="#7c3aed", hover_color="#6d28d9",
                      command=self.guardar_producto, **btn_opts).pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="✎  Actualizar producto",
                      fg_color="#0e7490", hover_color="#0c6080",
                      command=self.editar_producto, **btn_opts).pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="✕  Eliminar producto",
                      fg_color="#7f1d1d", hover_color="#6b1818",
                      command=self.eliminar_producto, **btn_opts).pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="↺  Limpiar campos",
                      fg_color="#2a1a58", hover_color="#3a2460",
                      border_width=1, border_color="#5a3fa0",
                      command=self._limpiar_todo, **btn_opts).pack(fill="x", pady=(8, 4))

        self.lbl_sel = ctk.CTkLabel(self.sidebar,
                                     text="Ningún producto seleccionado",
                                     font=ctk.CTkFont(size=10),
                                     text_color="#3d2d66",
                                     wraplength=230)
        self.lbl_sel.pack(side="bottom", padx=16, pady=12)

        # ── Panel derecho ─────────────────────────────────────────────────────
        right = ctk.CTkFrame(self.ventana, fg_color="#110822", corner_radius=0)
        right.pack(side="right", fill="both", expand=True)

        topbar = ctk.CTkFrame(right, fg_color="#1e1040",
                               corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="Inventario de productos",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ede4ff").pack(side="left", padx=20, pady=14)

        leg = ctk.CTkFrame(topbar, fg_color="transparent")
        leg.pack(side="right", padx=16)
        for txt, color in [("● Estable","#4ade80"),("● Crítico","#fbbf24"),
                            ("● Agotado","#f87171"),("● Normal","#8878aa")]:
            ctk.CTkLabel(leg, text=txt, font=ctk.CTkFont(size=10),
                         text_color=color).pack(side="left", padx=6)

        table_wrap = ctk.CTkFrame(right, fg_color="#161030", corner_radius=12)
        table_wrap.pack(fill="both", expand=True, padx=16, pady=14)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                         background="#161030", foreground="#ede4ff",
                         rowheight=32, fieldbackground="#161030",
                         borderwidth=0, font=("Segoe UI", 11))
        style.configure("Custom.Treeview.Heading",
                         background="#2a1a58", foreground="#a899c8",
                         font=("Segoe UI", 11, "bold"),
                         borderwidth=0, relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", "#5a3fa0")],
                  foreground=[("selected", "#ffffff")])
        style.map("Custom.Treeview.Heading",
                  background=[("active", "#3a2860")])

        cols = ("ID", "Nombre", "Precio", "Stock", "Estado")
        self.tabla = ttk.Treeview(table_wrap, columns=cols,
                                   show="headings", style="Custom.Treeview",
                                   selectmode="browse")

        widths = {"ID": 50, "Nombre": 240, "Precio": 100, "Stock": 90, "Estado": 110}
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=widths[col], anchor="center")

        self.tabla.tag_configure("estable", background="#1a3a2a", foreground="#6ee7a0")
        self.tabla.tag_configure("critico", background="#2e2610", foreground="#fbbf24")
        self.tabla.tag_configure("agotado", background="#2e1010", foreground="#f87171")
        self.tabla.tag_configure("normal",  background="#161030", foreground="#ede4ff")

        scroll_y = ttk.Scrollbar(table_wrap, orient="vertical",
                                  command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        self.tabla.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scroll_y.pack(side="right", fill="y", pady=4)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    # ── Popups personalizados ─────────────────────────────────────────────────

    def _confirmar(self, mensaje, callback):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("320x160")
        win.resizable(False, False)
        win.configure(fg_color="#1e1040")
        win.grab_set()
        win.lift()

        self.ventana.update_idletasks()
        rx = self.ventana.winfo_x() + self.ventana.winfo_width()//2 - 160
        ry = self.ventana.winfo_y() + self.ventana.winfo_height()//2 - 80
        win.geometry(f"320x160+{rx}+{ry}")

        ctk.CTkFrame(win, height=4, fg_color="#e05252", corner_radius=0).pack(fill="x")
        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(expand=True, fill="both", padx=24, pady=16)

        ctk.CTkLabel(body, text=mensaje, font=ctk.CTkFont(size=12),
                     text_color="#ede4ff", wraplength=260).pack(pady=(0, 16))

        brow = ctk.CTkFrame(body, fg_color="transparent")
        brow.pack(fill="x")

        ctk.CTkButton(brow, text="Cancelar", width=110, height=32,
                      corner_radius=8, fg_color="#2a1a58", hover_color="#3a2460",
                      border_width=1, border_color="#5a3fa0", text_color="#a899c8",
                      font=ctk.CTkFont(size=12),
                      command=win.destroy).pack(side="left")

        def _ok():
            win.destroy()
            callback()

        ctk.CTkButton(brow, text="Confirmar", width=110, height=32,
                      corner_radius=8, fg_color="#7f1d1d", hover_color="#6b1818",
                      text_color="#f87171", font=ctk.CTkFont(size=12, weight="bold"),
                      command=_ok).pack(side="right")

    def _show_error(self, msg):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("340x160")
        win.resizable(False, False)
        win.configure(fg_color="#1e1040")
        win.grab_set()
        win.lift()

        self.ventana.update_idletasks()
        rx = self.ventana.winfo_x() + self.ventana.winfo_width()//2 - 170
        ry = self.ventana.winfo_y() + self.ventana.winfo_height()//2 - 80
        win.geometry(f"340x160+{rx}+{ry}")

        ctk.CTkFrame(win, height=4, fg_color="#e05252", corner_radius=0).pack(fill="x")
        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(expand=True, fill="both", padx=24, pady=16)

        top = ctk.CTkFrame(body, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))

        badge = ctk.CTkFrame(top, width=34, height=34, corner_radius=17,
                              fg_color="#3d1a1a", border_width=1, border_color="#e05252")
        badge.pack(side="left", padx=(0, 10))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="✕", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#e05252").place(relx=0.5, rely=0.5, anchor="center")

        tf = ctk.CTkFrame(top, fg_color="transparent")
        tf.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(tf, text="Error", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ede4ff", anchor="w").pack(anchor="w")
        ctk.CTkLabel(tf, text=msg, font=ctk.CTkFont(size=11),
                     text_color="#8878aa", anchor="w", wraplength=200).pack(anchor="w")

        ctk.CTkButton(body, text="Entendido", width=110, height=32,
                      corner_radius=8, fg_color="#3d1a1a", hover_color="#4d2020",
                      border_width=1, border_color="#e05252", text_color="#e05252",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=win.destroy).pack(anchor="e")

    # ── Lógica ────────────────────────────────────────────────────────────────

    def cargar_productos(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT IdProducto, Nombre, Precio, Stock FROM Productos")
            for fila in cursor.fetchall():
                id_prod  = str(fila[0])
                nombre   = str(fila[1])
                precio   = str(fila[2])
                stock    = str(fila[3])
                stock_val = int(float(stock))

                if stock_val > 10:
                    estado, tag = "Estable", "estable"
                elif 1 <= stock_val <= 5:
                    estado, tag = "Crítico", "critico"
                elif stock_val == 0:
                    estado, tag = "Agotado", "agotado"
                else:
                    estado, tag = "Normal", "normal"

                self.tabla.insert("", "end",
                                  values=(id_prod, nombre, precio, stock, estado),
                                  tags=(tag,))
            conexion.close()
        except Exception as e:
            self._show_error(f"Error al cargar: {e}")

    def guardar_producto(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Productos (Nombre, Precio, Stock, Estado) VALUES (?, ?, ?, 1)",
                (self.txt_nombre.get(), float(self.txt_precio.get()),
                 int(self.txt_stock.get()))
            )
            conexion.commit()
            conexion.close()
            self._limpiar_todo()
            self.cargar_productos()
        except Exception as e:
            self._show_error(f"Error al guardar: {e}")

    def editar_producto(self):
        if not hasattr(self, "id_producto"):
            self._show_error("Selecciona un producto de la tabla primero.")
            return
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE Productos SET Nombre=?, Precio=?, Stock=? WHERE IdProducto=?",
                (self.txt_nombre.get(), float(self.txt_precio.get()),
                 int(self.txt_stock.get()), self.id_producto)
            )
            conexion.commit()
            conexion.close()
            self.cargar_productos()
        except Exception as e:
            self._show_error(f"Error al actualizar: {e}")

    def eliminar_producto(self):
        if not hasattr(self, "id_producto"):
            self._show_error("Selecciona un producto de la tabla primero.")
            return
        self._confirmar(
            "¿Estas seguro de eliminar el producto seleccionado?",
            self._hacer_eliminar
        )

    def _hacer_eliminar(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Productos WHERE IdProducto=?",
                           (self.id_producto,))
            conexion.commit()
            conexion.close()
            self._limpiar_todo()
            self.cargar_productos()
        except Exception as e:
            self._show_error(f"Error al eliminar: {e}")

    def seleccionar_producto(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        fila = self.tabla.item(seleccion[0])["values"]
        if not fila:
            return
        self.id_producto = fila[0]
        # Limpiar campos SIN borrar id_producto
        self.txt_nombre.delete(0, "end")
        self.txt_precio.delete(0, "end")
        self.txt_stock.delete(0, "end")
        self.txt_nombre.insert(0, str(fila[1]))
        self.txt_precio.insert(0, str(fila[2]))
        self.txt_stock.insert(0, str(fila[3]))
        self.lbl_sel.configure(text=f"Editando: {fila[1]}", text_color="#8b5cf6")

    def limpiar_campos(self):
        """Limpia solo los campos de texto, conserva id_producto."""
        self.txt_nombre.delete(0, "end")
        self.txt_precio.delete(0, "end")
        self.txt_stock.delete(0, "end")

    def _limpiar_todo(self):
        """Limpia campos Y resetea la selección completamente."""
        self.txt_nombre.delete(0, "end")
        self.txt_precio.delete(0, "end")
        self.txt_stock.delete(0, "end")
        self.lbl_sel.configure(text="Ningún producto seleccionado",
                                text_color="#3d2d66")
        if hasattr(self, "id_producto"):
            del self.id_producto
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)