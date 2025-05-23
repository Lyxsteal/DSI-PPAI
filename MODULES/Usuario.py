from MODULES.empleado import Empleado
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
        print('metodo llamado')
        empleado_nombre = None
        nombre= self.getNombre()
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT empleado FROM Usuario WHERE nombre = ?''', (nombre,))
        empleado = cursor.fetchone()
        empleado_nombre = empleado[0]
        print(empleado_nombre)
        conn.commit()
        conn.close()
        return empleado_nombre
    def getNombre(self):
        return self.nombre