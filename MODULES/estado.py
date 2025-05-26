import sqlite3
class Estado:
    def __init__(self, idEstado=None, nombre=None, ambito=None):
        self.__idEstado = idEstado
        self.__nombre = nombre
        self.__ambito = ambito

    def sosCompletamenteRealizada(self):
        return self.__nombre == "Completamente Realizada"

    def getIdEstado(self):
        return self.__idEstado
    def getNombre(self):
        return self.__nombre
    def getAmbito(self):
        return self.__ambito
    def sosAmbitoSismografo(self):
        if self.__ambito == "Sismografo":
            return True
        else:
            return False
    def sosAmbitoOrdenInspeccion(self):
        if self.__ambito == "Orden Inspeccion":
            return True
        else:
            return False
    def sosAmbito(self, ambito):
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Estados WHERE ambito = ?", (ambito,))
        ambitoOrdenInspeccion = cursor.fetchall()
        conn.close()
        return ambitoOrdenInspeccion if ambitoOrdenInspeccion else None
    def sosEstado(self, nombre):
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT idEstado FROM Estados WHERE nombreEstado = ?", (nombre,))
        estadoCerrada = cursor.fetchone()
        conn.close()
        return estadoCerrada[0] if estadoCerrada else None
    def sosFueradeServicio(self, nombre):
        conn = sqlite3.connect('MODULES/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT idEstado FROM Estados WHERE nombreEstado = ?", (nombre,))
        estadoFDS = cursor.fetchone()
        conn.close()
        return estadoFDS[0] if estadoFDS else None