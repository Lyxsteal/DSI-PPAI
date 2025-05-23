import sqlite3
from MODULES.sesion import Sesion
from datetime import datetime
from MODULES.usuario import Usuario
class GestorIS:
    def __init__(self, fechaHoraActual=None, mails=None, observacionCierre=None, ordenesInspeccion=None, sesionActual:Sesion=None):
        self.fechaHoraActual = None
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
                conn.close()
                sesion = Sesion(fechaInicio=fechaActual, fechaFin=None, usuario=Usuario(nombre))
                return sesion, 'Sesión iniciada con éxito.'
        return None, 'Usuario o contraseña incorrectos.'