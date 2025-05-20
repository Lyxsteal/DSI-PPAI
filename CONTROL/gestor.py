from datetime import datetime
import sqlite3
from MODULES.sesion import Sesion
from MODULES.estado import Estado
from MODULES.ordenInspeccion import OrdenInspeccion
from MODULES.estacionSismo import EstacionSismologica
from MODULES.sismografos import Sismografo
from MODULES.motivosTipo import MotivoTipo
from MODULES.Usuario import Usuario
from MODULES.empleado import Empleado

class GestorOrdenDeInspeccion:
    def __init__(self, fechaHoraActual=None, mails=None, observacionCierre=None, ordenesInspeccion=None, sesionActual:Sesion=None):
        self.fechaHoraActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.mails = mails
        self.observacionCierre = observacionCierre
        self.ordenesInspeccion = ordenesInspeccion
        self.sesion = sesionActual

    #Funcion que obtiene los usuarios de la base de datos (mover a usuario.py)
    def obtenerUsuario(self):
        conn = sqlite3.connect('MODULES/database.db')
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
                conn = sqlite3.connect('MODULES/database.db')
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
                self.sesion = Sesion(fechaActual, usuario)
                sesion = self.sesion
                return sesion, 'Sesión iniciada con éxito.'
        return None, 'Usuario o contraseña incorrectos.'
    def buscarEmpleadoLogueado(self):
        return self.sesionActual.obtenerEmpleadoLogeado()
    def obtenerDatos(self, fila, empleado):
        ordenesFiltro = []
        for orden in fila:
            numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, nombreEmpleado, idEstado, codigoES, nombreEstado, nombre, identificadorSismografo = orden
            estado = Estado(idEstado, nombreEstado)
            sismografo = Sismografo(codigoES, identificadorSismografo)  
            estacion = EstacionSismologica(codigoES, nombre, sismografo_obj=sismografo)
            ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, nombreEmpleado, estado, estacion)
            if ordenInspeccion.sosCompletamenteRealizada() == True: # and ordenInspeccion.sosDeEmpleado(empleado) == True:
                ordenesFiltro.append(ordenInspeccion)
        return ordenesFiltro
    def ordenaPorFechaFinalizacion(self, fila):
        ordenesFiltro = self.obtenerDatos(fila)   
        ordenesOrdenadas = sorted(ordenesFiltro, key=lambda o: datetime.strptime(o.getfechaHoraFinalizacion(), "%Y-%m-%d %H:%M:%S"))
        return ordenesOrdenadas