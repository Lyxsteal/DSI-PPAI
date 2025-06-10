from typing import Optional
from MODULES.estacionSismo import EstacionSismologica  # Adjust the import according to your project structure
from datetime import datetime
import sqlite3
from MODULES.empleado import Empleado
from MODULES.estado import Estado
from DATABASE.estadoCBD import setEstadoCierre
# Import or define EstacionSismologica before using it
# from .estacionSismologica import EstacionSismologica  # Uncomment and adjust if you have this module

class OrdenInspeccion:
    def __init__(
        self,
        numeroOrden,
        fechaHoraInicio=None,
        fechaHoraCierre=None,
        fechaHoraFinalizacion=None,
        observacionCierre=None,
        empleado:Empleado=None,
        estado:Estado=None,
        estacion:EstacionSismologica = None):
        self.__numeroOrden             = numeroOrden
        self.__fechaHoraInicio       = fechaHoraInicio
        self.__fechaHoraCierre       = fechaHoraCierre
        self.__fechaHoraFinalizacion = fechaHoraFinalizacion
        self.__observacionCierre     = observacionCierre
        self.__empleado              = empleado
        self.__estado                = estado
        self.__estacionSismo         = estacion

    def sosCompletamenteRealizada(self):
        return self.__estado.sosCompletamenteRealizada()
    
    def obtenerDatos(self):
        nroOrden = self.getNroOrden()
        fechaHoraFinalizacion = self.getfechaHoraFinalizacion()
        nombreEstacion =self.getNombreEstacion()
        idSismografo = self.getIdentificadorSismografo()
        return nroOrden, fechaHoraFinalizacion, nombreEstacion, idSismografo
    def getNroOrden(self):
        return self.__numeroOrden

    def getfechaHoraFinalizacion(self):
        return self.__fechaHoraFinalizacion
    
    def getIdentificadorSismografo(self):
        if self.__estacionSismo is None:
            return "SIN_ESTACION"
        return self.__estacionSismo.getIdentificadorSismografo()
    
    def getNombreEstacion(self):
        if self.__estacionSismo is None:
            return "SIN_ESTACION"
        return self.__estacionSismo.getNombreEstacion()
    
    def sosDeEmpleado(self, nombreEmpleado):
        if self.__empleado.obtenerNombre() == nombreEmpleado:
            return True
        
    def cerrar(self, idEstado, observacionCierre, ordenSeleccionada):
        tiempoActual = self.setFechaHoraCierre()
        self.setEstadoCierre(idEstado, tiempoActual, observacionCierre, ordenSeleccionada)

    def setFechaHoraCierre(self):
        tiempoActual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return tiempoActual
    
    def setEstadoCierre(self, idEstado, fechaCierre, observacionCierre, ordenSeleccionada):
        setEstadoCierre(fechaCierre,observacionCierre,idEstado, ordenSeleccionada.getNroOrden())
        print(f"Orden {ordenSeleccionada.getNroOrden()} cerrada correctamente.")
        
    def ponerSismografoFueraServicio(self, idEstadoFdS, fechaActual, comentario, motivoTipo):
        self.__estacionSismo.ponerSismografoFueraServicio(idEstadoFdS, fechaActual, comentario, motivoTipo)
