import customtkinter as ctk
import math


class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("750x520")
        self.root.minsize(520, 400)
        self.root.configure(bg="#110822")

        ctk.set_appearance_mode("dark")

        # Canvas fondo
        self.canvas = ctk.CTkCanvas(root, bg="#110822", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._floating = []
        self._init_floating_elements()
        self._animate_floating()

        # Tarjeta central
        self.frame = ctk.CTkFrame(
            root,
            fg_color="#1e1040",
            corner_radius=22,
            border_width=1,
            border_color="#5a3fa0",
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self._build_form()
        root.bind("<Configure>", self._on_resize)

    # ── Formulario ────────────────────────────────────────────────────────────

    def _build_form(self):
        inner = ctk.CTkFrame(self.frame, fg_color="transparent")
        inner.pack(padx=56, pady=44)

        # Ícono usando canvas SVG-like con CTkCanvas
        icon_canvas = ctk.CTkCanvas(inner, width=64, height=64,
                                     bg="#1e1040", highlightthickness=0)
        icon_canvas.pack(pady=(0, 6))
        # Dibujar ícono de libro estilizado
        for i, (y, w) in enumerate([(14,44),(24,40),(34,40),(44,36),(54,32)]):
            shade = ["#8b5cf6","#9d6ff7","#a87ef8","#b28ef9","#bd9dfa"][i]
            icon_canvas.create_rectangle(10, y, 10+w, y+7,
                                          fill=shade, outline="", width=0)
        icon_canvas.create_rectangle(8, 12, 13, 58, fill="#7c3aed", outline="")

        ctk.CTkLabel(
            inner,
            text="Sistema Librería",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ede4ff",
        ).pack(pady=(2, 2))

        ctk.CTkLabel(
            inner,
            text="Ingresa tus credenciales para continuar",
            font=ctk.CTkFont(size=12),
            text_color="#8878aa",
        ).pack(pady=(0, 22))

        # Separador
        sep = ctk.CTkFrame(inner, height=1, width=260, fg_color="#3a2860")
        sep.pack(pady=(0, 20))

        entry_opts = dict(
            width=270,
            height=42,
            corner_radius=11,
            fg_color="#2a1a58",
            border_color="#5a3fa0",
            border_width=1,
            text_color="#ede4ff",
            placeholder_text_color="#6655aa",
            font=ctk.CTkFont(size=13),
        )

        # Campo usuario con label
        ctk.CTkLabel(inner, text="Usuario", font=ctk.CTkFont(size=11),
                     text_color="#8878aa").pack(anchor="w")
        self.txt_user = ctk.CTkEntry(inner, placeholder_text="Ingresa tu usuario",
                                      **entry_opts)
        self.txt_user.pack(pady=(3, 14))

        ctk.CTkLabel(inner, text="Contraseña", font=ctk.CTkFont(size=11),
                     text_color="#8878aa").pack(anchor="w")
        self.txt_pass = ctk.CTkEntry(inner, placeholder_text="Ingresa tu contraseña",
                                      show="*", **entry_opts)
        self.txt_pass.pack(pady=(3, 22))

        ctk.CTkButton(
            inner,
            text="  Ingresar  →",
            width=270,
            height=44,
            corner_radius=11,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff",
            command=self.validar,
        ).pack()

        ctk.CTkLabel(
            inner,
            text="Sistema de gestión · Librería",
            font=ctk.CTkFont(size=10),
            text_color="#3d2d66",
        ).pack(pady=(16, 0))

    # ── Ventana de error personalizada ────────────────────────────────────────

    def _show_error(self, mensaje):
        win = ctk.CTkToplevel(self.root)
        win.title("")
        win.geometry("340x180")
        win.resizable(False, False)
        win.configure(fg_color="#1e1040")
        win.grab_set()

        # Centrar sobre el login
        self.root.update_idletasks()
        rx = self.root.winfo_x() + self.root.winfo_width() // 2 - 170
        ry = self.root.winfo_y() + self.root.winfo_height() // 2 - 90
        win.geometry(f"340x180+{rx}+{ry}")

        ctk.CTkFrame(win, height=4, fg_color="#e05252", corner_radius=0).pack(fill="x")

        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(expand=True, fill="both", padx=28, pady=16)

        top = ctk.CTkFrame(body, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        # Círculo de error
        badge = ctk.CTkFrame(top, width=36, height=36, corner_radius=18,
                              fg_color="#3d1a1a", border_width=1,
                              border_color="#e05252")
        badge.pack(side="left", padx=(0, 12))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="✕", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#e05252").place(relx=0.5, rely=0.5, anchor="center")

        txt_frame = ctk.CTkFrame(top, fg_color="transparent")
        txt_frame.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(txt_frame, text="Error de autenticación",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ede4ff", anchor="w").pack(anchor="w")
        ctk.CTkLabel(txt_frame, text=mensaje,
                     font=ctk.CTkFont(size=12),
                     text_color="#8878aa", anchor="w",
                     wraplength=200).pack(anchor="w")

        ctk.CTkButton(
            body, text="Entendido", width=120, height=34,
            corner_radius=8,
            fg_color="#3d1a1a", hover_color="#4d2020",
            border_width=1, border_color="#e05252",
            text_color="#e05252",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=win.destroy,
        ).pack(anchor="e")

    # ── Elementos flotantes ───────────────────────────────────────────────────

    EMOJIS = ["📚", "✏️", "📖", "🖊️", "📕", "📗", "📘", "📝"]
    POSITIONS = [
        (0.07, 0.10), (0.78, 0.08), (0.05, 0.62),
        (0.82, 0.68), (0.88, 0.28), (0.42, 0.85),
        (0.15, 0.80), (0.68, 0.16),
    ]

    def _init_floating_elements(self):
        self._floating = []
        for i, (emoji, (rx, ry)) in enumerate(zip(self.EMOJIS, self.POSITIONS)):
            phase = i * (2 * math.pi / len(self.EMOJIS))
            self._floating.append({"emoji": emoji, "rx": rx, "ry": ry, "phase": phase})

    def _animate_floating(self, tick=0):
        w = self.canvas.winfo_width() or 750
        h = self.canvas.winfo_height() or 520
        self.canvas.delete("float")

        for el in self._floating:
            offset = 14 * math.sin(tick * 0.035 + el["phase"])
            x = el["rx"] * w
            y = el["ry"] * h + offset
            self.canvas.create_text(
                x, y,
                text=el["emoji"],
                font=("Segoe UI Emoji", 28),
                fill="#5a3fa0",
                stipple="gray50",
                tags="float",
            )

        self.root.after(40, self._animate_floating, tick + 1)

    def _on_resize(self, event=None):
        pass

    # ── Lógica (sin cambios) ──────────────────────────────────────────────────

    def validar(self):
        from Database.conexion import conectar
        from views.menu import MenuPrincipal

        user = self.txt_user.get()
        pasw = self.txt_pass.get()

        con = conectar()
        cursor = con.cursor()
        cursor.execute(
            "SELECT Rol FROM Usuarios WHERE Usuario = ? AND Clave = ?", (user, pasw)
        )
        res = cursor.fetchone()
        con.close()

        if res:
            self.root.destroy()
            ventana_menu = ctk.CTk()
            MenuPrincipal(ventana_menu)
            ventana_menu.mainloop()
        else:
            self._show_error("Usuario o clave incorrecta")