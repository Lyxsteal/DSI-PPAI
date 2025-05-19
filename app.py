from flask import Flask, jsonify
from flask_cors import CORS  
import sqlite3
from MODULES.estado import Estado
from MODULES.ordenInspeccion import OrdenInspeccion
from MODULES.estacionSismo import EstacionSismologica
from MODULES.sismografos import Sismografo
from MODULES.modules import obtenerOrdenesRealizadas, obtener_orden_desde_db
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 2. Habilita CORS para la app


def db_obtener_todas_las_ordenes():
    # ... (tu lógica para obtener órdenes)
    filas = obtener_orden_desde_db()
    ordenesRealizadas = obtenerOrdenesRealizadas(filas)
    ordenes = []
    for fila in ordenesRealizadas:
        
        ordenes.append({
            "numeroOrden": fila[0], "fechaHoraInicio": fila[1], "fechaHoraCierre": fila[2],
            "fechaHoraFinalizacion": fila[3], "observacionCierre": fila[4], "idEmpleado": fila[5],
            "idEstado": fila[6], "codigoES": fila[7], "nombreEstado": fila[8],
            "nombreEstacion": fila[9], "identificadorSismografo": fila[10]
        })
    return ordenes

def db_obtener_ordenes_por_estado(id_estado_buscado):
    conn = sqlite3.connect('MODULES/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.numeroOrden, o.fechaHoraInicio, o.fechaHoraCierre, o.fechaHoraFinalizacion, 
               o.observacionCierre, o.idEmpleado, o.idEstado, o.codigoES,
               e.nombreEstado, es.nombre, sis.identificadorSismografo
        FROM OrdenesInspeccion o
        JOIN Estados e ON o.idEstado = e.idEstado
        JOIN EstacionesSismologicas es ON o.codigoES = es.codigo
        JOIN Sismografos sis ON o.codigoES = sis.codigoEstacion
    ''')
    filas = cursor.fetchall()
    conn.close()

    ordenes_filtro = []
    for datos_orden in filas:
        numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, idEstado, codigoES, nombreEstado, nombreEstacion, identificadorSismografo = datos_orden
        estado_obj = Estado(idEstado, nombreEstado)
        sismografo_obj = Sismografo(codigoEstacion=codigoES, identificadorSismografo=identificadorSismografo)
        estacion_obj = EstacionSismologica(codigo=codigoES, nombre=nombreEstacion, sismografo_obj=sismografo_obj)
        orden_inspeccion_obj = OrdenInspeccion(
            numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion,
            observacionCierre, idEmpleado, estado_obj, estacion_obj
        )
        if orden_inspeccion_obj.sosCompletamenteRealizada(id_estado_buscado):
            ordenes_filtro.append({
                "numeroOrden": orden_inspeccion_obj.getNroOrden(),
                "fechaHoraFinalizacion": orden_inspeccion_obj.getfechaHoraFinalizacion(),
                "identificadorSismografo": orden_inspeccion_obj.getIdentificadorSismografo(),
                "nombreEstacion": orden_inspeccion_obj.getNombreEstacion()
            })
    ordenes_ordenadas = sorted(
        ordenes_filtro,
        key=lambda o: datetime.strptime(o['fechaHoraFinalizacion'], "%Y-%m-%d %H:%M:%S") if o['fechaHoraFinalizacion'] else datetime.min
    )
    return ordenes_ordenadas

def obtenerTodasOrdenesComoObjetos(filas):
    ordenes = []
    for orden in filas:
        numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, idEstado, codigoES, nombreEstado, nombre, identificadorSismografo = orden
        estado = Estado(idEstado, nombreEstado)
        sismografo = Sismografo(codigoES, identificadorSismografo)  
        estacion = EstacionSismologica(codigoES, nombre, sismografo_obj=sismografo)
        ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, idEmpleado, estado, estacion)
        ordenes.append(ordenInspeccion)
    return ordenes

def db_obtener_motivos_tipo():
    conn = sqlite3.connect('MODULES/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion FROM MotivosTipo")
    motivos_raw = cursor.fetchall()
    conn.close()
    return [descripcion[0] for descripcion in motivos_raw]

@app.route('/')
def home():
    return "La API está corriendo correctamente"

@app.route('/api/ordenes', methods=['GET'])
def get_todas_las_ordenes_api(): # Renombrada para evitar colisión si se importa todo de otro script
    ordenes = obtenerTodasOrdenesComoObjetos()
    return jsonify(ordenes) //
@app.route('/api/ordenes/realizadas/<int:id_estado>', methods=['GET'])
def get_ordenes_completadas_api(id_estado): # Renombrada
    ordenes = db_obtener_ordenes_por_estado(id_estado)
    print(ordenes)
    return jsonify(ordenes)

@app.route('/api/motivos', methods=['GET'])
def get_motivos_api(): # Renombrada
    motivos = db_obtener_motivos_tipo()
    return jsonify(motivos)



if __name__ == '__main__':
    app.run(debug=True) # Flask se ejecutará por defecto en http://127.0.0.1:5000/
