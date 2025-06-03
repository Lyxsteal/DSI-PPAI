import sqlite3
def setFechaHoraFin(tiempoFin, idSismografo, fechaHoraInicio):
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE CambiosEstado
            SET fechaHoraFin = ?
            WHERE idSismografo = ? AND fechaHoraInicio = ?''',(tiempoFin, idSismografo, fechaHoraInicio))
        conn.commit()
        conn.close()