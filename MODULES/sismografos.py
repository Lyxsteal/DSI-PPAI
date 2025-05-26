from MODULES.cambioEstado import CambioEstado
import sqlite3
class Sismografo:
    def __init__(self, codigoEstacion, identificadorSismografo, fechaAdquisicion=None, nroSerie=None, cambioEstado:CambioEstado= None):
        self.__codigoEstacion = codigoEstacion
        self.__identificadorSismografo = identificadorSismografo
        self.__fechaAdquisicion = fechaAdquisicion
        self.__nroSerie = nroSerie
        self.__cambioEstado = cambioEstado

    def getIdentificadorSismografo(self):
        return self.__identificadorSismografo
    def setCambioEstado(self, cambioEstado):
        self.__cambioEstado = cambioEstado
    def fueraServicio(self, fechaActual, comentario, motivoTipo):
        actualCE= self.__cambioEstado.esEstadoActual(self.__identificadorSismografo)
        self.__cambioEstado.setFechaHoraFin(actualCE)
        self.cambiarEstadoFueraServicio(fechaActual, self.__identificadorSismografo, comentario, motivoTipo)
    def cambiarEstadoFueraServicio(self, idEstadoFdS, fechaActual, identificadorSismografo, comentario, motivoTipo):
        try:
            print(f"[DEBUG] Insertando CambioEstado con fecha: {fechaActual}, estado: {idEstadoFdS}, idSismografo: {identificadorSismografo}")
            conn = sqlite3.connect('MODULES/database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CambiosEstado (fechaHoraInicio, fechaHoraFin, idSismografo, idEstado) VALUES(?,?,?,?)",(fechaActual, None, identificadorSismografo, idEstadoFdS))
            conn.commit()
            conn.close()
            self.__cambioEstado = CambioEstado(fechaHoraInicio= fechaActual, fechaHoraFin= None, estado_obj= 2, idSismografo= identificadorSismografo, fechaActual= fechaActual, comentario= comentario, motivoTipo = motivoTipo)
        except sqlite3.Error as e:
            print(f"[ERROR] Falló el INSERT en CambiosEstado: {e}")