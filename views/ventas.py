import customtkinter as ctk
from tkinter import ttk
from Database.conexion import conectar


class VentanaVentas:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Ventas")
        self.ventana.geometry("1050x660")
        self.ventana.minsize(860, 540)
        self.ventana.configure(fg_color="#0a1a0f")
        self.ventana.lift()
        self.ventana.focus_force()
        self.ventana.after(100, self.ventana.lift)

        ctk.set_appearance_mode("dark")
        self.productos_db = self.cargar_productos_db()
        self._build_ui()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Panel izquierdo: carrito + acciones ───────────────────────────────
        left = ctk.CTkFrame(self.ventana, width=300,
                            fg_color="#0d2218", corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # Header
        head = ctk.CTkFrame(left, fg_color="#0a1c14", corner_radius=0)
        head.pack(fill="x")

        ic = ctk.CTkCanvas(head, width=36, height=36,
                           bg="#0a1c14", highlightthickness=0)
        ic.pack(side="left", padx=(16, 8), pady=14)
        ic.create_rectangle(4, 8, 32, 28, fill="#16a34a", outline="")
        ic.create_oval(8, 24, 16, 32, fill="#16a34a", outline="")
        ic.create_oval(20, 24, 28, 32, fill="#16a34a", outline="")
        ic.create_line(4, 8, 0, 2, fill="#16a34a", width=2)

        tf = ctk.CTkFrame(head, fg_color="transparent")
        tf.pack(side="left", pady=14)
        ctk.CTkLabel(tf, text="Punto de Venta",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#dcfce7").pack(anchor="w")
        ctk.CTkLabel(tf, text="Registra una nueva venta",
                     font=ctk.CTkFont(size=10),
                     text_color="#14532d").pack(anchor="w")

        ctk.CTkFrame(left, height=1, fg_color="#14532d").pack(fill="x", pady=(0, 8))

        # Selección de producto
        form = ctk.CTkFrame(left, fg_color="transparent")
        form.pack(fill="x", padx=16)

        ctk.CTkLabel(form, text="Producto",
                     font=ctk.CTkFont(size=11), text_color="#4ade80").pack(anchor="w", pady=(8, 2))
        self.combo_prod = ctk.CTkComboBox(
            form,
            values=list(self.productos_db.keys()),
            height=36, corner_radius=8,
            fg_color="#0a2a18", border_color="#16a34a",
            border_width=1, text_color="#dcfce7",
            button_color="#16a34a", button_hover_color="#15803d",
            dropdown_fg_color="#0a2a18", dropdown_text_color="#dcfce7",
            dropdown_hover_color="#14532d",
            font=ctk.CTkFont(size=12),
        )
        self.combo_prod.pack(fill="x")

        ctk.CTkLabel(form, text="Cantidad",
                     font=ctk.CTkFont(size=11), text_color="#4ade80").pack(anchor="w", pady=(10, 2))
        self.txt_cant = ctk.CTkEntry(
            form, placeholder_text="Ej: 2",
            height=36, corner_radius=8,
            fg_color="#0a2a18", border_color="#16a34a",
            border_width=1, text_color="#dcfce7",
            placeholder_text_color="#14532d",
            font=ctk.CTkFont(size=12),
        )
        self.txt_cant.pack(fill="x")

        ctk.CTkButton(
            form, text="＋  Agregar al carrito",
            height=38, corner_radius=9,
            fg_color="#16a34a", hover_color="#15803d",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff",
            command=self.agregar_a_carrito,
        ).pack(fill="x", pady=(14, 0))

        ctk.CTkFrame(left, height=1, fg_color="#14532d").pack(fill="x", pady=14)

        # DNI Cliente
        dni_frame = ctk.CTkFrame(left, fg_color="transparent")
        dni_frame.pack(fill="x", padx=16)

        ctk.CTkLabel(dni_frame, text="DNI del cliente",
                     font=ctk.CTkFont(size=11), text_color="#4ade80").pack(anchor="w", pady=(0, 2))
        self.txt_dni = ctk.CTkEntry(
            dni_frame, placeholder_text="Ej: 12345678",
            height=36, corner_radius=8,
            fg_color="#0a2a18", border_color="#16a34a",
            border_width=1, text_color="#dcfce7",
            placeholder_text_color="#14532d",
            font=ctk.CTkFont(size=12),
        )
        self.txt_dni.pack(fill="x")

        ctk.CTkFrame(left, height=1, fg_color="#14532d").pack(fill="x", pady=14)

        # Total
        total_frame = ctk.CTkFrame(left, fg_color="#061a0e", corner_radius=12,
                                    border_width=1, border_color="#14532d")
        total_frame.pack(fill="x", padx=16)

        ctk.CTkLabel(total_frame, text="TOTAL A COBRAR",
                     font=ctk.CTkFont(size=10),
                     text_color="#14532d").pack(pady=(10, 0))
        self.lbl_total = ctk.CTkLabel(
            total_frame, text="S/ 0.00",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4ade80",
        )
        self.lbl_total.pack(pady=(2, 10))

        # Botón finalizar
        ctk.CTkButton(
            left, text="✓  Finalizar Venta",
            height=44, corner_radius=9,
            fg_color="#15803d", hover_color="#166534",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff",
            command=self.finalizar_venta,
        ).pack(fill="x", padx=16, pady=(14, 4))

        ctk.CTkButton(
            left, text="✕  Vaciar carrito",
            height=34, corner_radius=9,
            fg_color="#0a2a18", hover_color="#0d3320",
            border_width=1, border_color="#16a34a",
            font=ctk.CTkFont(size=11),
            text_color="#4ade80",
            command=self.vaciar_carrito,
        ).pack(fill="x", padx=16, pady=4)

        self.lbl_items = ctk.CTkLabel(left, text="0 ítems en el carrito",
                                       font=ctk.CTkFont(size=10),
                                       text_color="#14532d")
        self.lbl_items.pack(side="bottom", pady=12)

        # ── Panel derecho: tabla carrito ──────────────────────────────────────
        right = ctk.CTkFrame(self.ventana, fg_color="#0a1a0f", corner_radius=0)
        right.pack(side="right", fill="both", expand=True)

        topbar = ctk.CTkFrame(right, fg_color="#0d2218",
                               corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="Carrito de venta",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#dcfce7").pack(side="left", padx=20, pady=14)

        ctk.CTkLabel(topbar, text="Selecciona un ítem y pulsa Supr para quitarlo",
                     font=ctk.CTkFont(size=10),
                     text_color="#14532d").pack(side="right", padx=16)

        table_wrap = ctk.CTkFrame(right, fg_color="#061a0e", corner_radius=12)
        table_wrap.pack(fill="both", expand=True, padx=16, pady=14)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Sales.Treeview",
                         background="#061a0e", foreground="#dcfce7",
                         rowheight=34, fieldbackground="#061a0e",
                         borderwidth=0, font=("Segoe UI", 11))
        style.configure("Sales.Treeview.Heading",
                         background="#0a2a18", foreground="#4ade80",
                         font=("Segoe UI", 11, "bold"),
                         borderwidth=0, relief="flat")
        style.map("Sales.Treeview",
                  background=[("selected", "#16a34a")],
                  foreground=[("selected", "#ffffff")])
        style.map("Sales.Treeview.Heading",
                  background=[("active", "#14532d")])

        cols = ("Producto", "Precio Unit.", "Cantidad", "Subtotal")
        self.tabla = ttk.Treeview(table_wrap, columns=cols,
                                   show="headings", style="Sales.Treeview",
                                   selectmode="browse")

        widths = {"Producto": 240, "Precio Unit.": 120, "Cantidad": 100, "Subtotal": 120}
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=widths[col], anchor="center")

        self.tabla.tag_configure("item",  background="#061a0e")
        self.tabla.tag_configure("item2", background="#0a2010")

        scroll_y = ttk.Scrollbar(table_wrap, orient="vertical",
                                  command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        self.tabla.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scroll_y.pack(side="right", fill="y", pady=4)

        self.tabla.bind("<Delete>", self._eliminar_seleccionado)

    # ── Popups ────────────────────────────────────────────────────────────────

    def _show_error(self, msg):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("340x160")
        win.resizable(False, False)
        win.configure(fg_color="#0d2218")
        win.grab_set(); win.lift()
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
                     text_color="#dcfce7", anchor="w").pack(anchor="w")
        ctk.CTkLabel(tf, text=msg, font=ctk.CTkFont(size=11),
                     text_color="#4ade80", anchor="w", wraplength=200).pack(anchor="w")
        ctk.CTkButton(body, text="Entendido", width=110, height=32,
                      corner_radius=8, fg_color="#3d1a1a", hover_color="#4d2020",
                      border_width=1, border_color="#e05252", text_color="#e05252",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=win.destroy).pack(anchor="e")

    def _show_success(self, msg):
        win = ctk.CTkToplevel(self.ventana)
        win.title("")
        win.geometry("320x150")
        win.resizable(False, False)
        win.configure(fg_color="#0d2218")
        win.grab_set(); win.lift()
        self.ventana.update_idletasks()
        rx = self.ventana.winfo_x() + self.ventana.winfo_width()//2 - 160
        ry = self.ventana.winfo_y() + self.ventana.winfo_height()//2 - 75
        win.geometry(f"320x150+{rx}+{ry}")
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
        ctk.CTkLabel(tf, text="¡Venta registrada!",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#dcfce7", anchor="w").pack(anchor="w")
        ctk.CTkLabel(tf, text=msg, font=ctk.CTkFont(size=11),
                     text_color="#4ade80", anchor="w").pack(anchor="w")

        def _cerrar():
            win.destroy()
            self.ventana.destroy()

        ctk.CTkButton(body, text="Aceptar", width=110, height=32,
                      corner_radius=8, fg_color="#14532d", hover_color="#166534",
                      border_width=1, border_color="#22c55e", text_color="#22c55e",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=_cerrar).pack(anchor="e")

    # ── Lógica ────────────────────────────────────────────────────────────────

    def cargar_productos_db(self):
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT IdProducto, Nombre, Precio, Stock FROM Productos")
        data = {row[1].strip(): (row[0], float(row[2]), int(row[3]))
                for row in cursor.fetchall()}
        con.close()
        return data

    def agregar_a_carrito(self):
        n = self.combo_prod.get().strip()
        if n not in self.productos_db:
            self._show_error("Selecciona un producto válido.")
            return
        try:
            cant = int(self.txt_cant.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            self._show_error("Ingresa una cantidad válida (número entero positivo).")
            return

        stock_disp = self.productos_db[n][2]
        if cant > stock_disp:
            self._show_error(f"Stock insuficiente.\nDisponible: {stock_disp} unidades.")
            return

        precio = self.productos_db[n][1]
        idx = len(self.tabla.get_children())
        tag = "item" if idx % 2 == 0 else "item2"
        self.tabla.insert("", "end",
                           values=(n, f"{precio:.2f}", cant, f"{precio*cant:.2f}"),
                           tags=(tag,))
        self.txt_cant.delete(0, "end")
        self.actualizar_total()

    def actualizar_total(self):
        items = self.tabla.get_children()
        total = sum(float(self.tabla.item(c)["values"][3]) for c in items)
        self.lbl_total.configure(text=f"S/ {total:.2f}")
        self.lbl_items.configure(text=f"{len(items)} ítem{'s' if len(items)!=1 else ''} en el carrito")

    def vaciar_carrito(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.actualizar_total()

    def _eliminar_seleccionado(self, event=None):
        sel = self.tabla.selection()
        if sel:
            self.tabla.delete(sel[0])
            self.actualizar_total()

    def finalizar_venta(self):
        if not self.tabla.get_children():
            self._show_error("El carrito está vacío.\nAgrega productos antes de finalizar.")
            return

        con = conectar()
        cursor = con.cursor()
        try:
            dni = self.txt_dni.get().strip()
            cursor.execute("SELECT IdCliente FROM Clientes WHERE DNI = ?", (dni,))
            res = cursor.fetchone()
            if not res:
                self._show_error("No se encontró un cliente con ese DNI.\nVerifica el número ingresado.")
                return
            id_cli = res[0]

            total = sum(float(self.tabla.item(c)["values"][3])
                        for c in self.tabla.get_children())
            cursor.execute("INSERT INTO Ventas (Total, IdCliente) VALUES (?, ?)",
                           (total, id_cli))
            cursor.execute("SELECT @@IDENTITY")
            id_v = int(cursor.fetchone()[0])

            for item in self.tabla.get_children():
                n, p, cant, sub = self.tabla.item(item)["values"]
                id_p = self.productos_db[n.strip()][0]
                cursor.execute(
                    "INSERT INTO DetalleVenta (IdVenta, IdProducto, Cantidad, Precio, Subtotal) VALUES (?,?,?,?,?)",
                    (id_v, id_p, int(cant), float(p), float(sub))
                )
                cursor.execute(
                    "UPDATE Productos SET Stock = Stock - ? WHERE IdProducto = ?",
                    (int(cant), id_p)
                )

            con.commit()
            self._show_success(f"Total cobrado: S/ {total:.2f}")
        except Exception as e:
            con.rollback()
            self._show_error(str(e))
        finally:
            con.close()