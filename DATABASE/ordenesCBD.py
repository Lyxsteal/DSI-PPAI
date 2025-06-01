import sqlite3
def buscarOrdenesInspeccion():
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.*, e.nombreEstado FROM OrdenesInspeccion o
        JOIN Estados e ON o.idEstado = e.idEstado
    ''')
    ordenes = cursor.fetchall()
    conn.close()
    
    return ordenes if ordenes else ('No hay ordenes de inspeccion')