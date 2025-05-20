import tkinter as tk
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
        self.ventanaSesion.title("Inicio de Sesion")
        self.ventanaSesion.geometry("250x300")
        alto_ventana = 300
        y_centro = alto_ventana // 2
        etiqueta = tk.Label(self.ventanaSesion, text="Iniciar Sesión", fg= '#4bc5eb')
        etiqueta.config(font=("Cascadia Code", 20, "bold"))
        etiqueta.pack()
        etiqueta1 = tk.Label(self.ventanaSesion, text="Nombre de usuario:")
        etiqueta1.config(font=("Cascadia Code", 8, "bold"))
        etiqueta1.place(relx= 0.5, y= y_centro - 60, anchor=tk.CENTER)

        self.insertar_usuario = tk.Entry(self.ventanaSesion)
        self.insertar_usuario.place(relx=0.5, y=y_centro - 30, width=200, anchor=tk.CENTER)

        etiqueta2 = tk.Label(self.ventanaSesion, text="Contraseña:")
        etiqueta2.config(font=("Cascadia Code", 8, "bold"))
        etiqueta2.place(relx= 0.5, y=y_centro + 5, anchor=tk.CENTER)
        self.insertar_contraseña = tk.Entry(self.ventanaSesion, show="*")
        self.insertar_contraseña.place(relx=0.5, y=y_centro + 25, width=200, anchor=tk.CENTER)
        boton_ingresar = tk.Button(
        self.ventanaSesion,
        text="Ingresar",
        command= self.obtener_datos
        )
        boton_ingresar.place(relx=0.5, y=y_centro + 60, anchor=tk.CENTER)
        boton_ingresar.config(bg= '#5c55e6', fg= '#ffffff', font=("Corbel", 8, "bold"))
        self.ventanaSesion.mainloop()

    #Funcion GUI Pantalla de ordenes de inspeccion
    def habilitar_segunda_pantalla(self):
        self.ventanaOrdenes = tk.Tk()
        self.ventanaOrdenes.title("Órdenes de Inspección")
        self.ventanaOrdenes.geometry("250x300")
        alto_ventana = 300
        y_centro = alto_ventana // 2
        etiqueta = tk.Label(self.ventanaOrdenes, text="Órdenes de Inspección", fg= '#4bc5eb')
        etiqueta.config(font=("Cascadia Code", 20, "bold"))
        etiqueta.pack()
        etiqueta1 = tk.Label(self.ventanaOrdenes, text="Nombre de usuario:")
        etiqueta1.config(font=("Cascadia Code", 8, "bold"))
        etiqueta1.place(relx= 0.5, y= y_centro - 60, anchor=tk.CENTER)
