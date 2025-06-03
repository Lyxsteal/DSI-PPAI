from MODULES.motivoFueraServicio import MotivoFueraServicio
from MODULES.motivosTipo import MotivoTipo
import sqlite3
def insertMotivoFS(fechaActual, comentario, motivo):
    try:
            print(f'[DEBUG] Insertando MotivoFueraServicio con comentario: {comentario}, motivoTipo: {motivo}')
            conn = sqlite3.connect('DATABASE/database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO MotivosFueraServicio(fechaInicio, comentario, descripcion) VALUES(?,?,?)''',(fechaActual, comentario, motivo))
            conn.commit()
            conn.close()
            MotivoFueraServicio(comentario, motivoTipo=MotivoTipo(motivo))
    except sqlite3.Error as e:
        print(f"[ERROR] Falló el INSERT en MotivosFueraServicio: {e}")