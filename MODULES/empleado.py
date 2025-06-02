from MODULES.rol import Rol

class Empleado:
    def __init__(self, nombre=None, apellido=None, mail=None, telefono=None, idEmpleado=None, rol:Rol= None):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__mail = mail
        self.__telefono = telefono
        self.__idEmpleado = idEmpleado
        self.__rol = rol

    def obtenerNombre(self):
        return self.__nombre
    
    def obtenerTelefono(self):
        return self.__telefono
    
    def esResponsableReparacion(self):
        return self.__rol.esResponsableReparacion()
    
    def obtenerMail(self):
        return self.__mail
    
    def sosDeEmpleado(self, empleado_actual):
        if self.__nombre == empleado_actual:
            return True
        else:
            return False