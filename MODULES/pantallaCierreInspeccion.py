from CONTROL.gestor import GestorOrdenDeInspeccion
from MODULES.modules import obtenerUsuario, obtenerOrdenesRealizadas, obtener_orden_desde_db
import sqlite3
from MODULES.Usuario import Usuario
from datetime import datetime
from MODULES.sesion import Sesion
from MODULES.empleado import Empleado
class PantallaCierreInspeccion:

    def __init__(self, usuario:Usuario=None):
        self.usuario = None
    def IniciarSesion(self):
        nombre_iniciado= input('Bienvenido, ingrese su nombre de usuario: ')
        contraseña_iniciado = input('Bienvenido, ingrese su contraseña: ')
        usuarios = obtenerUsuario()
        fechaActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for usuario in usuarios:
            nombre = usuario[0]
            contraseña = usuario[1]
            if nombre == nombre_iniciado and contraseña == contraseña_iniciado:
                conn = sqlite3.connect('MODULES/database.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Sesion (fechaInicio, usuario)
                    VALUES (?, ?)
                ''', (fechaActual, nombre))
                cursor.execute('''SELECT empleado FROM Usuario WHERE nombre = ?''', (nombre_iniciado,))
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
                self.sesion = Sesion(fechaActual, usuario)
                sesion = self.sesion
            return sesion, 'Sesión iniciada con éxito.'
        print('Usuario o contraseña incorrectos.')
        return None
    
    #
    def mostrarOrdCompletamenteRealizadas(self, sesion):
        filas = obtener_orden_desde_db()
        gestor = GestorOrdenDeInspeccion(sesionActual= sesion)
        ordenes_filtradas = gestor.obtenerDatos(filas, sesion)
        for orden in ordenes_filtradas:
            print("Número de orden:", orden.getNroOrden(), 
                  'Fecha de finalización:', orden.getfechaHoraFinalizacion(), 
                  'Identificador del sismógrafo:', orden.getIdentificadorSismografo(),
                  'Nombre de la estación:', orden.getNombreEstacion())

    def habilitarPantalla(self):
        sesion, mensaje = self.IniciarSesion()
        if sesion is not None:
            print('Sesión iniciada con éxito.')
            print('Bienvenido, ', sesion.obtenerEmpleadoLogeado().getNombre()) 
            print("Opciones disponibles:")
            print("1. Cerrar orden de inspección")
            opcion = input("Seleccione una opción (ingrese el número): ")
            if opcion == "1":
                print("Ha seleccionado: Cerrar orden de inspección")
                self.mostrarOrdCompletamenteRealizadas(sesion)
