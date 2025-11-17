import sqlite3
from MODULES.empleado import Empleado
from MODULES.rol import Rol
def obtenerEmpleado(nombre):
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT empleado FROM Usuario WHERE nombre = ?''', (nombre,))
        empleado = cursor.fetchone()
        empleado_nombre = empleado[0]
        conn.commit()
        conn.close()
        return empleado_nombre

def obtenerEmpleadosTodos():
    empleadosTodos_objetos = []
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Empleados")
    empleados = cursor.fetchall()
    conn.close()
    for empleado in empleados:
        nombre, apellido, mail, telefono, idEmpleado, rol = empleado
        empleadosTodos_objetos.append(Empleado(nombre, apellido, mail, telefono, idEmpleado, rol=Rol(descripcion=None, rol=rol)))
    return empleadosTodos_objetos
