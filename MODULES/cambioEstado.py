import sqlite3
from datetime import datetime
from MODULES.motivoFueraServicio import MotivoFueraServicio
from DATABASE.cambioestadoCBD import setFechaHoraFin
from DATABASE.motivosCDB import insertMotivoFS
class CambioEstado:
    def __init__(self, fechaHoraInicio = None, fechaHoraFin = None, idEstado= None, idSismografo = None, comentario=None, motivoTipo:MotivoFueraServicio=None):
        self.__fechaHoraInicio = fechaHoraInicio
        self.__fechaHoraFin = fechaHoraFin
        self.__estado = idEstado
        self.__idSismografo = idSismografo
        self.__motivo = motivoTipo
        if motivoTipo is not None and comentario is not None:
            self.crearMotivoFueraServicio(fechaHoraInicio, comentario, motivoTipo)
    def getIdSismografo(self):
        return self.__idSismografo
    def getFechaHoraInicio(self):
        return self.__fechaHoraInicio
    def esEstadoActual(self):
        if self.__fechaHoraFin is None:
            return True
        else:
            return False
    def setFechaHoraFin(self, cambio):
        tiempoFin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('peeediilo', cambio[2], cambio[0])
        setFechaHoraFin(tiempoFin, cambio[2], cambio[0])
    def crearMotivoFueraServicio(self, fechaActual, comentario_por_motivo, motivo):
        for motivo, comentario in comentario_por_motivo.items():
            insertMotivoFS(fechaActual, comentario, motivo)
            self.__motivo = MotivoFueraServicio(comentario, motivo)