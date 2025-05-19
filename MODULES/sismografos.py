class Sismografo:
    def __init__(self, codigoEstacion, identificadorSismografo, fechaAdquisicion=None, nroSerie=None):
        self.__codigoEstacion = codigoEstacion
        self.__identificadorSismografo = identificadorSismografo
        self.__fechaAdquisicion = fechaAdquisicion
        self.__nroSerie = nroSerie

    def getIdentificadorSismografo(self):
        return self.__identificadorSismografo