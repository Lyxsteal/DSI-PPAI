class Empleado:
    def __init__(self, nombre, apellido, mail, telefono, idEmpleado):
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.telefono = telefono
        self.idEmpleado = idEmpleado
    
    def obtenerNombre(self):
        return self.nombre
    
    def obtenerTelefono(self):
        return self.telefono
    