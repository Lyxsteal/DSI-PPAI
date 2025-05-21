from datetime import datetime
from MODULES.usuario import Usuario
class Sesion:
    def __init__(self, fechaInicio, fechaFin=None, usuario:Usuario=None):
        self.fechaInicio = datetime.now()
        self.fechaFin = fechaFin
        self.usuario = usuario
    
    def obtenerEmpleadoLogeado(self):
        return self.usuario.getNombre()
        