from MODULES.empleado import Empleado
from DATABASE.empleadoCBD import obtenerEmpleado
import sqlite3
class Usuario:
    def __init__(self, nombre, contraseña=None, empleado:Empleado=None):
        self.nombre = nombre
        self.contraseña = contraseña
        self.empleado = empleado
    
    def obtenerEmpleado(self):
        return self.empleado.obtenerNombre()
    
    def getNombre(self):
        return self.nombre
    
    def getNombreEmpleado(self):
        empleado_nombre = self.obtenerEmpleado
        return empleado_nombre
    
    def obtenerEmpleado(self):
        self.empleado = obtenerEmpleado(self.nombre)
        return self.empleado
    def getNombre(self):
        return self.nombre