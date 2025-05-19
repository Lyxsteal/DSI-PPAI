import sqlite3
def conexionBD():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    return conexion, cursor