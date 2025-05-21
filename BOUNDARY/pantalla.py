import tkinter as tk
from tkinter import ttk

from CONTROL.gestor import GestorOrdenDeInspeccion
class Pantalla():
    def __init__(self):
        self.nombre_usuario = None
        self.contraseña_iniciada = None
        self.insertar_usuario = None
        self.insertar_contraseña = None
        self.sesion = None
        self.ventanaSesion = None

    #Funcion para obtener los datos de la ventana cuando apretas el boton    
    def obtener_datos(self):
        nombre_usuario = self.insertar_usuario.get()
        contraseña_iniciada = self.insertar_contraseña.get()
        print("Nombre de usuario:", nombre_usuario)
        print("Contraseña:", contraseña_iniciada)
        gestor = GestorOrdenDeInspeccion()
        sesion, mensaje = gestor.iniciarSesion(nombre_usuario, contraseña_iniciada)
        print(mensaje)
        if sesion:
            self.sesion = sesion  # guardar la sesión si querés usarla después
            self.ventanaSesion.destroy()
            self.habilitar_segunda_pantalla()
        else:
            self.ventanaSesion.destroy()

    #Funcion para habilitar la primera pantalla (inicio de sesion)        
    def seleccionOpcionIniciarSesion(self):
        self.habilitar_primera_pantalla()

    #Funcion GUI Pantalla inicio de sesion           
    def habilitar_primera_pantalla(self):
        self.ventanaSesion = tk.Tk()
        self.ventanaSesion.title("Inicio de Sesión")
        self.ventanaSesion.geometry("360x460")
        self.ventanaSesion.configure(bg="#1e1e2f")  # Fondo general oscuro

        alto_ventana = 460

        # Sombra más clara debajo
        sombra = tk.Frame(self.ventanaSesion, bg="#2c2c3a")
        sombra.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=300, height=360)

        # Tarjeta superior
        tarjeta = tk.Frame(self.ventanaSesion, bg="#2a2a3b")
        tarjeta.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=300, height=360, x=-3, y=-3)

        # Título
        etiqueta = tk.Label(tarjeta, text="Iniciar Sesión", fg="#ffffff", bg="#2a2a3b")
        etiqueta.config(font=("Segoe UI", 18, "bold"))
        etiqueta.pack(pady=(30, 20))

        # Etiqueta usuario
        etiqueta1 = tk.Label(tarjeta, text="Usuario", bg="#2a2a3b", fg="#bbbbbb", anchor="w")
        etiqueta1.config(font=("Segoe UI", 10))
        etiqueta1.pack(fill="x", padx=40)

        self.insertar_usuario = tk.Entry(tarjeta, font=("Segoe UI", 10), bd=0,
                                         highlightthickness=1, highlightbackground="#444", highlightcolor="#4bc5eb",
                                         bg="#3a3a4f", fg="#ffffff", insertbackground="white")
        self.insertar_usuario.pack(padx=40, pady=(0, 20), ipady=5, fill="x")

        # Etiqueta contraseña
        etiqueta2 = tk.Label(tarjeta, text="Contraseña", bg="#2a2a3b", fg="#bbbbbb", anchor="w")
        etiqueta2.config(font=("Segoe UI", 10))
        etiqueta2.pack(fill="x", padx=40)

        self.insertar_contraseña = tk.Entry(tarjeta, font=("Segoe UI", 10), bd=0, show="*",
                                            highlightthickness=1, highlightbackground="#444", highlightcolor="#4bc5eb",
                                            bg="#3a3a4f", fg="#ffffff", insertbackground="white")
        self.insertar_contraseña.pack(padx=40, pady=(0, 30), ipady=5, fill="x")

        # Botón estilo neón
        boton_ingresar = tk.Button(
            tarjeta,
            text="Ingresar",
            command=self.obtener_datos,
            bg="#4bc5eb",
            fg="white",
            activebackground="#38b0d8",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        boton_ingresar.pack(pady=(0, 20), ipadx=10, ipady=5)

        self.ventanaSesion.mainloop()



    #Funcion GUI Pantalla de ordenes de inspeccion
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

