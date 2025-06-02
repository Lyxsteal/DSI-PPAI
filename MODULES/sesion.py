from datetime import datetime
from MODULES.Usuario import Usuario
class Sesion:
    def __init__(self, fechaInicio, fechaFin=None, usuario:Usuario=None):
        self.__fechaInicio = datetime.now()
        self.__fechaFin = fechaFin
        self.__usuario = usuario
    
    def obtenerEmpleadoLogeado(self):
        return self.__usuario.obtenerEmpleado()
        