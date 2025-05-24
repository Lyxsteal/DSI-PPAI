from MODULES.modules import obtenerUsuario, obtenerOrdenesRealizadas, obtener_orden_desde_db
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from CONTROL.gestorOrdenes import GestorOrdenDeInspeccion
from MODULES.sesion import Sesion

class PantallaOrdenInspeccion:

    def __init__(self, sesion:Sesion, gestor:GestorOrdenDeInspeccion = None):
        self.gestor = gestor
        self.sesion = sesion
        self.ventanaIntermedia = None
        self.ventanaOrdenes = None
        self.ordenes_completas = []
        self.ordenSeleccionada = None

    def seleccionOpcionCerrarOrdenInspeccion(self):
        self.ventanaIntermedia = tk.Tk()
        self.ventanaIntermedia.title("Opciones")
        self.ventanaIntermedia.geometry("360x250")
        self.ventanaIntermedia.configure(bg="#1e1e2f")

        frame = tk.Frame(self.ventanaIntermedia, bg="#2a2a3b")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=300, height=150)

        radio = tk.Button(
            frame,
            text="Cerrar Orden Inspección",
            bg="#2a2a3b",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            activebackground="#2a2a3b",
            activeforeground="white",
            command=self.ayudaSeleccionOpcionCerrarOrdenInspeccion
        )
        radio.pack(pady=(50, 20))

    def ayudaSeleccionOpcionCerrarOrdenInspeccion(self):
        print('Opción seleccionada: Cerrar Orden Inspeccion')
        self.ventanaIntermedia.destroy()
        self.habilitarPantalla()

    def habilitarPantalla(self):
        print("Pantalla de Cierre de Orden de Inspección habilitada")
        self.gestor = GestorOrdenDeInspeccion(sesionActual=self.sesion)
        self.gestor.iniciarCierreOrdenInspeccion()

        self.ventanaOrdenes = tk.Tk()
        self.ventanaOrdenes.title("Cierre de Orden")
        self.ventanaOrdenes.geometry("600x550")
        alto_ventana = 550
        y_centro = alto_ventana // 2

        etiqueta = tk.Label(self.ventanaOrdenes, text="", fg='#4bc5eb')
        etiqueta.config(font=("Cascadia Code", 20, "bold"))
        etiqueta.pack()
        etiqueta1 = tk.Label(self.ventanaOrdenes, text="Nombre de usuario:")
        etiqueta1.config(font=("Cascadia Code", 8, "bold"))
        etiqueta1.place(relx=0.5, y=y_centro - 200, anchor=tk.CENTER)

        frame = tk.Frame(self.ventanaOrdenes, bg="#2a2a3b")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=440, height=500)

        titulo = tk.Label(frame, text="Cierre de Orden", bg="#2a2a3b", fg="white", font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=10)

        tk.Label(frame, text="Seleccione una orden:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w")

        self.ordenes_completas = self.gestor.ordenes
        lista_visual = self.mostrarOrdCompletamenteRealizadas(self.ordenes_completas)
        self.ordenSeleccionada = tk.StringVar()
        self.ordenes_combo = ttk.Combobox(frame, values=lista_visual, textvariable=self.ordenSeleccionada, state="readonly")
        self.ordenes_combo.pack(padx=20, fill="x", pady=5)

        tk.Label(frame, text="Observación de cierre:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w", pady=(10, 0))
        self.observacion_entry = tk.Entry(frame, font=("Segoe UI", 10))
        self.observacion_entry.pack(padx=20, fill="x", pady=5)

        self.comentarios_motivos = {}  # Nuevo: para guardar los Entry de comentarios por motivo

        tk.Label(frame, text="Motivos Fuera de Servicio:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(padx=20, anchor="w", pady=(10, 0))
        self.motivos_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=4, exportselection=False)
        for motivo in ["Falla técnica", "Equipo no disponible"]:
            self.motivos_listbox.insert(tk.END, motivo)
        self.motivos_listbox.pack(padx=20, fill="x", pady=5)
        self.motivos_listbox.bind('<<ListboxSelect>>', self.actualizar_comentarios_por_motivo)  # Nuevo: actualizar comentarios

        self.comentarios_frame = tk.Frame(frame, bg="#2a2a3b")  # Nuevo: frame para comentarios por motivo
        self.comentarios_frame.pack(padx=20, fill="x", pady=5)

        tk.Button(
            frame, text="Confirmar Cierre", command=self.confirmar_cierre,
            bg="#29d884", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2"
        ).pack(pady=20, ipadx=10, ipady=5)

        tk.Button(
            frame, text="Cancelar", command=self.ventanaOrdenes.destroy,
            bg="#d84b4b", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2"
        ).pack(pady=5, ipadx=10, ipady=5)

        self.ventanaOrdenes.mainloop()

    def mostrarOrdCompletamenteRealizadas(self, ordenes):
        lista_visual = []
        for orden in ordenes:
            texto = f"N°: {orden.getNroOrden()} | Fin: {orden.getfechaHoraFinalizacion()} | Estación: {orden.getNombreEstacion()} | Sismógrafo: {orden.getIdentificadorSismografo()}"
            lista_visual.append(texto)
        print("Lista visual para combobox:", lista_visual)
        return lista_visual

    def pedirSeleccionOrdenInspeccion(self):
        return self.ordenes_combo.current() >= 0

    def tomarOrdenInspeccionSeleccionada(self):
        idx = self.ordenes_combo.current()
        if idx < 0:
            return None
        return self.ordenes_completas[idx]

    def pedirObservacionCierreOrden(self):
        return self.observacion_entry.get()

    def tomarObservacionCierreOrden(self):
        return self.observacion_entry.get()

    def mostrarMotivosTipoFueraServicio(self):
        return [self.motivos_listbox.get(i) for i in range(self.motivos_listbox.size())]

    def pedirSeleccionMotivoTipoFueraServicio(self):
        return len(self.motivos_listbox.curselection()) > 0

    def tomarMotivoTipoFueraServicio(self):
        return [self.motivos_listbox.get(i) for i in self.motivos_listbox.curselection()]

    def pedirComentario(self):
        return self.comentario_entry.get()

    def tomarComentario(self):
        return self.comentario_entry.get()

    def pedirConfirmacionCierreOrden(self):
        print("UI: Pidiendo confirmación final para cerrar la orden.")
        return messagebox.askyesno("Confirmar Cierre", "¿Está seguro de que desea cerrar esta orden de inspección?")

    def tomarConfirmacionCierreOrden(self):
        return True

    def confirmar_cierre(self):
        idx = self.ordenes_combo.current()
        if idx < 0:
            messagebox.showerror("Error", "Debe seleccionar una orden.")
            return

        orden_obj = self.ordenes_completas[idx]
        observacion = self.observacion_entry.get()
        motivos = [self.motivos_listbox.get(i) for i in self.motivos_listbox.curselection()]

        # Nuevo: obtener comentarios por motivo
        comentarios_por_motivo = {}
        for motivo in motivos:
            comentario = self.comentarios_motivos[motivo].get() if motivo in self.comentarios_motivos else ""
            if not comentario:
                messagebox.showerror("Error", f"Debe ingresar un comentario para el motivo '{motivo}'.")
                return
            comentarios_por_motivo[motivo] = comentario

        self.gestor.tomarOrdenInspeccionSeleccionada(orden_obj)
        self.gestor.tomarObservacionCierreOrden(observacion)
        self.gestor.tomarMotivoTipoFueraServicio(motivos)
        

        if not self.gestor.validarExistenciaObservacion():
            messagebox.showerror("Error", "Observación requerida.")
            return

        if not self.gestor.validarExistenciaMotivoSeleccionado():
            messagebox.showerror("Error", "Debe seleccionar al menos un motivo.")
            return

        if not self.pedirConfirmacionCierreOrden():
            return

        estado_cerrada = self.gestor.buscarEstadoCerrada()
        self.gestor.cerrarOrdenInspeccion(estado_cerrada)
        self.gestor.enviarMails()
        self.gestor.finCU()
        messagebox.showinfo("Éxito", "La orden fue cerrada correctamente.")
        self.ventanaOrdenes.destroy()

    def actualizar_comentarios_por_motivo(self, event=None):
        # Borra los widgets anteriores
        for widget in self.comentarios_frame.winfo_children():
            widget.destroy()
        self.comentarios_motivos.clear()

        motivos_seleccionados = [self.motivos_listbox.get(i) for i in self.motivos_listbox.curselection()]
        for motivo in motivos_seleccionados:
            lbl = tk.Label(self.comentarios_frame, text=f"Comentario para '{motivo}':", bg="#2a2a3b", fg="#bbbbbb", font=("Segoe UI", 9))
            lbl.pack(anchor="w")
            entry = tk.Entry(self.comentarios_frame, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(0, 5))
            self.comentarios_motivos[motivo] = entry
