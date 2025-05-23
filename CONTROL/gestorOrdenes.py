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

class GestorOrdenDeInspeccion:
    def __init__(self, sesionActual:Sesion, empleado:Optional[Empleado] = None, motivoTipo:Optional[MotivoTipo] = None, estado:Optional[Estado] = None, 
                 pantallaCCRS:Optional[PantallaCCRS] = None, interfaz:Optional[InterfazNotificacionEmail] = None , ordenes = None):
        self.sesion = sesionActual
        self.empleado = empleado
        self.motivoTipo = motivoTipo
        self.estado = estado
        self.pantallaCCRS = pantallaCCRS
        self.interfaz = interfaz
        self.empleado = None
        self.ordenes = None

    def iniciarCierreOrdenInspeccion(self):
        print('Inicio el Cierre de Orden Inspeccion')
        self.empleado = self.buscarEmpleadoLogueado()
        empleado_log = self.sesion.obtenerEmpleadoLogeado()
        print('Empleado logueado: ' + empleado_log)  # <--- Cambiado aquí
        ordenes = self.ordenaPorFechaFinalizacion(self.buscarOrdenesDeInspeccion())
        self.ordenes = ordenes  
        print('Existen ' + str(len(ordenes)) + ' ordenes con este empleado que están en estado completamente realizadas')
        print('Son las siguientes:')
        for i in ordenes:
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
            estado = Estado(idEstado, nombreEstado)
            sismografo = Sismografo(codigoES, identificadorSismografo)
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

    def pedirObservacionCierreOrden(self):
        pass

    def tomarObservacionCierreOrden(self, observacion):
        self.observacionCierre = observacion

    def buscarMotivoTiposFueraServicio(self):
        pass

    def pedirSeleccionMotivoTipoFueraServicio(self):
        pass

    def tomarMotivoTipoFueraServicio(self, motivos):
        self.motivosSeleccionados = motivos
    
    def pedirComentario(self):
        pass

    def tomarComentario(self, comentario):
        self.comentario = comentario

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
        """Devuelve la fecha y hora actual en formato string."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def buscarFueraDeServicio(self):
        """Devuelve los motivos de fuera de servicio desde la base de datos."""
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombreMotivo FROM MotivosFueraServicio")
        motivos = [row[0] for row in cursor.fetchall()]
        conn.close()
        return motivos

    def cerrarOrdenInspeccion(self, idEstado):
        if not self.ordenSeleccionada:
            print("No hay orden seleccionada.")
            return
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        fecha_cierre = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            UPDATE OrdenesInspeccion
            SET fechaHoraCierre = ?, observacionCierre = ?, idEstado = ?
            WHERE numeroOrden = ?
        ''', (fecha_cierre, self.observacionCierre, idEstado, self.ordenSeleccionada.getNroOrden()))
        conn.commit()
        conn.close()
        print(f"Orden {self.ordenSeleccionada.getNroOrden()} cerrada correctamente.")

    def ponerSismografoFueraEstado(self):
        """Ejemplo: Cambia el estado del sismógrafo a fuera de servicio."""
        if not self.ordenSeleccionada:
            print("No hay orden seleccionada para poner fuera de servicio.")
            return
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        # Suponiendo que hay un campo 'estado' en la tabla Sismografos
        cursor.execute('''
            UPDATE Sismografos
            SET estado = ?
            WHERE identificadorSismografo = ?
        ''', ('Fuera de Servicio', self.ordenSeleccionada.getIdentificadorSismografo()))
        conn.commit()
        conn.close()
        print(f"Sismógrafo {self.ordenSeleccionada.getIdentificadorSismografo()} puesto fuera de servicio.")

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
        print(f"Motivos: {self.motivosSeleccionados}")
        print(f"Comentario: {self.comentario}")

    def finCU(self):
        print('Fin Caso de Uso')