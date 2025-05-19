class EstacionSismologica:
    def __init__(self, codigo, nombre, documentoCertifAdq=None, fechaSolicCertif=None, latitud=None, longitud=None, sismografo_obj = None):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__documentoCertifAdq = documentoCertifAdq
        self.__fechaSolicCertif = fechaSolicCertif
        self.__latitud = latitud
        self.__longitud = longitud
        self.__sismografo = sismografo_obj
    def getNombreEstacion(self):
        return self.__nombre
    def getIdentificadorSismografo(self):
        if self.__sismografo is None:
            return "SIN_SISMOGRAFO"
        return self.__sismografo.getIdentificadorSismografo()