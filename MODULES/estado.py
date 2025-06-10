import sqlite3
class Estado:
    def __init__(self, idEstado=None, ambito=None, nombre=None):
        self.__idEstado = idEstado
        self.__ambito = ambito
        self.__nombre = nombre

    def sosCompletamenteRealizada(self):
        if self.__nombre == "Completamente Realizada":
            return True
        else:
            return False

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
    def sosCerrada(self):
        if self.__nombre == "Cerrada":
            return True, self.__idEstado
        else:
            return False, None
    def sosFueraDeServicio(self):
        if self.__nombre == "Fuera de Servicio":
            return True, self.getIdEstado()
        else:
            return False, None    