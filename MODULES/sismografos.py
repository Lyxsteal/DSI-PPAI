from MODULES.cambioEstado import CambioEstado
from DATABASE.cambioestadoCBD import getCambiosEstado, insertCambioEstado
from MODULES.estado import Estado
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
        print('el sismografo:', self.__identificadorSismografo)
        cambiosEstado = getCambiosEstado(self.__identificadorSismografo)
        for cambio in cambiosEstado:
            fechaHoraInicio, fechaHoraFin, idSismografo, idEstado = cambio
            cambioEstado = CambioEstado(fechaHoraInicio, fechaHoraFin, idSismografo, idEstado)
            if cambioEstado.esEstadoActual() == True:
                print('id sismografo: ', cambioEstado.getIdSismografo)
                cambioEstado.setFechaHoraFin(cambio)
                break
        else:
            print('No se encontró cambio de estado actual para el sismografo: ', self.__identificadorSismografo)
            exit()
        self.cambiarEstadoFueraServicio(idEstadoFdS, fechaActual, self.__identificadorSismografo, comentario, motivoTipo)
    def cambiarEstadoFueraServicio(self, idEstadoFdS, fechaActual, identificadorSismografo, comentario, motivoTipo):
        insertCambioEstado(fechaActual, identificadorSismografo, idEstadoFdS)
        self.__cambioEstado = CambioEstado(fechaHoraInicio= fechaActual, fechaHoraFin= None, idEstado= Estado(idEstado=idEstadoFdS), idSismografo= identificadorSismografo, comentario= comentario, motivoTipo = motivoTipo)
        