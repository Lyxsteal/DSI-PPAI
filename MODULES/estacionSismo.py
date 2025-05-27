from MODULES.sismografos import Sismografo
class EstacionSismologica:
    def __init__(self, codigo=None, nombre=None, documentoCertifAdq=None, fechaSolicCertif=None, latitud=None, longitud=None, sismografo:Sismografo=None):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__documentoCertifAdq = documentoCertifAdq
        self.__fechaSolicCertif = fechaSolicCertif
        self.__latitud = latitud
        self.__longitud = longitud
        self.__sismografo = sismografo
    def getNombreEstacion(self):
        return self.__nombre
    def getIdentificadorSismografo(self):
        if self.__sismografo is None:
            return "SIN_SISMOGRAFO"
        return self.__sismografo.getIdentificadorSismografo()
    def ponerSismografoFueraServicio(self, idEstadoFdS,fechaActual, comentario, motivoTipo):
        self.__sismografo.fueraServicio(idEstadoFdS,fechaActual, comentario, motivoTipo)