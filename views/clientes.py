import customtkinter as ctk
from tkinter import ttk
from Database.conexion import conectar


class VentanaClientes:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Clientes")
        self.ventana.geometry("980x640")
        self.ventana.minsize(800, 520)
        self.ventana.configure(fg_color="#110822")
        self.ventana.lift()
        self.ventana.focus_force()
        self.ventana.after(100, self.ventana.lift)

        ctk.set_appearance_mode("dark")
        self._build_ui()
        self.cargar_clientes()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self.ventana, width=260,
                               fg_color="#0d1f3c", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Header sidebar
        head = ctk.CTkFrame(sidebar, fg_color="#0a1830", corner_radius=0)
        head.pack(fill="x")

        ic = ctk.CTkCanvas(head, width=36, height=36,
                           bg="#0a1830", highlightthickness=0)
        ic.pack(side="left", padx=(16, 8), pady=14)
        # Ícono persona estilizado
        ic.create_oval(10, 2, 26, 18, fill="#0e7490", outline="")
        ic.create_arc(4, 16, 32, 36, start=0, extent=180, fill="#0e7490", outline="")

        tf = ctk.CTkFrame(head, fg_color="transparent")
        tf.pack(side="left", pady=14)
        ctk.CTkLabel(tf, text="Clientes",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#e0f2fe").pack(anchor="w")
        ctk.CTkLabel(tf, text="Gestión de clientes",
                     font=ctk.CTkFont(size=10),
                     text_color="#164e63").pack(anchor="w")

        ctk.CTkFrame(sidebar, height=1, fg_color="#0e3a52").pack(fill="x", pady=(0, 8))

        # Formulario
        form = ctk.CTkFrame(sidebar, fg_color="transparent")
        form.pack(fill="x", padx=16, pady=4)

        entry_opts = dict(
            height=36, corner_radius=8,
            fg_color="#0a2540", border_color="#0e7490",
            border_width=1, text_color="#e0f2fe",
            placeholder_text_color="#164e63",
            font=ctk.CTkFont(size=12),
        )

        campos = [
            ("Nombre completo", "Ej: Juan Pérez", "txt_nombre"),
            ("DNI", "Ej: 12345678", "txt_dni"),
            ("Teléfono", "Ej: 987654321", "txt_telefono"),
        ]
        for label, placeholder, attr in campos:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=11),
                         text_color="#67a8c0").pack(anchor="w", pady=(10, 2))
            entry = ctk.CTkEntry(form, placeholder_text=placeholder, **entry_opts)
            entry.pack(fill="x")
            setattr(self, attr, entry)

        ctk.CTkFrame(sidebar, height=1, fg_color="#0e3a52").pack(fill="x", pady=16)

        # Botones
        btn_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16)

        btn_opts = dict(height=38, corner_radius=9,
                        font=ctk.CTkFont(size=12, weight="bold"))

        ctk.CTkButton(btn_frame, text="＋  Guardar cliente",
                      fg_color="#0e7490", hover_color="#0c6080",
                      command=self.guardar_cliente, **btn_opts).pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="✎  Actualizar cliente",
                      fg_color="#1d4ed8", hover_color="#1e40af",
                      command=self.editar_cliente, **btn_opts).pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="✕  Eliminar cliente",
                      fg_color="#7f1d1d", hover_color="#6b1818",
                      command=self.eliminar_cliente, **btn_opts).pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="↺  Limpiar campos",
                      fg_color="#0a2540", hover_color="#0d2f50",
                      border_width=1, border_color="#0e7490",
                      command=self._limpiar_todo, **btn_opts).pack(fill="x", pady=(8, 4))

        self.lbl_sel = ctk.CTkLabel(sidebar,
                                     text="Ningún cliente seleccionado",
                                     font=ctk.CTkFont(size=10),
                                     text_color="#0e3a52", wraplength=230)
        self.lbl_sel.pack(side="bottom", padx=16, pady=12)

        # ── Panel derecho ─────────────────────────────────────────────────────
        right = ctk.CTkFrame(self.ventana, fg_color="#110822", corner_radius=0)
        right.pack(side="right", fill="both", expand=True)

        topbar = ctk.CTkFrame(right, fg_color="#0d1f3c",
                               corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="Directorio de clientes",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#e0f2fe").pack(side="left", padx=20, pady=14)

        # Contador
        self.lbl_count = ctk.CTkLabel(topbar, text="0 clientes registrados",
                                       font=ctk.CTkFont(size=11),
                                       text_color="#164e63")
        self.lbl_count.pack(side="right", padx=20)

        # Tabla
        table_wrap = ctk.CTkFrame(right, fg_color="#0a1830", corner_radius=12)
        table_wrap.pack(fill="both", expand=True, padx=16, pady=14)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Clients.Treeview",
                         background="#0a1830", foreground="#e0f2fe",
                         rowheight=32, fieldbackground="#0a1830",
                         borderwidth=0, font=("Segoe UI", 11))
        style.configure("Clients.Treeview.Heading",
                         background="#0d2a40", foreground="#67a8c0",
                         font=("Segoe UI", 11, "bold"),
                         borderwidth=0, relief="flat")
        style.map("Clients.Treeview",
                  background=[("selected", "#0e7490")],
                  foreground=[("selected", "#ffffff")])
        style.map("Clients.Treeview.Heading",
                  background=[("active", "#0e3a52")])

        cols = ("ID", "Nombre", "DNI", "Teléfono", "Estado")
        self.tabla = ttk.Treeview(table_wrap, columns=cols,
                                   show="headings", style="Clients.Treeview",
                                   selectmode="browse")

        widths = {"ID": 50, "Nombre": 220, "DNI": 120, "Teléfono": 130, "Estado": 100}
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=widths[col], anchor="center")

        self.tabla.tag_configure("activo",   background="#0a2540", foreground="#e0f2fe")
        self.tabla.tag_configure("inactivo", background="#1a0a0a", foreground="#f87171")
        self.tabla.tag_configure("odd",      background="#0d1f3c")

        scroll_y = ttk.Scrollbar(table_wrap, orient="vertical",
                                  command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        self.tabla.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scroll_y.pack(side="right", fill="y", pady=4)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    # ── Popups ────────────────────────────────────────────────────────────────

    def _show_error(self, msg):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("340x160")
        win.resizable(False, False)
        win.configure(fg_color="#0d1f3c")
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
                     text_color="#e0f2fe", anchor="w").pack(anchor="w")
        ctk.CTkLabel(tf, text=msg, font=ctk.CTkFont(size=11),
                     text_color="#67a8c0", anchor="w", wraplength=200).pack(anchor="w")
        ctk.CTkButton(body, text="Entendido", width=110, height=32,
                      corner_radius=8, fg_color="#3d1a1a", hover_color="#4d2020",
                      border_width=1, border_color="#e05252", text_color="#e05252",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=win.destroy).pack(anchor="e")

    def _show_success(self, msg):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("320x140")
        win.resizable(False, False)
        win.configure(fg_color="#0d1f3c")
        win.grab_set()
        win.lift()
        self.ventana.update_idletasks()
        rx = self.ventana.winfo_x() + self.ventana.winfo_width()//2 - 160
        ry = self.ventana.winfo_y() + self.ventana.winfo_height()//2 - 70
        win.geometry(f"320x140+{rx}+{ry}")

        ctk.CTkFrame(win, height=4, fg_color="#22c55e", corner_radius=0).pack(fill="x")
        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(expand=True, fill="both", padx=24, pady=16)
        top = ctk.CTkFrame(body, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        badge = ctk.CTkFrame(top, width=34, height=34, corner_radius=17,
                              fg_color="#14532d", border_width=1, border_color="#22c55e")
        badge.pack(side="left", padx=(0, 10))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="✓", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#22c55e").place(relx=0.5, rely=0.5, anchor="center")
        tf = ctk.CTkFrame(top, fg_color="transparent")
        tf.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(tf, text="Operación exitosa",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#e0f2fe", anchor="w").pack(anchor="w")
        ctk.CTkLabel(tf, text=msg, font=ctk.CTkFont(size=11),
                     text_color="#67a8c0", anchor="w").pack(anchor="w")
        ctk.CTkButton(body, text="Aceptar", width=110, height=32,
                      corner_radius=8, fg_color="#14532d", hover_color="#166534",
                      border_width=1, border_color="#22c55e", text_color="#22c55e",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=win.destroy).pack(anchor="e")

    def _confirmar(self, mensaje, callback):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("320x160")
        win.resizable(False, False)
        win.configure(fg_color="#0d1f3c")
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
                     text_color="#e0f2fe", wraplength=260).pack(pady=(0, 16))
        brow = ctk.CTkFrame(body, fg_color="transparent")
        brow.pack(fill="x")
        ctk.CTkButton(brow, text="Cancelar", width=110, height=32,
                      corner_radius=8, fg_color="#0a2540", hover_color="#0d2f50",
                      border_width=1, border_color="#0e7490", text_color="#67a8c0",
                      font=ctk.CTkFont(size=12), command=win.destroy).pack(side="left")

        def _ok():
            win.destroy()
            callback()

        ctk.CTkButton(brow, text="Confirmar", width=110, height=32,
                      corner_radius=8, fg_color="#7f1d1d", hover_color="#6b1818",
                      text_color="#f87171", font=ctk.CTkFont(size=12, weight="bold"),
                      command=_ok).pack(side="right")

    # ── Lógica ────────────────────────────────────────────────────────────────

    def cargar_clientes(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT IdCliente, Nombre, DNI, Telefono, Estado FROM Clientes")
            filas = cursor.fetchall()
            conexion.close()
            for idx, fila in enumerate(filas):
                estado_val = str(fila[4])
                estado_txt = "Activo" if estado_val in ("1", "True", "true") else "Inactivo"
                tag = "activo" if estado_txt == "Activo" else "inactivo"
                if idx % 2 == 1 and tag == "activo":
                    tag = "odd"
                self.tabla.insert("", "end",
                                  values=(str(fila[0]), str(fila[1]),
                                          str(fila[2]), str(fila[3]), estado_txt),
                                  tags=(tag,))
            self.lbl_count.configure(text=f"{len(filas)} clientes registrados")
        except Exception as e:
            self._show_error(f"No se pudo cargar: {e}")

    def guardar_cliente(self):
        if not self.txt_nombre.get().strip():
            self._show_error("El nombre es obligatorio.")
            return
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO Clientes (Nombre, DNI, Telefono, Estado) VALUES (?, ?, ?, 1)",
                (self.txt_nombre.get(), self.txt_dni.get(), self.txt_telefono.get())
            )
            conexion.commit()
            conexion.close()
            self._limpiar_todo()
            self.cargar_clientes()
            self._show_success("Cliente guardado correctamente.")
        except Exception as e:
            self._show_error(f"Error al guardar: {e}")

    def editar_cliente(self):
        if not hasattr(self, "id_cliente"):
            self._show_error("Selecciona un cliente de la tabla primero.")
            return
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE Clientes SET Nombre=?, DNI=?, Telefono=? WHERE IdCliente=?",
                (self.txt_nombre.get(), self.txt_dni.get(),
                 self.txt_telefono.get(), self.id_cliente)
            )
            conexion.commit()
            conexion.close()
            self.cargar_clientes()
            self._show_success("Cliente actualizado correctamente.")
        except Exception as e:
            self._show_error(f"Error al editar: {e}")

    def eliminar_cliente(self):
        if not hasattr(self, "id_cliente"):
            self._show_error("Selecciona un cliente de la tabla primero.")
            return
        self._confirmar(
            "¿Eliminar este cliente?\nEsta acción no se puede deshacer.",
            self._hacer_eliminar
        )

    def _hacer_eliminar(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Clientes WHERE IdCliente=?", (self.id_cliente,))
            conexion.commit()
            conexion.close()
            self._limpiar_todo()
            self.cargar_clientes()
        except Exception as e:
            self._show_error(f"Error al eliminar: {e}")

    def seleccionar_cliente(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        fila = self.tabla.item(seleccion[0])["values"]
        if not fila:
            return
        self.id_cliente = fila[0]
        self.txt_nombre.delete(0, "end")
        self.txt_dni.delete(0, "end")
        self.txt_telefono.delete(0, "end")
        self.txt_nombre.insert(0, str(fila[1]))
        self.txt_dni.insert(0, str(fila[2]))
        self.txt_telefono.insert(0, str(fila[3]))
        self.lbl_sel.configure(text=f"Editando: {fila[1]}", text_color="#0e7490")

    def limpiar_campos(self):
        self.txt_nombre.delete(0, "end")
        self.txt_dni.delete(0, "end")
        self.txt_telefono.delete(0, "end")

    def _limpiar_todo(self):
        self.txt_nombre.delete(0, "end")
        self.txt_dni.delete(0, "end")
        self.txt_telefono.delete(0, "end")
        self.lbl_sel.configure(text="Ningún cliente seleccionado", text_color="#0e3a52")
        if hasattr(self, "id_cliente"):
            del self.id_cliente
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)