class Estado:
    def __init__(self, idEstado, nombre, ambito=None):
        self.__idEstado = idEstado
        self.__nombre = nombre
        self.__ambito = ambito

    def sosCompletamenteRealizada(self, id_buscada):
        if self.__idEstado == id_buscada:
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
        if self.__nombre == "Cerrado":
            return True
        else:
            return False
    def sosFueradeServicio(self):
        if self.__nombre == "Fuera de Servicio":
            return True
        else:
            return False
    def cerrar(self):
        