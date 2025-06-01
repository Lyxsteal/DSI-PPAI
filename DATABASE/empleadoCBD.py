import sqlite3
def obtenerEmpleado(nombre):
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT empleado FROM Usuario WHERE nombre = ?''', (nombre,))
        empleado = cursor.fetchone()
        empleado_nombre = empleado[0]
        conn.commit()
        conn.close()
        return empleado_nombre