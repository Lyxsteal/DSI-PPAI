import sqlite3
def buscarOrdenesInspeccion():
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.*, e.nombreEstado, es.nombre, s.identificadorSismografo FROM OrdenesInspeccion o
        JOIN Estados e ON o.idEstado = e.idEstado
        JOIN EstacionesSismologicas es ON o.codigoES = es.codigo
        JOIN Sismografos s ON s.codigoEstacion = es.codigo
    ''')
    ordenes = cursor.fetchall()
    conn.close()
    
    return ordenes if ordenes else ('No hay ordenes de inspeccion')