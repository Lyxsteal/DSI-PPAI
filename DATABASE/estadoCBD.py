from MODULES.estado import Estado
import sqlite3
def estadoConsulta():
    estados_objetos = []
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Estados")
    estados = cursor.fetchall()
    conn.close()
    for estado in estados:
        nombreEstado, ambito, idEstado = estado
        estados_objetos.append(Estado(idEstado, ambito, nombreEstado))
    return estados_objetos if estados else None
def idCompletamenteRealizada():
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT idEstado FROM Estados WHERE nombreEstado = 'Completamente Realizada'")
    idEstadoCR = cursor.fetchall()
    conn.close()
    return idEstadoCR
def setEstadoCierre(fechaCierre, observacionCierre, idEstado, ordenSeleccionada):
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute('''
            UPDATE OrdenesInspeccion
            SET fechaHoraCierre = ?, observacionCierre = ?, idEstado = ?
            WHERE numeroOrden = ?
        ''', (fechaCierre, observacionCierre, idEstado, ordenSeleccionada))
    conn.commit()
    conn.close()