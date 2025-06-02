import sqlite3
from MODULES.empleado import Empleado

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
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Empleados")
    empleados_data = cursor.fetchall()
    conn.close()
    empleados = [Empleado(*data) for data in empleados_data]
    return empleados