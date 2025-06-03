import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from CONTROL.gestorOrdenes import GestorOrdenDeInspeccion
from MODULES.sesion import Sesion

class PantallaOrdenInspeccion:

    def __init__(self, sesion:Sesion, gestor:GestorOrdenDeInspeccion = None):
        self.__gestor = gestor
        self.__sesion = sesion
        self.__ventanaIntermedia = None
        self.__ventanaOrdenes = None
        self.__ordenes_completas = []
        self.__ordenSeleccionada = None

    def seleccionOpcionCerrarOrdenInspeccion(self):
        self.__ventanaIntermedia = tk.Tk()
        self.__ventanaIntermedia.title("Opciones")
        self.__ventanaIntermedia.geometry("360x250")
        self.__ventanaIntermedia.configure(bg="#1e1e2f")

        frame = tk.Frame(self.__ventanaIntermedia, bg="#2a2a3b")
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
        self.__ventanaIntermedia.destroy()
        self.habilitarPantalla()

    def habilitarPantalla(self):
        print("Pantalla de Cierre de Orden de Inspección habilitada")
        self.__gestor = GestorOrdenDeInspeccion(sesionActual=self.__sesion)
        self.__gestor.iniciarCierreOrdenInspeccion()

        self.__ventanaOrdenes = tk.Tk()
        self.__ventanaOrdenes.title("Cierre de Orden")
        self.__ventanaOrdenes.geometry("600x600")

        frame = tk.Frame(self.__ventanaOrdenes, bg="#2a2a3b")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = tk.Label(frame, text="Cierre de Orden", bg="#2a2a3b", fg="white", font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=(10, 20))

        tk.Label(frame, text="Seleccione una orden:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(anchor="w")

        self.__ordenes_completas = self.__gestor.buscarOrdenes()
        lista_visual = self.mostrarOrdCompletamenteRealizadas(self.__ordenes_completas)
        self.__ordenSeleccionada = tk.StringVar()
        self.ordenes_combo = ttk.Combobox(frame, values=lista_visual, textvariable=self.__ordenSeleccionada, state="readonly")
        self.ordenes_combo.pack(fill="x", pady=5)

        tk.Label(frame, text="Observación de cierre:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))
        self.observacion_entry = tk.Entry(frame, font=("Segoe UI", 10))
        self.observacion_entry.pack(fill="x", pady=5)

        self.comentarios_motivos = {}

        tk.Label(frame, text="Motivos Fuera de Servicio:", bg="#2a2a3b", fg="#bbbbbb", anchor="w", font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))
        self.motivos_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=6, exportselection=False)
        lista_motivos = self.mostrarMotivosTipoFueraServicio()
        for motivo in lista_motivos:
            self.motivos_listbox.insert(tk.END, motivo)
        self.motivos_listbox.pack(fill="x", pady=5)
        self.motivos_listbox.bind('<<ListboxSelect>>', self.actualizar_comentarios_por_motivo)

        # --- Scrollable comentarios por motivo ---
        comentarios_container = tk.Frame(frame, bg="#2a2a3b")
        comentarios_container.pack(fill="both", expand=False, pady=5)
        canvas = tk.Canvas(comentarios_container, bg="#2a2a3b", height=120, highlightthickness=0)
        scrollbar = tk.Scrollbar(comentarios_container, orient="vertical", command=canvas.yview)
        self.comentarios_frame = tk.Frame(canvas, bg="#2a2a3b")

        self.comentarios_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.comentarios_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # --- Fin scrollable ---

        tk.Button(
            frame, text="Confirmar Cierre", command=self.tomarConfirmacionCierreOrden,
            bg="#29d884", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2"
        ).pack(pady=10, ipadx=10, ipady=5)

        tk.Button(
            frame, text="Cancelar", command=self.__ventanaOrdenes.destroy,
            bg="#d84b4b", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2"
        ).pack(pady=5, ipadx=10, ipady=5)

        self.__ventanaOrdenes.mainloop()

    def mostrarOrdCompletamenteRealizadas(self, ordenes_ordenadas):
        lista_visual = []
        for orden in ordenes_ordenadas:
            texto = f"N°: {orden[0]} | Fin: {orden[1]} | Estación: {orden[2]} | Sismógrafo: {orden[3]}"
            lista_visual.append(texto)
        print("Lista visual para combobox:", lista_visual)
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

    def pedirSeleccionMotivoTipoFueraServicio(self):
        return len(self.motivos_listbox.curselection()) > 0

    def tomarMotivoTipoFueraServicio(self):
        motivos = [self.motivos_listbox.get(i) for i in self.motivos_listbox.curselection()]
        self.__gestor.tomarMotivoTipoFueraServicio(motivos)
        return motivos

    def pedirComentario(self):
        return self.tomarComentario()
    
    def tomarComentario(self):
        return self.comentario_entry.get()

    # def tomarConfirmacionCierreOrden(self):
    #     return True 

    def tomarConfirmacionCierreOrden(self):
        ordenSelec = self.tomarOrdenInspeccionSeleccionada()

        if ordenSelec is None:
            return
        observacion = self.pedirObservacionCierreOrden()
        motivos = self.tomarMotivoTipoFueraServicio()
        comentarios_por_motivo = {}

        for motivo in motivos:
            comentario = self.comentarios_motivos[motivo].get() if motivo in self.comentarios_motivos else ""
            if not comentario:
                messagebox.showerror("Error", f"Debe ingresar un comentario para el motivo '{motivo}'.")
                return
            comentarios_por_motivo[motivo] = comentario
        self.__gestor.tomarComentario(comentarios_por_motivo)

        if not self.__gestor.tomarConfirmacionCierreOrden(ordenSelec, observacion, motivos):
            print("Validacion fallida, no se puede cerrar la orden.")
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
            lbl = tk.Label(self.comentarios_frame, text=f"Comentario para '{motivo}':", bg="#2a2a3b", fg="#bbbbbb", font=("Segoe UI", 9))
            lbl.pack(anchor="w")
            entry = tk.Entry(self.comentarios_frame, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(0, 5))
            self.comentarios_motivos[motivo] = entry
