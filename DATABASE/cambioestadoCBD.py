import sqlite3
from datetime import datetime
def getCambiosEstado(idSismografo):
        cambiosEstado = []
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM CambiosEstado WHERE idSismografo= ?''',(idSismografo,) )
        cambiosEstado = cursor.fetchall()
        conn.close()
        if cambiosEstado is None:
            print(f"No se encontró cambio de estado para el sismografo seleccionado")
        return cambiosEstado
def setFechaHoraFin(tiempoFin, idSismografo, fechaHoraInicio):
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE CambiosEstado
            SET fechaHoraFin = ?
            WHERE idSismografo = ? AND fechaHoraInicio = ?''',(tiempoFin, idSismografo, fechaHoraInicio))
        conn.commit()
        conn.close()
def insertCambioEstado(fechaActual, identificadorSismografo, idEstadoFdS):
        try:
            conn = sqlite3.connect('DATABASE/database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CambiosEstado (fechaHoraInicio, fechaHoraFin, idSismografo, idEstado) VALUES(?,?,?,?)",(fechaActual, None, identificadorSismografo, idEstadoFdS))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"[ERROR] Falló el INSERT en CambiosEstado: {e}")