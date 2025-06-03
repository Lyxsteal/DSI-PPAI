from MODULES.empleado import Empleado
from DATABASE.empleadoCBD import obtenerEmpleado
import sqlite3

class Usuario:
    def __init__(self, nombre, contraseña=None, empleado:Empleado=None):
        self.__nombre = nombre
        self.__contraseña = contraseña
        self.__empleado = empleado
    
    def obtenerEmpleado(self):
        return self.__empleado.obtenerNombre()
    
    def getNombre(self):
        return self.__nombre
    
    def getNombreEmpleado(self):
        empleado_nombre = self.obtenerEmpleado
        return empleado_nombre
    
    def obtenerEmpleado(self):
        self.__empleado = obtenerEmpleado(self.__nombre)
        return self.__empleado
    
    def getNombre(self):
        return self.__nombre