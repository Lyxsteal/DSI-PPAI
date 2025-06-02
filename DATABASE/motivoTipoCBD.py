import sqlite3
from MODULES.motivosTipo import MotivoTipo
def obtenerMotivoTipo():
    motivos_objetos = []
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT descripcion FROM MotivosTipo''')
    motivos = cursor.fetchall()
    conn.close()
    for motivo in motivos:
        descripcion = motivo
        motivos_objetos.append(MotivoTipo(descripcion))
    return motivos_objetos