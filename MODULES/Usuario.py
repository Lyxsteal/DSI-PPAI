from MODULES.empleado import Empleado
class Usuario:
    def __init__(self, nombre, contraseña, empleado:Empleado):
        self.nombre = nombre
        self.contraseña = contraseña
        self.__empleado = empleado
    
    def obtenerEmpleado(self):
        return self.__empleado.obtenerNombre()
    def getNombre(self):
        return self.nombre