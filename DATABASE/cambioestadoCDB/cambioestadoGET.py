import sqlite3
from datetime import datetime
from MODULES.cambioEstado import CambioEstado
from MODULES.estado import Estado
from MODULES.motivoFueraServicio import MotivoFueraServicio
from MODULES.motivosTipo import MotivoTipo
def getCambiosEstado(idSismografo):
        cambiosEstado_objetos = []
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM CambiosEstado WHERE idSismografo= ?''',(idSismografo,) )
        cambiosEstado = cursor.fetchall()
        conn.close()
        if cambiosEstado is None:
            print(f"No se encontró cambio de estado para el sismografo seleccionado")
        print(cambiosEstado)
        for cambio in cambiosEstado:
            fechaHoraInicio, fechaHoraFin, idSismografo, idEstado = cambio
            cambiosEstado_objetos.append(CambioEstado(fechaHoraInicio, fechaHoraFin, estado=Estado(idEstado=idEstado), idSismografo=idSismografo))
        return cambiosEstado_objetos
def insertCambioEstado(fechaActual, identificadorSismografo, idEstadoFdS, comentarios_por_motivo, motivoTipo):
        try:
            conn = sqlite3.connect('DATABASE/database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CambiosEstado (fechaHoraInicio, fechaHoraFin, idSismografo, idEstado) VALUES(?,?,?,?)",(fechaActual, None, identificadorSismografo, idEstadoFdS))
            conn.commit()
            conn.close()
            CambioEstado(fechaHoraInicio= fechaActual, fechaHoraFin= None, estado= Estado(idEstado=idEstadoFdS), idSismografo= identificadorSismografo, 
                         motivoFS = comentarios_por_motivo)
        except sqlite3.Error as e:
            print(f"[ERROR] Falló el INSERT en CambiosEstado: {e}")