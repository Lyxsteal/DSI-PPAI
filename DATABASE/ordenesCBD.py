from MODULES.empleado import Empleado
from MODULES.ordenInspeccion import OrdenInspeccion
from MODULES.estado import Estado
from MODULES.estacionSismo import EstacionSismologica
from MODULES.sismografos import Sismografo
from MODULES.cambioEstado import CambioEstado
import sqlite3
def buscarOrdenesInspeccion():
    ordenes_objeto = []
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
    for orden in ordenes:
        numeroOrden, fechaHoraCierre, fechaHoraFinalizacion, fechaHoraInicio, observacion, nombreEmpleado, idEstado, codigoES, nombreEstado, nombreES, idSismografo = orden
        ordenes_objeto.append(OrdenInspeccion(numeroOrden, fechaHoraInicio=None, fechaHoraCierre=None, fechaHoraFinalizacion=fechaHoraFinalizacion, observacionCierre=None,
                                               empleado=Empleado(nombreEmpleado), estado=Estado(idEstado=idEstado, nombre=nombreEstado), estacion=EstacionSismologica(codigoES,nombre= nombreES, sismografo=Sismografo(codigoES,identificadorSismografo=idSismografo,cambioEstado=CambioEstado()))))
            
    return ordenes_objeto if ordenes else ('No hay ordenes de inspeccion')

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