import tkinter as tk
from tkinter import ttk, messagebox

from CONTROL.gestorOrdenes import GestorOrdenDeInspeccion
from MODULES.sesion import Sesion

# ==== PALETA ====
BG_WINDOW = "#0c1524"       # fondo general
BG_CARD   = "#18263a"       # tarjeta central
BG_FIELD  = "#22334b"       # campos grandes
FG_TEXT   = "#e6edf7"
FG_MUTED  = "#a2b1c9"
ACCENT    = "#ff8a3d"
ACCENT_D  = "#e07022"


class PantallaOrdenInspeccion:

    def __init__(self, sesion: Sesion, gestor: GestorOrdenDeInspeccion = None):
        self.__gestor = gestor
        self.__sesion = sesion
        self.__ventanaIntermedia = None
        self.__ventanaOrdenes = None
        self.__ordenes_completas = []
        self.__ordenSeleccionada = None
        self.comentarios_motivos = {}

    # =========================
    # Ventana de opción inicial
    # =========================
    def seleccionOpcionCerrarOrdenInspeccion(self):
        self.__ventanaIntermedia = tk.Tk()
        self.__ventanaIntermedia.title("Opciones")
        self.__ventanaIntermedia.geometry("380x220")
        self.__ventanaIntermedia.configure(bg=BG_WINDOW)

        wrapper = tk.Frame(self.__ventanaIntermedia, bg=BG_WINDOW)
        wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        card = tk.Frame(wrapper, bg=BG_CARD)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="Acciones disponibles",
            bg=BG_CARD,
            fg=FG_TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(18, 8))

        tk.Label(
            card,
            text="Elija qué desea hacer",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=("Segoe UI", 10)
        ).pack()

        btn = tk.Button(
            card,
            text="Cerrar orden de inspección",
            command=self.ayudaSeleccionOpcionCerrarOrdenInspeccion,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_D,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )
        btn.pack(pady=(20, 15), ipadx=14, ipady=5)

    def ayudaSeleccionOpcionCerrarOrdenInspeccion(self):
        self.__ventanaIntermedia.destroy()
        self.habilitarPantalla()

    # =========================
    # Ventana principal del CU
    # =========================
    def habilitarPantalla(self):
        print("Pantalla de Cierre de Orden de Inspección habilitada")
        self.__gestor = GestorOrdenDeInspeccion(sesionActual=self.__sesion)
        self.__gestor.iniciarCierreOrdenInspeccion()

        root = tk.Tk()
        self.__ventanaOrdenes = root
        root.title("Cierre de Orden de Inspección")
        root.geometry("720x600")
        root.configure(bg=BG_WINDOW)

        # Estilos ttk (para que combobox/scrollbars combinen)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background=BG_CARD, foreground=FG_TEXT, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", foreground=FG_MUTED)
        style.configure("TCombobox",
                        fieldbackground="white",
                        background="white",
                        foreground="#1b1b1b")
        style.map("TCombobox",
                  fieldbackground=[("readonly", "white")])

        # Wrapper + “card”
        wrapper = tk.Frame(root, bg=BG_WINDOW)
        wrapper.pack(fill="both", expand=True, padx=24, pady=24)

        card = tk.Frame(wrapper, bg=BG_CARD)
        card.pack(fill="both", expand=True, padx=4, pady=4)

        # Usamos grid para armonía
        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

        # Título
        lbl_title = tk.Label(
            card,
            text="Cierre de Orden",
            bg=BG_CARD,
            fg=FG_TEXT,
            font=("Segoe UI", 18, "bold")
        )
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(18, 10))

        sep = ttk.Separator(card, orient="horizontal")
        sep.grid(row=1, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 15))

        row = 2

        # ================= Datos generales =================
        ttk.Label(card, text="Seleccione una orden:", style="Muted.TLabel").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=22, pady=(0, 4)
        )

        self.__ordenes_completas = self.__gestor.buscarOrdenes()
        lista_visual = self.mostrarOrdCompletamenteRealizadas(self.__ordenes_completas)

        self.__ordenSeleccionada = tk.StringVar()
        self.ordenes_combo = ttk.Combobox(
            card,
            values=lista_visual,
            textvariable=self.__ordenSeleccionada,
            state="readonly",
        )
        self.ordenes_combo.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=22, pady=(0, 10))

        row += 2

        ttk.Label(card, text="Observación de cierre:", style="Muted.TLabel").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=22, pady=(10, 4)
        )

        self.observacion_entry = tk.Entry(card, font=("Segoe UI", 10))
        self.observacion_entry.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=22, pady=(0, 10))

        row += 2

        # ================= Motivos =================
        ttk.Label(card, text="Motivos de Fuera de Servicio:", style="Muted.TLabel").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=22, pady=(10, 4)
        )

        self.motivos_listbox = tk.Listbox(
            card,
            selectmode=tk.MULTIPLE,
            height=6,
            bg=BG_FIELD,
            fg=FG_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#202f46",
            selectbackground=ACCENT,
            selectforeground="white",
        )
        lista_motivos = self.mostrarMotivosTipoFueraServicio()
        for motivo in lista_motivos:
            self.motivos_listbox.insert(tk.END, motivo)
        self.motivos_listbox.grid(row=row + 1, column=0, columnspan=2, sticky="nsew", padx=22, pady=(0, 8))
        self.motivos_listbox.bind("<<ListboxSelect>>", self.actualizar_comentarios_por_motivo)

        row += 2

        # ================= Comentarios por motivo =================
        ttk.Label(card, text="Comentarios por motivo:", style="Muted.TLabel").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=22, pady=(8, 4)
        )

        comentarios_container = tk.Frame(card, bg=BG_CARD)
        comentarios_container.grid(row=row + 1, column=0, columnspan=2,
                                   sticky="nsew", padx=22, pady=(0, 10))

        card.rowconfigure(row + 1, weight=1)

        canvas = tk.Canvas(comentarios_container, bg=BG_CARD, highlightthickness=0)
        scrollbar = tk.Scrollbar(comentarios_container, orient="vertical", command=canvas.yview)
        self.comentarios_frame = tk.Frame(canvas, bg=BG_CARD)

        self.comentarios_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.comentarios_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.comentarios_motivos.clear()

        row += 2

        # ================= Botones =================
        buttons_frame = tk.Frame(card, bg=BG_CARD)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=(12, 18))

        btn_confirmar = tk.Button(
            buttons_frame,
            text="Confirmar cierre",
            command=self.tomarConfirmacionCierreOrden,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_D,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )
        btn_confirmar.pack(side="left", padx=(0, 10), ipadx=12, ipady=5)

        btn_cancelar = tk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.__ventanaOrdenes.destroy,
            bg="#c24747",
            fg="white",
            activebackground="#a33737",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11),
            cursor="hand2"
        )
        btn_cancelar.pack(side="left", ipadx=12, ipady=5)

        root.mainloop()

    # ================= Lógica auxiliar =================
    def mostrarOrdCompletamenteRealizadas(self, ordenes_ordenadas):
        lista_visual = []
        for orden in ordenes_ordenadas:
            texto = f"N° {orden[0]}  |  Fin: {orden[1]}  |  Estación: {orden[2]}  |  Sismógrafo: {orden[3]}"
            lista_visual.append(texto)
        return lista_visual

    def pedirSeleccionOrdenInspeccion(self):
        idx = self.ordenes_combo.current()
        if idx < 0:
            messagebox.showerror("Error", "Debe seleccionar una orden.")
            return False
        return True

    def tomarOrdenInspeccionSeleccionada(self):
        if not self.pedirSeleccionOrdenInspeccion():
            return None
        idx = self.ordenes_combo.current()
        return self.__ordenes_completas[idx]

    def pedirObservacionCierreOrden(self):
        observacion = self.tomarObservacionCierreOrden()
        self.__gestor.tomarObservacionCierreOrden(observacion)
        return observacion

    def tomarObservacionCierreOrden(self):
        return self.observacion_entry.get()

    def mostrarMotivosTipoFueraServicio(self):
        return self.__gestor.buscarMotivoTiposFueraServicio()

    def tomarMotivoTipoFueraServicio(self):
        motivos = [self.motivos_listbox.get(i) for i in self.motivos_listbox.curselection()]
        self.__gestor.tomarMotivoTipoFueraServicio(motivos)
        return motivos

    def tomarConfirmacionCierreOrden(self):
        ordenSelec = self.tomarOrdenInspeccionSeleccionada()
        if ordenSelec is None:
            return

        observacion = self.pedirObservacionCierreOrden()
        motivos = self.tomarMotivoTipoFueraServicio()
        comentarios_por_motivo = {}

        for motivo in motivos:
            comentario = self.comentarios_motivos.get(motivo)
            comentario = comentario.get() if comentario else ""
            if not comentario:
                messagebox.showerror("Error", f"Debe ingresar un comentario para el motivo '{motivo}'.")
                return
            comentarios_por_motivo[motivo] = comentario

        self.__gestor.tomarComentario(comentarios_por_motivo)

        if not self.__gestor.tomarConfirmacionCierreOrden(ordenSelec, observacion, motivos):
            print("Validación fallida, no se puede cerrar la orden.")
            return

        self.__gestor.enviarMails()
        self.__gestor.finCU()
        messagebox.showinfo("Éxito", "La orden fue cerrada correctamente.")
        self.__ventanaOrdenes.destroy()

    def actualizar_comentarios_por_motivo(self, event=None):
        for widget in self.comentarios_frame.winfo_children():
            widget.destroy()
        self.comentarios_motivos.clear()

        motivos_seleccionados = [self.motivos_listbox.get(i) for i in self.motivos_listbox.curselection()]
        for motivo in motivos_seleccionados:
            lbl = tk.Label(
                self.comentarios_frame,
                text=f"Comentario para '{motivo}':",
                bg=BG_CARD,
                fg=FG_MUTED,
                font=("Segoe UI", 9, "bold")
            )
            lbl.pack(anchor="w", pady=(0, 2))

            entry = tk.Entry(self.comentarios_frame, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(0, 6))

            self.comentarios_motivos[motivo] = entry
