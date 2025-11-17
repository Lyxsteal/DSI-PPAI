import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from CONTROL.gestorIS import GestorIS
from BOUNDARY.pantallaOrdenInspeccion import PantallaOrdenInspeccion
from MODULES.sesion import Sesion

# ==== PALETA NUEVA ====
# Degradado naranja
GRADIENT_TOP = "#ffb27d"     # naranja claro
GRADIENT_BOTTOM = "#ff7b22"  # naranja fuerte

# Card azul oscuro elegante
CARD_BG = "#18263a"
INPUT_BG = "#22334b"
TEXT_FG = "#e6edf7"
TEXT_MUTED = "#c3cfe2"

ACCENT = "#ff8a3d"
ACCENT_DARK = "#e07022"


class Pantalla():
    def __init__(self):
        self.insertar_usuario = None
        self.insertar_contraseña = None
        self.ventanaSesion = None
        self.gestor = None
        self.counter = 0

    # =============================
    # Generar degradado naranja
    # =============================
    def crear_degradado(self, canvas, width, height, color1, color2):
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)

        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
            canvas.create_line(0, i, width, i, fill=color)

    def obtener_datos(self):
        nombre_usuario = self.insertar_usuario.get()
        contraseña_iniciada = self.insertar_contraseña.get()

        self.gestor = GestorIS()
        sesion, mensaje = self.gestor.iniciarSesion(nombre_usuario, contraseña_iniciada)

        if sesion:
            pantallaOPI = PantallaOrdenInspeccion(sesion=sesion)
            self.ventanaSesion.destroy()
            pantallaOPI.seleccionOpcionCerrarOrdenInspeccion()
        else:
            self.counter += 1
            if self.counter > 3:
                messagebox.showerror("Error", 'Demasiados intentos fallidos, cerrando ventana...')
                self.ventanaSesion.destroy()

    # ====================================================
    # PANTALLA DE LOGIN CON DEGRADADO NARANJA + CARD AZUL
    # ====================================================
    def habilitar_primera_pantalla(self):
        self.ventanaSesion = tk.Tk()
        self.ventanaSesion.title("Inicio de Sesión")
        self.ventanaSesion.geometry("420x520")
        self.ventanaSesion.resizable(False, False)

        # Canvas para degradado
        canvas = tk.Canvas(self.ventanaSesion, width=420, height=520, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        self.ventanaSesion.update()
        w, h = 420, 520
        self.crear_degradado(canvas, w, h, GRADIENT_TOP, GRADIENT_BOTTOM)

        # ==== TARJETA AZUL OSCURO ====
        card = tk.Frame(self.ventanaSesion, bg=CARD_BG)
        card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=380)

        # ===== TÍTULO =====
        titulo = tk.Label(
            card,
            text="Iniciar Sesión",
            bg=CARD_BG,
            fg=TEXT_FG,
            font=("Segoe UI", 20, "bold")
        )
        titulo.pack(pady=(25, 4))

        subtitulo = tk.Label(
            card,
            text="Ingrese sus credenciales para continuar",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9)
        )
        subtitulo.pack(pady=(0, 18))

        # ===== INPUT USUARIO =====
        lbl_user = tk.Label(
            card,
            text="Usuario",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=("Segoe UI", 10),
            anchor="w"
        )
        lbl_user.pack(fill="x", padx=36)

        self.insertar_usuario = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bd=0,
            bg=INPUT_BG,
            fg=TEXT_FG,
            insertbackground="white"
        )
        self.insertar_usuario.pack(padx=36, pady=(2, 16), ipady=6, fill="x")

        # ===== INPUT CONTRASEÑA =====
        lbl_pass = tk.Label(
            card,
            text="Contraseña",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=("Segoe UI", 10),
            anchor="w"
        )
        lbl_pass.pack(fill="x", padx=36)

        self.insertar_contraseña = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bd=0,
            show="*",
            bg=INPUT_BG,
            fg=TEXT_FG,
            insertbackground="white"
        )
        self.insertar_contraseña.pack(padx=36, pady=(2, 22), ipady=6, fill="x")

        # ===== BOTÓN INGRESAR =====
        boton_ingresar = tk.Button(
            card,
            text="Ingresar",
            command=self.obtener_datos,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_DARK,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2"
        )
        boton_ingresar.pack(pady=(0, 16), ipadx=18, ipady=7)

        # ===== PIE =====
        pie = tk.Label(
            card,
            text="Sistema de gestión de órdenes de inspección",
            bg=CARD_BG,
            fg=TEXT_MUTED,
            font=("Segoe UI", 8)
        )
        pie.pack(side="bottom", pady=(0, 10))

        # ENTER = ingresar
        self.ventanaSesion.bind("<Return>", lambda e: self.obtener_datos())

        self.ventanaSesion.mainloop()

    def seleccionOpcionIniciarSesion(self):
        self.habilitar_primera_pantalla()
