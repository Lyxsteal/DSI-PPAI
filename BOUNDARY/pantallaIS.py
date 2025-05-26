import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3
import os

from CONTROL.gestorIS import GestorIS
from BOUNDARY.pantallaOrdenInspeccion import PantallaOrdenInspeccion
from MODULES.Usuario import Usuario
from MODULES.sesion import Sesion
from MODULES.empleado import Empleado

class Pantalla():
    def __init__(self):
        self.nombre_usuario = None
        self.contraseña_iniciada = None
        self.insertar_usuario = None
        self.insertar_contraseña = None
        self.sesion = None
        self.ventanaSesion = None
        self.pantallaOI = None
        self.gestor = None

    # IMPORTANTE : Cambiar para que tome los datos de la ventana y no los temporales para testing 
    # Funcion para obtener los datos de la ventana cuando apretas el boton  
    def obtener_datos(self):
        #nombre_usuario = self.insertar_usuario.get()
        #contraseña_iniciada = self.insertar_contraseña.get()
        nombre_usuario = 'jperez'
        contraseña_iniciada = 'Clave123#'
        print("Nombre de usuario:", nombre_usuario)
        print("Contraseña:", contraseña_iniciada)
        #No me deberia servir porqe existe sesion abajo
        #sesionActual = Sesion(Usuario(nombre_usuario, contraseña_iniciada))
        self.gestor = GestorIS()
        sesion, mensaje = self.gestor.iniciarSesion(nombre_usuario, contraseña_iniciada)
        print(mensaje)
        if sesion:
            pantallaOPI = PantallaOrdenInspeccion(sesion = sesion)
            self.sesion = sesion 
            self.ventanaSesion.destroy()
            pantallaOPI.seleccionOpcionCerrarOrdenInspeccion() 
        else:
            self.ventanaSesion.destroy()


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

    def seleccionOpcionIniciarSesion(self):
        self.habilitar_primera_pantalla()
    
"""         #Funcion que obtiene los usuarios de la base de datos (mover a usuario.py)
    def obtenerUsuario(self):
        db_path = os.path.join(os.path.dirname(__file__), '../MODULES/database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nombre, contraseña
            FROM Usuario
        ''')
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    
    #Funcion que obtiene los datos de la bd, los verifica con los ingresados en la pantalla, crea una sesion en la tabla Sesion
    def iniciarSesion(self, nombre_usuario, contraseña_iniciada):
        sesion = None
        usuarios = self.obtenerUsuario()
        fechaActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for usuario in usuarios:
            nombre = usuario[0]
            contraseña = usuario[1]
            if nombre == nombre_usuario and contraseña == contraseña_iniciada:
                db_path = os.path.join(os.path.dirname(__file__), '../MODULES/database.db')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Sesion (fechaInicio, usuario)
                    VALUES (?, ?)
                ''', (fechaActual, nombre))
                cursor.execute('''SELECT empleado FROM Usuario WHERE nombre = ?''', (nombre_usuario,))
                empleado = cursor.fetchone()
                empleado_nombre = empleado[0]
                conn.commit()
                cursor.execute('''
                    SELECT * FROM Empleados WHERE nombre = ?
                ''', (empleado_nombre,))
                fila_empleado = cursor.fetchone()
                if fila_empleado:
                    empleado_selec = Empleado(fila_empleado[0], fila_empleado[1], fila_empleado[2], fila_empleado[3], fila_empleado[4])
                conn.close()
                usuario = Usuario(nombre, contraseña, empleado_selec)
                self.sesion = Sesion(fechaInicio=fechaActual, usuario=usuario)
                sesion = self.sesion
                return sesion, 'Sesión iniciada con éxito.'
        return None, 'Usuario o contraseña incorrectos.' """