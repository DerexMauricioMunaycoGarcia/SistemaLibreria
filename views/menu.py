import customtkinter as ctk
import math
from views.productos import VentanaProductos
from views.clientes import VentanaClientes
from views.ventas import VentanaVentas
from views.reportes import VentanaReportes


class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Librería")
        self.root.geometry("900x580")
        self.root.minsize(600, 420)
        self.root.configure(bg="#110822")

        ctk.set_appearance_mode("dark")

        # Canvas fondo animado
        self.canvas = ctk.CTkCanvas(root, bg="#110822", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._floating = []
        self._init_floating()
        self._animate(0)

        # Contenedor principal centrado
        self.main = ctk.CTkFrame(root, fg_color="transparent")
        self.main.place(relx=0.5, rely=0.5, anchor="center")

        self._build_ui()
        root.bind("<Configure>", lambda e: None)

    def _build_ui(self):
        # ── Encabezado ────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.pack(pady=(0, 32))

        # Ícono libro
        ic = ctk.CTkCanvas(header, width=52, height=52,
                            bg="#110822", highlightthickness=0)
        ic.pack(side="left", padx=(0, 14))
        for i, (y, w, c) in enumerate([
            (6, 40, "#8b5cf6"), (16, 36, "#9d6ff7"),
            (26, 36, "#a87ef8"), (36, 32, "#b28ef9"), (46, 28, "#bd9dfa")
        ]):
            ic.create_rectangle(6, y, 6+w, y+7, fill=c, outline="")
        ic.create_rectangle(4, 4, 10, 52, fill="#7c3aed", outline="")

        title_f = ctk.CTkFrame(header, fg_color="transparent")
        title_f.pack(side="left")
        ctk.CTkLabel(title_f, text="Sistema Librería",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color="#ede4ff").pack(anchor="w")
        ctk.CTkLabel(title_f, text="Panel principal de gestión",
                     font=ctk.CTkFont(size=12),
                     text_color="#5a4880").pack(anchor="w")

        # Separador
        ctk.CTkFrame(self.main, height=1, width=560,
                     fg_color="#2a1a58").pack(pady=(0, 28))

        # ── Grid de tarjetas ──────────────────────────────────────────────────
        grid = ctk.CTkFrame(self.main, fg_color="transparent")
        grid.pack()

        CARDS = [
            ("📚", "Productos",  "Gestiona el inventario\nde libros y artículos", self.abrir_productos, "#7c3aed", "#5b21b6"),
            ("👤", "Clientes",   "Administra la base\nde clientes registrados",  self.abrir_clientes,  "#0e7490", "#0c6080"),
            ("💰", "Ventas",     "Registra y consulta\nlas ventas realizadas",    self.abrir_ventas,    "#065f46", "#054d38"),
            ("📊", "Reportes",   "Visualiza estadísticas\ny genera informes",     self.abrir_reportes,  "#92400e", "#78350f"),
        ]

        for i, (emoji, titulo, desc, cmd, color, hover) in enumerate(CARDS):
            row, col = divmod(i, 2)
            card = ctk.CTkFrame(grid,
                                width=250, height=130,
                                fg_color="#1e1040",
                                corner_radius=16,
                                border_width=1,
                                border_color="#2e1f60")
            card.grid(row=row, column=col, padx=12, pady=12)
            card.pack_propagate(False)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(expand=True, fill="both", padx=18, pady=14)

            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")

            # Badge emoji
            badge = ctk.CTkFrame(top, width=38, height=38,
                                  corner_radius=10,
                                  fg_color=color)
            badge.pack(side="left", padx=(0, 10))
            badge.pack_propagate(False)
            ctk.CTkLabel(badge, text=emoji,
                         font=ctk.CTkFont(size=18),
                         text_color="#ffffff").place(relx=0.5, rely=0.5, anchor="center")

            txt = ctk.CTkFrame(top, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(txt, text=titulo,
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#ede4ff", anchor="w").pack(anchor="w")
            ctk.CTkLabel(txt, text=desc,
                         font=ctk.CTkFont(size=11),
                         text_color="#5a4880", anchor="w",
                         justify="left").pack(anchor="w")

            ctk.CTkButton(inner,
                          text="Abrir  →",
                          height=30, corner_radius=8,
                          fg_color=color, hover_color=hover,
                          font=ctk.CTkFont(size=12, weight="bold"),
                          text_color="#ffffff",
                          command=cmd).pack(fill="x", pady=(10, 0))

        # ── Pie ───────────────────────────────────────────────────────────────
        ctk.CTkFrame(self.main, height=1, width=560,
                     fg_color="#2a1a58").pack(pady=(24, 10))
        ctk.CTkLabel(self.main, text="Sistema de gestión · Librería  —  v1.0",
                     font=ctk.CTkFont(size=10),
                     text_color="#2e1f60").pack()

    # ── Flotantes ─────────────────────────────────────────────────────────────

    EMOJIS = ["📚", "✏️", "📖", "🖊️", "📕", "📗", "📘", "📝"]
    POSITIONS = [
        (0.04, 0.08), (0.88, 0.06), (0.03, 0.68),
        (0.90, 0.72), (0.92, 0.32), (0.46, 0.90),
        (0.12, 0.85), (0.76, 0.18),
    ]

    def _init_floating(self):
        for i, (emoji, (rx, ry)) in enumerate(zip(self.EMOJIS, self.POSITIONS)):
            self._floating.append({
                "emoji": emoji, "rx": rx, "ry": ry,
                "phase": i * (2 * math.pi / len(self.EMOJIS)),
            })

    def _animate(self, tick):
        w = self.canvas.winfo_width() or 900
        h = self.canvas.winfo_height() or 580
        self.canvas.delete("float")
        for el in self._floating:
            offset = 14 * math.sin(tick * 0.035 + el["phase"])
            self.canvas.create_text(
                el["rx"] * w, el["ry"] * h + offset,
                text=el["emoji"],
                font=("Segoe UI Emoji", 28),
                fill="#5a3fa0", stipple="gray50", tags="float",
            )
        self.root.after(40, self._animate, tick + 1)

    # ── Acciones (sin cambios) ─────────────────────────────────────────────────

    def abrir_productos(self):
        VentanaProductos()

    def abrir_clientes(self):
        VentanaClientes()

    def abrir_ventas(self):
        VentanaVentas()

    def abrir_reportes(self):
        VentanaReportes()