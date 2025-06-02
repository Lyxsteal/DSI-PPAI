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
from tkinter import messagebox
from DATABASE.estadoCBD import estadoConsulta
from DATABASE.ordenesCBD import buscarOrdenesInspeccion

class GestorOrdenDeInspeccion:
    def __init__(self, sesionActual:Sesion, empleado:Optional[Empleado] = None, motivos = None, estado:Optional[Estado] = None, 
                 pantallaCCRS:Optional[PantallaCCRS] = None, interfaz:Optional[InterfazNotificacionEmail] = None , ordenes = None, fechaActual = None, ordenSeleccionada = None, observacion = None):
        self.sesion = sesionActual
        self.empleado = empleado
        self.motivos = motivos
        self.estado = estado
        self.pantallaCCRS = PantallaCCRS()
        self.interfaz = InterfazNotificacionEmail()
        self.ordenes = ordenes
        self.fechaActual = fechaActual
        self.ordenSeleccionada = ordenSeleccionada
        self.comentarios = None
        self.observacionCierre = observacion
        self.ambitoOI = None
        self.ambitoSismografo = None
        self.existeCerrada = None
        self.idCerrada = None
        self.idFDS = None
        self.motivosSeleccionados = None
        self.diccOrdenesInspeccion = {}

    def iniciarCierreOrdenInspeccion(self):
        print('Inicio el Cierre de Orden Inspeccion')
        self.buscarEmpleadoLogueado()

    def buscarEmpleadoLogueado(self):
        empleado_actual = self.sesion.obtenerEmpleadoLogeado()
        self.buscarOrdenesDeInspeccion(empleado_actual)
        
    def buscarOrdenesDeInspeccion(self, empleado_actual):
        ordenes = buscarOrdenesInspeccion()
        ordenesFiltroDatos = []
        ordenesFiltroObjetos = []
        for orden in ordenes:
            numeroOrden, fechaHoraCierre, fechaHoraFinalizacion, fechaHoraInicio, observacion, nombreEmpleado, idEstado, codigoES, nombreEstado, nombreES, idSismografo = orden
            self.ordenInspeccion = OrdenInspeccion(numeroOrden, fechaHoraInicio=None, fechaHoraCierre=None, fechaHoraFinalizacion=fechaHoraFinalizacion, observacionCierre=None,
                                               empleado=Empleado(nombreEmpleado), estado=Estado(idEstado=idEstado, nombre=nombreEstado), estacion=EstacionSismologica(codigoES,nombre= nombreES, sismografo=Sismografo(codigoES,identificadorSismografo=idSismografo,cambioEstado=CambioEstado())))
            if self.ordenInspeccion.sosDeEmpleado(empleado_actual) is True and self.ordenInspeccion.sosCompletamenteRealizada() is True:
                    nroOrden, fechaHoraFinalizacion, nombreEstacion, idSismografo = self.ordenInspeccion.obtenerDatos()
                    ordenesFiltroDatos.append([nroOrden, fechaHoraFinalizacion, nombreEstacion, idSismografo])
                    ordenesFiltroObjetos.append(self.ordenInspeccion)
                    self.diccOrdenesInspeccion[nroOrden] = self.ordenInspeccion
        print(self.diccOrdenesInspeccion)
        self.ordenaPorFechaFinalizacion(ordenesFiltroDatos)
    
    def ordenaPorFechaFinalizacion(self, ordenes):
        ordenesOrdenadas = sorted(ordenes, key=lambda o: datetime.strptime(o[1], "%Y-%m-%d %H:%M:%S"))
        self.ordenes = ordenesOrdenadas
        return self.ordenes
    
    def tomarOrdenInspeccionSeleccionada(self, orden):
        self.ordenSeleccionada = self.diccOrdenesInspeccion[orden[0]]
        return orden

    def pedirObservacionCierreOrden(self):
        pass

    def tomarObservacionCierreOrden(self, observacion):
        self.observacionCierre = observacion
        return observacion
    
    def buscarMotivoTiposFueraServicio(self):
        lista_motivos = []
        conn = sqlite3.connect('DATABASE/database.db')
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

    def tomarComentario(self, comentario_por_motivo):
        self.comentarios = comentario_por_motivo
        return self.comentarios
        
    def pedirConfirmacionCierreOrden(self):
        print("UI: Pidiendo confirmación final para cerrar la orden.")
        return messagebox.askyesno("Confirmar Cierre", "¿Está seguro de que desea cerrar esta orden de inspección?")


    def tomarConfirmacionCierreOrden(self, ordenSelec, observacion, motivos):
        print(observacion)
        print(motivos)
        self.tomarOrdenInspeccionSeleccionada(ordenSelec)
        self.observacionCierre = self.validarExistenciaObservacion(observacion)
        if self.observacionCierre is None:
            return
        self.motivosSeleccionados = self.validarExistenciaMotivoSeleccionado(motivos)
        if self.motivosSeleccionados is None:
            return
        self.buscarEstadoCerrada()
        return True
            

    def validarExistenciaObservacion(self, observacion):
        observacion = observacion.strip()
        if observacion == "":
            messagebox.showerror("Error", "Debe ingresar una observación.")
            return
        else:
            return observacion

    def validarExistenciaMotivoSeleccionado(self, motivos):
        motivosSeleccionados = motivos
        if len(motivosSeleccionados) == 0:
            messagebox.showerror("Error", "Debe seleccionar al menos un motivo.")
            return 
        else:
            return motivosSeleccionados
    def buscarEstadoCerrada(self):
        estados = estadoConsulta()
        for estado in estados:
            nombreEstado, ambito, idEstado = estado
            self.estado = Estado(idEstado, ambito, nombreEstado)
            self.ambitoOI = self.estado.sosAmbitoOrdenInspeccion()
            if self.ambitoOI is True:
                break
        if self.ambitoOI is False:
            messagebox.showerror("Error", "No se pudo encontrar el ambito 'Orden Inspeccion'.")
            exit()
        for estado in estados:
            nombreEstado, ambito, idEstado = estado
            self.estado = Estado(idEstado, ambito, nombreEstado)
            self.existeCerrada, self.idCerrada = self.estado.sosCerrada()
            if self.existeCerrada is True:
                self.getFechaHoraActual(estados)
                break
        else:
            messagebox.showerror("Error", "No se pudo encontrar el estado 'Cerrada'.")
            exit()

    
    def getFechaHoraActual(self, estados):
        self.fechaActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.buscarFueraDeServicio(estados)

    def buscarFueraDeServicio(self, estados):
        for estado in estados:
            nombreEstado, ambito, idEstado = estado
            self.estado = Estado(idEstado, ambito, nombreEstado)
            self.ambitoSis = self.estado.sosAmbitoSismografo()
            if self.ambitoSis == True:
                break
        if self.ambitoSis is False:
            messagebox.showerror("Error", "No se pudo encontrar el ambito 'Sismografo'.")
            exit()
        for estado in estados:
            nombreEstado, ambito, idEstado = estado
            self.estado = Estado(idEstado, ambito, nombreEstado)
            self.idFDS = self.estado.sosFueraDeServicio()
            if self.idFDS is True:
                break
        if self.idFDS is False:
            messagebox.showerror("Error", "No se pudo encontrar el estado 'Fuera de Servicio'.")
            exit()
        self.cerrarOrdenInspeccion(self.fechaActual, self.idFDS, self.idCerrada, self.observacionCierre, self.ordenSeleccionada, self.comentarios, self.motivosSeleccionados)
                

    def cerrarOrdenInspeccion(self, fechaActual, idEstadoFdS, idCerrada, observacionCierre, ordenSeleccionada, comentario, motivoTipo):
        print(idCerrada, observacionCierre, ordenSeleccionada)
        self.ordenSeleccionada.cerrar(self.idCerrada, observacionCierre, ordenSeleccionada)
        self.ponerSismografoFueraEstado(idEstadoFdS, fechaActual, comentario, motivoTipo)

    def ponerSismografoFueraEstado(self, idEstadoFdS, fechaActual, comentario, motivoTipo):
        self.ordenSeleccionada.ponerSismografoFueraServicio(idEstadoFdS, fechaActual, comentario, motivoTipo)

    def buscarResponsablesReparacion(self):
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Empleados")
        self.mails_responsables = []
        for row in cursor.fetchall():
            empleado = Empleado(row[0])
            if empleado.esResponsableReparacion():
                self.mails_responsables.append(empleado.obtenerMail())
        conn.close()

    def enviarMails(self):
        # Simula envío
        # Teniendo los mails en self.mails_responsables
        print("Enviando email de notificación...")
        self.interfaz.enviarNotificacion()
        self.pantallaCCRS.publicarNotificacion()

    def finCU(self):
        print('Fin Caso de Uso')