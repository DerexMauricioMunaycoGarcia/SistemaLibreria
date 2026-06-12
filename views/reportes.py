import customtkinter as ctk
from tkinter import ttk
from Database.conexion import conectar


class VentanaReportes:
    def __init__(self):
        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Reportes")
        self.ventana.geometry("1050x640")
        self.ventana.minsize(860, 500)
        self.ventana.configure(fg_color="#1a0f00")
        self.ventana.lift()
        self.ventana.focus_force()
        self.ventana.after(100, self.ventana.lift)

        ctk.set_appearance_mode("dark")
        self._build_ui()
        self.cargar_datos()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self.ventana, width=240,
                               fg_color="#1f1200", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Header
        head = ctk.CTkFrame(sidebar, fg_color="#180e00", corner_radius=0)
        head.pack(fill="x")

        ic = ctk.CTkCanvas(head, width=36, height=36,
                           bg="#180e00", highlightthickness=0)
        ic.pack(side="left", padx=(16, 8), pady=14)
        # Ícono gráfico de barras
        for x, h, c in [(4,20,"#f59e0b"),(13,28,"#fbbf24"),(22,14,"#f59e0b"),(31,32,"#fbbf24")]:
            ic.create_rectangle(x, 36-h, x+7, 34, fill=c, outline="")

        tf = ctk.CTkFrame(head, fg_color="transparent")
        tf.pack(side="left", pady=14)
        ctk.CTkLabel(tf, text="Reportes",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#fef3c7").pack(anchor="w")
        ctk.CTkLabel(tf, text="Historial de ventas",
                     font=ctk.CTkFont(size=10),
                     text_color="#78350f").pack(anchor="w")

        ctk.CTkFrame(sidebar, height=1, fg_color="#78350f").pack(fill="x", pady=(0, 16))

        # Tarjetas de resumen
        self.card_ventas  = self._make_card(sidebar, "Total ventas",   "0",      "#f59e0b")
        self.card_ingresos = self._make_card(sidebar, "Ingresos",      "S/ 0.00", "#fbbf24")
        self.card_productos = self._make_card(sidebar, "Ítems vendidos", "0",    "#f59e0b")

        ctk.CTkFrame(sidebar, height=1, fg_color="#78350f").pack(fill="x", pady=16)

        # Botón actualizar
        ctk.CTkButton(
            sidebar, text="↻  Actualizar reporte",
            height=38, corner_radius=9,
            fg_color="#92400e", hover_color="#78350f",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#fef3c7",
            command=self.cargar_datos,
        ).pack(fill="x", padx=16, pady=4)

        self.lbl_count = ctk.CTkLabel(sidebar,
                                       text="Cargando...",
                                       font=ctk.CTkFont(size=10),
                                       text_color="#78350f")
        self.lbl_count.pack(side="bottom", pady=12)

        # ── Panel derecho ─────────────────────────────────────────────────────
        right = ctk.CTkFrame(self.ventana, fg_color="#1a0f00", corner_radius=0)
        right.pack(side="right", fill="both", expand=True)

        topbar = ctk.CTkFrame(right, fg_color="#1f1200",
                               corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="Historial completo de ventas",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#fef3c7").pack(side="left", padx=20, pady=14)

        ctk.CTkLabel(topbar, text="Ordenado por fecha más reciente",
                     font=ctk.CTkFont(size=10),
                     text_color="#78350f").pack(side="right", padx=16)

        # Tabla
        table_wrap = ctk.CTkFrame(right, fg_color="#120b00", corner_radius=12)
        table_wrap.pack(fill="both", expand=True, padx=16, pady=14)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Reports.Treeview",
                         background="#120b00", foreground="#fef3c7",
                         rowheight=32, fieldbackground="#120b00",
                         borderwidth=0, font=("Segoe UI", 11))
        style.configure("Reports.Treeview.Heading",
                         background="#1f1200", foreground="#f59e0b",
                         font=("Segoe UI", 11, "bold"),
                         borderwidth=0, relief="flat")
        style.map("Reports.Treeview",
                  background=[("selected", "#92400e")],
                  foreground=[("selected", "#ffffff")])
        style.map("Reports.Treeview.Heading",
                  background=[("active", "#2d1a00")])

        cols = ("Fecha", "Cliente", "DNI", "Producto", "Cant", "Subtotal")
        self.tabla = ttk.Treeview(table_wrap, columns=cols,
                                   show="headings", style="Reports.Treeview",
                                   selectmode="browse")

        widths = {"Fecha": 140, "Cliente": 160, "DNI": 100,
                  "Producto": 180, "Cant": 70, "Subtotal": 100}
        for col in cols:
            self.tabla.heading(col, text=col,
                               command=lambda c=col: self._sort_by(c))
            self.tabla.column(col, width=widths[col], anchor="center")

        self.tabla.tag_configure("row1", background="#120b00")
        self.tabla.tag_configure("row2", background="#1a1000")

        scroll_y = ttk.Scrollbar(table_wrap, orient="vertical",
                                  command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(table_wrap, orient="horizontal",
                                  command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set,
                              xscrollcommand=scroll_x.set)
        scroll_y.pack(side="right", fill="y", pady=4)
        scroll_x.pack(side="bottom", fill="x", padx=4)
        self.tabla.pack(side="left", fill="both", expand=True, padx=4, pady=4)

    def _make_card(self, parent, label, value, color):
        card = ctk.CTkFrame(parent, fg_color="#120b00", corner_radius=10,
                             border_width=1, border_color="#78350f")
        card.pack(fill="x", padx=16, pady=4)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=10),
                     text_color="#92400e").pack(anchor="w")
        lbl = ctk.CTkLabel(row, text=value,
                           font=ctk.CTkFont(size=18, weight="bold"),
                           text_color=color)
        lbl.pack(anchor="w")
        return lbl

    def _sort_by(self, col):
        """Ordenar tabla al hacer clic en encabezado."""
        items = [(self.tabla.set(k, col), k) for k in self.tabla.get_children()]
        items.sort(reverse=getattr(self, f"_sort_{col}_rev", False))
        for i, (_, k) in enumerate(items):
            self.tabla.move(k, "", i)
            tag = "row1" if i % 2 == 0 else "row2"
            self.tabla.item(k, tags=(tag,))
        setattr(self, f"_sort_{col}_rev",
                not getattr(self, f"_sort_{col}_rev", False))

    # ── Lógica ────────────────────────────────────────────────────────────────

    def cargar_datos(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        query = """
        SELECT V.Fecha, C.Nombre, C.DNI, P.Nombre, DV.Cantidad, DV.Subtotal
        FROM Ventas V
        JOIN Clientes C ON V.IdCliente = C.IdCliente
        JOIN DetalleVenta DV ON V.IdVenta = DV.IdVenta
        JOIN Productos P ON DV.IdProducto = P.IdProducto
        ORDER BY V.Fecha DESC
        """
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            con.close()

            total_ingresos = 0.0
            total_items = 0

            for idx, row in enumerate(filas):
                fecha = row[0].strftime("%d/%m/%Y %H:%M")
                subtotal = float(row[5])
                total_ingresos += subtotal
                total_items += int(row[4])
                tag = "row1" if idx % 2 == 0 else "row2"
                self.tabla.insert("", "end",
                                  values=(fecha, row[1], row[2],
                                          row[3], row[4], f"S/ {subtotal:.2f}"),
                                  tags=(tag,))

            n = len(filas)
            self.card_ventas.configure(text=str(n))
            self.card_ingresos.configure(text=f"S/ {total_ingresos:.2f}")
            self.card_productos.configure(text=str(total_items))
            self.lbl_count.configure(
                text=f"{n} registro{'s' if n != 1 else ''} encontrado{'s' if n != 1 else ''}"
            )

        except Exception as e:
            self.lbl_count.configure(text=f"Error: {e}", text_color="#e05252")