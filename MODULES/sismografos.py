from MODULES.cambioEstado import CambioEstado
from DATABASE.cambioestadoCDB.cambioestadoGET import getCambiosEstado, insertCambioEstado
from MODULES.estado import Estado
from MODULES.motivoFueraServicio import MotivoFueraServicio
from MODULES.motivosTipo import MotivoTipo
import sqlite3

class Sismografo:
    def __init__(self, codigoEstacion, identificadorSismografo=None, fechaAdquisicion=None, nroSerie=None, cambioEstado:CambioEstado= None):
        self.__codigoEstacion = codigoEstacion
        self.__identificadorSismografo = identificadorSismografo
        self.__fechaAdquisicion = fechaAdquisicion
        self.__nroSerie = nroSerie
        self.__cambioEstado = cambioEstado

    def getIdentificadorSismografo(self):
        return self.__identificadorSismografo
    
    def fueraServicio(self, idEstadoFdS, fechaActual, comentario, motivoTipo):
        cambiosEstado_objetos = getCambiosEstado(self.__identificadorSismografo)
        for cambio in cambiosEstado_objetos:
            self.__cambioEstado = cambio
            if self.__cambioEstado.esEstadoActual() is True:
                self.__cambioEstado.setFechaHoraFin(cambio)
                break
        else:
            print('No se encontró cambio de estado actual para el sismografo: ', self.__identificadorSismografo)
            exit()
        self.cambiarEstadoFueraServicio(idEstadoFdS, fechaActual, self.__identificadorSismografo, comentario, motivoTipo)

    def cambiarEstadoFueraServicio(self, idEstadoFdS, fechaActual, identificadorSismografo, comentario, motivoTipo):
        insertCambioEstado(fechaActual, identificadorSismografo, idEstadoFdS, comentario, motivoTipo)
        