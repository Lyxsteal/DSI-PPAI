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
from MODULES.ISujetoOrden import ISujetoOrden
from tkinter import messagebox
from DATABASE.estadoCBD import estadoConsulta
from DATABASE.ordenesCBD import buscarOrdenesInspeccion
from DATABASE.motivoTipoCBD import obtenerMotivoTipo
from DATABASE.empleadoCBD import obtenerEmpleadosTodos

class GestorOrdenDeInspeccion(ISujetoOrden):
    def __init__(self, sesionActual:Sesion, estado:Optional[Estado] = None, 
                 pantallaCCRS:Optional[PantallaCCRS] = None, interfaz:Optional[InterfazNotificacionEmail] = None , ordenes = None, fechaActual = None, ordenSeleccionada = None, observacion = None, orden:OrdenInspeccion=None):
        self.__sesion = sesionActual
        self.__estado = estado
        self.__pantallaCCRS = pantallaCCRS or PantallaCCRS()
        self.__interfaz = interfaz or InterfazNotificacionEmail()
        self.__observadores = []
        self.__ordenesOrdenadas = None
        self.__fechaActual = fechaActual
        self.__ordenSeleccionada = ordenSeleccionada
        self.__comentarios = None
        self.__observacionCierre = observacion
        self.__ambitoOI = None
        self.__ambitoSis = None
        self.__existeCerrada = None
        self.__idCerrada = None
        self.__idFDS = None
        self.__estadoFDSNombre = None
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
        self.__ordenesOrdenadas = ordenesOrdenadas
        return self.__ordenesOrdenadas
    
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
            self.__existeCerrada, idCerrada = self.__estado.sosCerrada()
            if self.__existeCerrada is True:
                self.__idCerrada = idCerrada
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
            self.__ambitoSis = self.__estado.sosAmbitoSismografo()
            if self.__ambitoSis is True:
                break
        if self.__ambitoSis is False:
            messagebox.showerror("Error", "No se pudo encontrar el ambito 'Sismografo'.")
            exit()
        existsFDS = False
        for estado in estados_objetos:
            self.__estado = estado 
            existsFDS, idFDS = self.__estado.sosFueraDeServicio()
            if existsFDS is True:
                self.__idFDS = idFDS
                self.__estadoFDSNombre = self.__estado.getNombre()
                break
        if existsFDS is False:
            messagebox.showerror("Error", "No se pudo encontrar el estado 'Fuera de Servicio'.")
            exit()
        self.cerrarOrdenInspeccion()
        self.notificar()

    def cerrarOrdenInspeccion(self):
        self.suscribir([self.__interfaz, self.__pantallaCCRS])
        self.__ordenSeleccionada.cerrar(self.__idCerrada, self.__observacionCierre)
        self.ponerSismografoFueraEstado()

    def ponerSismografoFueraEstado(self):
        self.__ordenSeleccionada.ponerSismografoFueraServicio(self.__idFDS, self.__fechaActual, self.__comentarios, self.__motivosSeleccionados)

    def notificar(self):
        motivos = []
        if self.__motivosSeleccionados:
            for motivo in self.__motivosSeleccionados:
                if hasattr(motivo, "getDescripcion"):
                    motivos.append(motivo.getDescripcion())
                else:
                    motivos.append(str(motivo))
        id_sismografo = self.__ordenSeleccionada.getIdentificadorSismografo()
        nombre_estado = self.__estadoFDSNombre
        fecha_registro = self.__fechaActual
        comentarios = self.__comentarios
        destinatarios = self.buscarResponsablesReparacion()
        for observador in self.__observadores:
            if hasattr(observador, "destinatarios"):
                observador.destinatarios = destinatarios
            observador.publicarNotificacion(
                id_sismografo,
                nombre_estado,
                fecha_registro,
                motivos,
                comentarios
            )

    def suscribir(self, observadores):
        if observadores is None:
            return
        if not isinstance(observadores, list):
            observadores = [observadores]
        for observador in observadores:
            if observador and observador not in self.__observadores:
                self.__observadores.append(observador)

    def desuscribir(self, observadores):
        if observadores is None:
            return
        if not isinstance(observadores, list):
            observadores = [observadores]
        self.__observadores = [obs for obs in self.__observadores if obs not in observadores]

    def obtener_observadores(self):
        return list(self.__observadores)

    def buscarResponsablesReparacion(self):
        self.__mails_responsables = []
        empleadoTodos_objetos = obtenerEmpleadosTodos()
        for empleado in empleadoTodos_objetos:
            self._empleado = empleado
            if empleado.esResponsableReparacion() is True:
                self.__mails_responsables.append(empleado.obtenerMail())
        return self.__mails_responsables

    def finCU(self):
        print('Fin Caso de Uso')

    def buscarOrdenes(self):
        return self.__ordenesOrdenadas
