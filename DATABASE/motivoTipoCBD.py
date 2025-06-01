import sqlite3

def obtenerMotivoTipo():
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT descripcion FROM MotivosTipo''')
    motivos = cursor.fetchall()
    conn.close()
    return motivos