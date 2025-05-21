from CONTROL.gestor import GestorOrdenDeInspeccion
from MODULES.modules import obtenerUsuario, obtenerOrdenesRealizadas, obtener_orden_desde_db
import sqlite3
from MODULES.usuario import Usuario
from datetime import datetime
from MODULES.sesion import Sesion
from MODULES.empleado import Empleado
import tkinter as tk
from tkinter import ttk
class PantallaOrdenInspeccion:

    def __init__(self, gestor,usuario:Usuario=None):
        self.gestor = gestor
        self.usuario = usuario

# Como tal no existe 'IniciarSesion' en el diagrama y no veo que se use asi que eliminé la función

    def seleccionOpcionCerrarOrdenInspeccion(self):
        print("Opcion Cerrar orden de inspección seleccionada")

    def habilitarPantalla(self):
        self.habilitar_segunda_pantalla()

    def habilitar_segunda_pantalla(self):
        self.ventanaOrdenes = tk.Tk()
        self.ventanaOrdenes.title()
        self.ventanaOrdenes.geometry("600x550")
        alto_ventana = 550
        y_centro = alto_ventana // 2

        etiqueta = tk.Label(self.ventanaOrdenes, text="", fg='#4bc5eb')
        etiqueta.config(font=("Cascadia Code", 20, "bold"))
        etiqueta.pack()
        etiqueta1 = tk.Label(self.ventanaOrdenes, text="Nombre de usuario:")
        etiqueta1.config(font=("Cascadia Code", 8, "bold"))
        etiqueta1.place(relx=0.5, y=y_centro - 200, anchor=tk.CENTER)

        # Tarjeta
        frame = tk.Frame(self.ventanaOrdenes, bg="#2a2a3b")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=440, height=500)

        # Título
        titulo = tk.Label(frame, text="Cierre de Orden", bg="#2a2a3b", fg="white", font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=10)

        # Ordenes realizadas (simulado)
        tk.Label(frame, text="Seleccione una orden:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w")
        ordenes_combo = ttk.Combobox(frame, values=["Orden #101", "Orden #102", "Orden #103"])
        ordenes_combo.pack(padx=20, fill="x", pady=5)

        # Observación
        tk.Label(frame, text="Observación de cierre:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w", pady=(10, 0))
        observacion_entry = tk.Entry(frame, font=("Segoe UI", 10))
        observacion_entry.pack(padx=20, fill="x", pady=5)

        # Motivos
        tk.Label(frame, text="Motivos Fuera de Servicio:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w", pady=(10, 0))
        motivos_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=4, exportselection=False)
        for motivo in ["Falla técnica", "Equipo no disponible"]:
            motivos_listbox.insert(tk.END, motivo)
        motivos_listbox.pack(padx=20, fill="x", pady=5)

        # Comentario por motivo
        tk.Label(frame, text="Comentario general:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w", pady=(10, 0))
        comentario_entry = tk.Entry(frame, font=("Segoe UI", 10))
        comentario_entry.pack(padx=20, fill="x", pady=5)

        # Botón Confirmar
        def confirmar_cierre():
            orden = ordenes_combo.get()
            observacion = observacion_entry.get()
            motivos = [motivos_listbox.get(i) for i in motivos_listbox.curselection()]
            comentario = comentario_entry.get()
            print("Orden:", orden)
            print("Observación:", observacion)
            print("Motivos seleccionados:", motivos)
            print("Comentario:", comentario)

        tk.Button(
            frame, text="Confirmar Cierre", command=confirmar_cierre,
            bg="#29d884", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2"
        ).pack(pady=20, ipadx=10, ipady=5)
        self.ventanaOrdenes.mainloop()

    def mostrarOrdCompletamenteRealizadas(self, sesion):
        filas = obtener_orden_desde_db()
        self.gestor = GestorOrdenDeInspeccion(sesion)
        ordenes_filtradas = self.gestor.buscarOrdenesDeInspeccion(filas, sesion)
        for orden in ordenes_filtradas:
            print("Número de orden:", orden.getNroOrden(), 
                  'Fecha de finalización:', orden.getfechaHoraFinalizacion(), 
                  'Identificador del sismógrafo:', orden.getIdentificadorSismografo(),
                  'Nombre de la estación:', orden.getNombreEstacion())