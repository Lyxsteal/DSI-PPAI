from datetime import datetime
import sqlite3
from typing import Optional
import os

from MODULES.sesion import Sesion
from MODULES.empleado import Empleado
from MODULES.motivosTipo import MotivoTipo
from MODULES.ordenInspeccion import OrdenInspeccion
from MODULES.estado import Estado
from BOUNDARY.pantallaCCRS import PantallaCCRS
from BOUNDARY.interfazNotificacionEmail import InterfazNotificacionEmail
from MODULES.estacionSismo import EstacionSismologica
from MODULES.sismografos import Sismografo
from MODULES.cambioEstado import CambioEstado

class GestorOrdenDeInspeccion:
    def __init__(self, sesionActual:Sesion, empleado:Optional[Empleado] = None, motivos = None, estado:Optional[Estado] = None, 
                 pantallaCCRS:Optional[PantallaCCRS] = None, interfaz:Optional[InterfazNotificacionEmail] = None , ordenes = None, fechaActual = None, ordenSeleccionada = None, observacion = None):
        self.sesion = sesionActual
        self.empleado = empleado
        self.motivos = motivos
        self.estado = estado
        self.pantallaCCRS = pantallaCCRS
        self.interfaz = interfaz
        self.ordenes = ordenes
        self.fechaActual = fechaActual
        self.ordenSeleccionada = ordenSeleccionada
        self.comentarios = []
        self.observacionCierre = observacion

    def iniciarCierreOrdenInspeccion(self):
        print('Inicio el Cierre de Orden Inspeccion')
        self.empleado = self.buscarEmpleadoLogueado()
        print('Empleado logueado: ' + self.empleado)  # <--- Cambiado aquí
        ordenes = self.buscarOrdenesDeInspeccion()
        ordenes_ordenadas = self.ordenaPorFechaFinalizacion(ordenes)
        self.ordenes = ordenes_ordenadas  
        print('Existen ' + str(len(ordenes_ordenadas)) + ' ordenes con este empleado que están en estado completamente realizadas')
        print('Son las siguientes:')
        for i in ordenes_ordenadas:
            print(i.getNroOrden())

    def buscarEmpleadoLogueado(self):
        return self.sesion.obtenerEmpleadoLogeado()
        
    def buscarOrdenesDeInspeccion(self):
        db_path = os.path.join(os.path.dirname(__file__), '../MODULES/database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.numeroOrden, o.fechaHoraInicio, o.fechaHoraCierre, o.fechaHoraFinalizacion, o.observacionCierre, 
                o.nombreEmpleado, o.idEstado, o.codigoES, e.nombreEstado, es.nombre, s.identificadorSismografo
            FROM OrdenesInspeccion o
            JOIN Estados e ON o.idEstado = e.idEstado
            JOIN EstacionesSismologicas es ON o.codigoES = es.codigo
            JOIN Sismografos s ON o.codigoES = s.codigoEstacion
        ''')
        ordenes = cursor.fetchall()
        conn.close()

        ordenesFiltro = []
        for orden in ordenes:
            numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, nombreEmpleado, idEstado, codigoES, nombreEstado, nombre, identificadorSismografo = orden
            cambioEstado = CambioEstado()
            estado = Estado(idEstado, nombreEstado)
            sismografo = Sismografo(codigoES, identificadorSismografo)
            sismografo.setCambioEstado(cambioEstado)
            estacion = EstacionSismologica(codigoES, nombre, sismografo_obj=sismografo)
            ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio, fechaHoraCierre, fechaHoraFinalizacion, observacionCierre, nombreEmpleado, estado, estacion)
            if self.empleado is not None and ordenInspeccion.sosCompletamenteRealizada() and ordenInspeccion.sosDeEmpleado(self.empleado):
                ordenesFiltro.append(ordenInspeccion)
        return ordenesFiltro
    
    def ordenaPorFechaFinalizacion(self, ordenes):
        ordenesOrdenadas = sorted(ordenes, key=lambda o: datetime.strptime(o.getfechaHoraFinalizacion(), "%Y-%m-%d %H:%M:%S"))
        return ordenesOrdenadas
    
    def tomarOrdenInspeccionSeleccionada(self, orden):
        self.ordenSeleccionada = orden
        return orden

    def pedirObservacionCierreOrden(self):
        pass

    def tomarObservacionCierreOrden(self, observacion):
        self.observacionCierre = observacion
        return observacion
    def buscarMotivoTiposFueraServicio(self):
        lista_motivos = []
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT descripcion FROM MotivosTipo
        ''')
        motivos = cursor.fetchall()
        conn.close()
        for i in motivos:
            descripcion = i
            motivo = MotivoTipo(descripcion)
            motivo.getDescripcion()
            lista_motivos.append(motivo)
        return lista_motivos

    def pedirSeleccionMotivoTipoFueraServicio(self):
        pass

    def tomarMotivoTipoFueraServicio(self, motivos):
        self.motivosSeleccionados = motivos
        return motivos
    def pedirComentario(self):
        pass

    def tomarComentario(self, comentario):
        self.comentarios.append(comentario)
        return self.comentarios
        
    def pedirConfirmacionCierreOrden(self):
        pass

    def tomarConfirmacionCierreOrden(self):
        pass

    def validarExistenciaObservacion(self):
        return bool(self.observacionCierre.strip())

    def validarExistenciaMotivoSeleccionado(self):
        return bool(self.motivosSeleccionados)

    def buscarEstadoCerrada(self):
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT idEstado FROM Estados WHERE nombreEstado = ?", ('Cerrada',))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def getFechaHoraActual(self):
        self.fechaActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.fechaActual
    def buscarFueraDeServicio(self):
        """Devuelve los motivos de fuera de servicio desde la base de datos."""
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT idEstado FROM Estados WHERE nombreEstado = ?", ('Fuera de Servicio'))
        fueraDeServ = cursor.fetchone()
        conn.close()
        return fueraDeServ[0] if fueraDeServ else None

    def cerrarOrdenInspeccion(self, fechaActual, idEstadoFdS, idEstadoCerrada, observacionCierre, ordenSeleccionada, comentario, motivoTipo):
        self.ordenSeleccionada.cerrar(idEstadoCerrada, observacionCierre, ordenSeleccionada)
        self.ponerSismografoFueraEstado(idEstadoFdS, fechaActual, comentario, motivoTipo)

    def ponerSismografoFueraEstado(self, fechaActual, comentario, motivoTipo):
        self.ordenSeleccionada.ponerSismografoFueraServicio(fechaActual, comentario, motivoTipo)
    def buscarResponsablesReparacion(self):
        """Ejemplo: Busca responsables de reparación (puedes adaptar según tu modelo)."""
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Empleados WHERE rol = ?", ('Responsable Reparación',))
        responsables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return responsables

    def enviarMails(self):
        # Simula envío
        print("Enviando email de notificación...")

    def finCU(self):
        print('Fin Caso de Uso')