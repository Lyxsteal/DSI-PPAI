import sqlite3
import asyncio
from MODULES.estado import Estado
from MODULES.ordenInspeccion import OrdenInspeccion
from MODULES.estacionSismo import EstacionSismologica
from MODULES.sismografos import Sismografo
from MODULES.motivosTipo import MotivoTipo
from datetime import datetime

def obtener_orden_desde_db():
    conn = sqlite3.connect('MODULES/database.db')
    cursor = conn.cursor()
    # Consultar orden con join a estado
    cursor.execute('''
        SELECT o.*, e.nombreEstado, es.nombre, sis.identificadorSismografo
        FROM OrdenesInspeccion o
        JOIN Estados e ON o.idEstado = e.idEstado
        JOIN EstacionesSismologicas es ON o.codigoES = es.codigo
        JOIN Sismografos sis ON o.codigoES = sis.codigoEstacion
    ''')
    filas = cursor.fetchall()
    conn.close()
    return filas
"""     for orden in fila:
        numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, idEstado, nombreEstado = orden
        estado = Estado(idEstado, nombreEstado)
        ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, estado)
        ordenes.append(ordenInspeccion)"""

fila = obtener_orden_desde_db()
def obtenerOrdenesRealizadas(fila):
    ordenesFiltro = []
    id_buscada = int(input('La id que busca es: '))

    for orden in fila:
        numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, idEstado, codigoES, nombreEstado, nombre, identificadorSismografo = orden
        estado = Estado(idEstado, nombreEstado)
        sismografo = Sismografo(codigoES, identificadorSismografo)  
        estacion = EstacionSismologica(codigoES, nombre, sismografo_obj=sismografo)
        ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, estado, estacion)   
        if ordenInspeccion.sosCompletamenteRealizada(id_buscada) == True:
            ordenesFiltro.append(ordenInspeccion)
            
    ordenesOrdenadas = sorted(ordenesFiltro, key=lambda o: datetime.strptime(o.getfechaHoraFinalizacion(), "%Y-%m-%d %H:%M:%S"))
    print("Órdenes ordenadas por Fecha de Finalización:")
    for orden in ordenesOrdenadas:
        print(orden.getNroOrden(), orden.getfechaHoraFinalizacion(), orden.getIdentificadorSismografo(), orden.getNombreEstacion())

    return ordenesOrdenadas, fila
obtenerOrdenesRealizadas(fila)
def obtenerMotivosTipo():
    conn = sqlite3.connect('MODULES/database.db')
    cursor = conn.cursor()
    # Consultar motivos y tipos de orden
    cursor.execute("SELECT descripcion FROM MotivosTipo")
    filas = cursor.fetchall()
    conn.close()
    return filas
motivos = obtenerMotivosTipo()
def buscarMotivosTipoFueraServicio(motivos):
    motivosTipo = []
    for motivo in motivos:
        descripcion = motivo
        motivo = MotivoTipo(descripcion)
        motivosTipo.append(motivo)
        #print('Motivo: ', motivo.getDescripcion())
    for motivo in motivosTipo:
        print('Motivo: ', motivo.getDescripcion())
    return motivosTipo
buscarMotivosTipoFueraServicio(motivos)

#debe comprobar que sea ambito "OrdenInspeccion" y estado "cerrada"
def obtenerEstado():
    conn = sqlite3.connect('MODULES/database.db')
    cursor = conn.cursor()
    # Consultar orden con join a estado
    cursor.execute('''
        SELECT *
        FROM Estados
    ''')
    filas = cursor.fetchall()
    conn.close()
    return filas
estados = obtenerEstado()
def buscarEstadoFueraSismo(estados):
    estadosSismo = []
    for fila in estados:
        nombreEstado, ambito, idEstado = fila
        estado = Estado(idEstado, nombreEstado, ambito)
        if estado.sosAmbitoSismografo() == True:
            estadosSismo.append(estado)
    for estado in estadosSismo:
        if estado.sosFueradeServicio() == True:
            print('Existe')
    return estado
    
def buscarEstadoCerradaOrden(estados):
    estadosOrden = []
    for fila in estados:
        nombreEstado, ambito, idEstado = fila
        estado = Estado(idEstado, nombreEstado, ambito)
        if estado.sosAmbitoOrdenInspeccion() == True:
            estadosOrden.append(estado)
    for estado in estadosOrden:
            if estado.sosCerrada() == True:
                print('Existe')        
    return estado
buscarEstadoCerradaOrden(estados)
buscarEstadoFueraSismo(estados)

def getOrdenInspeccion():
    conn = sqlite3.connect('MODULES/database.db')
    cursor = conn.cursor()
    # Consultar orden con join a estado
    cursor.execute('''
        SELECT * FROM OrdenesInspeccion
    ''')
    filas = cursor.fetchall()
    conn.close()
    return filas
def cerrarOrdenInspeccion(filas):
    for fila in filas:
        numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, idEstado, codigoES = fila
        estado = Estado(idEstado)
        estacion = EstacionSismologica(codigoES)
        ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, estado, estacion)
        if ordenInspeccion.getIdEstado() == 1:

    return ordenInspeccion