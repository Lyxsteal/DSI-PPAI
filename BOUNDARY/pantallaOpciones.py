import tkinter as tk
from tkinter import ttk
from BOUNDARY.pantallaOrdenInspeccion import PantallaOrdenInspeccion
from CONTROL.gestor import GestorOrdenDeInspeccion
class PantallaOpciones:
    def __init__(self, gestor):
        self.gestor = gestor
        self.ventanaIntermedia = None
        self.pantallaOI = None

    def habilitar_pantalla_intermedia(self):
        self.ventanaIntermedia = tk.Tk()
        self.ventanaIntermedia.title("Opciones")
        self.ventanaIntermedia.geometry("360x250")
        self.ventanaIntermedia.configure(bg="#1e1e2f")

        frame = tk.Frame(self.ventanaIntermedia, bg="#2a2a3b")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=300, height=150)

        # Variable para el radiobutton
        self.opcion_intermedia = tk.StringVar(value="")

        radio = tk.Button(
            frame,
            text="Cerrar Orden Inspección",
            bg="#2a2a3b",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            activebackground="#2a2a3b",
            activeforeground="white",
            command=self._continuar_a_segunda_pantalla  
        )
        radio.pack(pady=(50, 20))

        self.ventanaIntermedia.mainloop()
    def _continuar_a_segunda_pantalla(self):
        # Uso los metodos del diagrama seleccionOpcionCerrarOrdenInspeccion y habilitarPantalla
        self.pantallaOI = PantallaOrdenInspeccion(gestor = self.gestor)
        self.pantallaOI.seleccionOpcionCerrarOrdenInspeccion()
        self.ventanaIntermedia.destroy()
        self.pantallaOI.habilitarPantalla()