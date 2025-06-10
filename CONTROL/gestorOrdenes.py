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
from DATABASE.motivoTipoCBD import obtenerMotivoTipo
from DATABASE.empleadoCBD import obtenerEmpleadosTodos

class GestorOrdenDeInspeccion:
    def __init__(self, sesionActual:Sesion, empleado:Optional[Empleado] = None, motivos = None, estado:Optional[Estado] = None, 
                 pantallaCCRS:Optional[PantallaCCRS] = None, interfaz:Optional[InterfazNotificacionEmail] = None , ordenes = None, fechaActual = None, ordenSeleccionada = None, observacion = None, orden:OrdenInspeccion=None):
        self.__sesion = sesionActual
        self.__empleado = empleado
        self.__motivos = motivos
        self.__estado = estado
        self.__pantallaCCRS = PantallaCCRS()
        self.__interfaz = InterfazNotificacionEmail()
        self.__ordenes = ordenes
        self.__fechaActual = fechaActual
        self.__ordenSeleccionada = ordenSeleccionada
        self.__comentarios = None
        self.__observacionCierre = observacion
        self.__ambitoOI = None
        self.__ambitoSismografo = None
        self.__existeCerrada = None
        self.__idCerrada = None
        self.__idFDS = None
        self.__motivosSeleccionados = None
        self.__diccOrdenesInspeccion = {}
        self.__ordenInspeccion = orden
        self.__mails_responsables = []

    def iniciarCierreOrdenInspeccion(self):
        print('Inicio el Cierre de Orden Inspeccion')
        self.buscarEmpleadoLogueado()

    def buscarEmpleadoLogueado(self):
        empleado_actual = self.__sesion.obtenerEmpleadoLogeado()
        self.buscarOrdenesDeInspeccion(empleado_actual)
        
    def buscarOrdenesDeInspeccion(self, empleado_actual):
        ordenes_objetos = buscarOrdenesInspeccion()
        ordenesFiltroDatos = []
        ordenesFiltroObjetos = []
        for orden in ordenes_objetos:
            self.__ordenInspeccion = orden 
            if self.__ordenInspeccion.sosDeEmpleado(empleado_actual) is True and self.__ordenInspeccion.sosCompletamenteRealizada() is True:
                    nroOrden, fechaHoraFinalizacion, nombreEstacion, idSismografo = self.__ordenInspeccion.obtenerDatos()
                    ordenesFiltroDatos.append([nroOrden, fechaHoraFinalizacion, nombreEstacion, idSismografo])
                    ordenesFiltroObjetos.append(orden)
                    self.__diccOrdenesInspeccion[nroOrden] = self.__ordenInspeccion
        self.ordenarPorFechaFinalizacion(ordenesFiltroDatos)
    
    def ordenarPorFechaFinalizacion(self, ordenes):
        ordenesOrdenadas = sorted(ordenes, key=lambda o: datetime.strptime(o[1], "%Y-%m-%d %H:%M:%S"))
        self.__ordenes = ordenesOrdenadas
        return self.__ordenes
    
    def tomarOrdenInspeccionSeleccionada(self, orden):
        self.__ordenSeleccionada = self.__diccOrdenesInspeccion[orden[0]]
        return orden

    def pedirObservacionCierreOrden(self):
        pass

    def tomarObservacionCierreOrden(self, observacion):
        self.__observacionCierre = observacion
        return observacion
    
    def buscarMotivoTiposFueraServicio(self):
        lista_motivos = []
        motivos_objetos = obtenerMotivoTipo()
        for motivo in motivos_objetos:
            self.__motivos = motivo
            motivo.getDescripcion()
            lista_motivos.append(motivo)
        return lista_motivos

    def tomarMotivoTipoFueraServicio(self, motivos):
        self.__motivosSeleccionados = motivos
        return motivos

    def tomarComentario(self, comentario_por_motivo):
        self.__comentarios = comentario_por_motivo
        return self.__comentarios
        
    def pedirConfirmacionCierreOrden(self):
        print("UI: Pidiendo confirmación final para cerrar la orden.")
        return messagebox.askyesno("Confirmar Cierre", "¿Está seguro de que desea cerrar esta orden de inspección?")

    def tomarConfirmacionCierreOrden(self, ordenSelec, observacion, motivos):
        print('Observacion: ', observacion)
        print('Motivos:', motivos)
        self.tomarOrdenInspeccionSeleccionada(ordenSelec)
        self.__observacionCierre = self.validarExistenciaObservacion(observacion)
        if self.__observacionCierre is None:
            return
        self.__motivosSeleccionados = self.validarExistenciaMotivoSeleccionado(motivos)
        if self.__motivosSeleccionados is None:
            return
        if not self.pedirConfirmacionCierreOrden():
            messagebox.showinfo("Cancelado", "El cierre de la orden ha sido cancelado.")
            exit()
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
        estados_objetos = estadoConsulta()
        for estado in estados_objetos:
            self.__estado = estado
            self.__ambitoOI = self.__estado.sosAmbitoOrdenInspeccion()
            if self.__ambitoOI is True:
                break
        if self.__ambitoOI is False:
            messagebox.showerror("Error", "No se pudo encontrar el ambito 'Orden Inspeccion'.")
            exit()
        for estado in estados_objetos:
            self.__estado = estado
            self.__existeCerrada, self.__idCerrada = self.__estado.sosCerrada()
            if self.__existeCerrada is True:
                self.getFechaHoraActual(estados_objetos)
                break
        else:
            messagebox.showerror("Error", "No se pudo encontrar el estado 'Cerrada'.")
            exit()
    
    def getFechaHoraActual(self, estados_objetos):
        self.__fechaActual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.buscarFueraDeServicio(estados_objetos)

    def buscarFueraDeServicio(self, estados_objetos):
        for estado in estados_objetos:
            self.__estado = estado
            self.ambitoSis = self.__estado.sosAmbitoSismografo()
            if self.ambitoSis is True:
                break
        if self.ambitoSis is False:
            messagebox.showerror("Error", "No se pudo encontrar el ambito 'Sismografo'.")
            exit()
        for estado in estados_objetos:
            self.__estado = estado 
            self.__idFDS = self.__estado.sosFueraDeServicio()
            if self.__idFDS is True:
                break
        if self.__idFDS is False:
            messagebox.showerror("Error", "No se pudo encontrar el estado 'Fuera de Servicio'.")
            exit()
        self.cerrarOrdenInspeccion(self.__fechaActual, self.__idFDS, self.__idCerrada, self.__observacionCierre, self.__ordenSeleccionada, self.__comentarios, self.__motivosSeleccionados)       

    def cerrarOrdenInspeccion(self, fechaActual, idEstadoFdS, idCerrada, observacionCierre, ordenSeleccionada, comentario, motivoTipo):
        self.__ordenSeleccionada.cerrar(self.__idCerrada, observacionCierre, ordenSeleccionada)
        self.ponerSismografoFueraEstado(idEstadoFdS, fechaActual, comentario, motivoTipo)

    def ponerSismografoFueraEstado(self, idEstadoFdS, fechaActual, comentario, motivoTipo):
        self.__ordenSeleccionada.ponerSismografoFueraServicio(idEstadoFdS, fechaActual, comentario, motivoTipo)

    def buscarResponsablesReparacion(self):
        empleadoTodos_objetos = obtenerEmpleadosTodos()
        for empleado in empleadoTodos_objetos:
            self._empleado = empleado
            if empleado.esResponsableReparacion() is True:
                self.__mails_responsables.append(empleado.obtenerMail())
        self.enviarMails()

    def enviarMails(self):
        # Simula envío
        # Teniendo los mails en self.mails_responsables
        for mail in self.__mails_responsables:
            print("Enviando email de notificación...")
        self.__interfaz.enviarNotificacion()
        self.__pantallaCCRS.publicarNotificacion()

    def finCU(self):
        print('Fin Caso de Uso')

    def buscarOrdenes(self):
        return self.__ordenes