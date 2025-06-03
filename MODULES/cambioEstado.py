import sqlite3
from datetime import datetime
from MODULES.motivoFueraServicio import MotivoFueraServicio
from MODULES.estado import Estado
from DATABASE.cambioestadoCDB.cambioestadoSETFH import setFechaHoraFin
from DATABASE.motivosCDB import insertMotivoFS
class CambioEstado:
    def __init__(self, fechaHoraInicio = None, fechaHoraFin = None, estado:Estado= None, idSismografo = None, motivoFS:dict=None):
        self.__fechaHoraInicio = fechaHoraInicio
        self.__fechaHoraFin = fechaHoraFin
        self.__estado = estado
        self.__idSismografo = idSismografo
        self.__motivoFS = motivoFS
        if motivoFS is not None:
            self.crearMotivoFueraServicio(fechaHoraInicio, motivoFS)
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
        print('peeediilo', cambio.getIdSismografo(), cambio.getFechaHoraInicio())
        setFechaHoraFin(tiempoFin, cambio.getIdSismografo(), cambio.getFechaHoraInicio())
        
    def crearMotivoFueraServicio(self, fechaActual, motivoFS):
        for motivo, comentario in motivoFS.items():
            insertMotivoFS(fechaActual, comentario, motivo)
    