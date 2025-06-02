from MODULES.rol import Rol

class Empleado:
    def __init__(self, nombre=None, apellido=None, mail=None, telefono=None, idEmpleado=None, rol:Rol= Rol("Responsable de Reparación")):
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.telefono = telefono
        self.idEmpleado = idEmpleado
        self.rol = rol

    def obtenerNombre(self):
        return self.nombre
    
    def obtenerTelefono(self):
        return self.telefono
    
    def esResponsableReparacion(self):
        return self.rol.esResponsableReparacion()
    
    def obtenerMail(self):
        return self.mail
    
    def sosDeEmpleado(self, empleado_actual):
        if self.nombre == empleado_actual:
            return True
        else:
            return False