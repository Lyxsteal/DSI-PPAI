class OrdenInspeccion:
    def __init__(
        self,
        numeroOrden,
        fechaHoraInicio=None,
        fechaHoraCierre=None,
        fechaHoraFinalizacion=None,
        observacionCierre=None,
        empleado=None,
        estado=None,
        estacion=None,
        
    ):
        self.__numeroOrden           = numeroOrden
        self.__fechaHoraInicio       = fechaHoraInicio
        self.__fechaHoraCierre       = fechaHoraCierre
        self.__fechaHoraFinalizacion = fechaHoraFinalizacion
        self.__observacionCierre     = observacionCierre
        self.__empleado              = empleado
        self.__estado                = estado
        self.__estacionSismo         = estacion

    def sosCompletamenteRealizada(self):
        return self.__estado.sosCompletamenteRealizada()

    def getNroOrden(self):
        return self.__numeroOrden

    def getfechaHoraFinalizacion(self):
        return self.__fechaHoraFinalizacion
    
    def getIdentificadorSismografo(self):
        if self.__estacionSismo is None:
            return "SIN_ESTACION"
        return self.__estacionSismo.getIdentificadorSismografo()
    
    def getNombreEstacion(self):
        return self.__estacionSismo.getNombreEstacion()
    
    def sosDeEmpleado(self, empleado):
        if self.__empleado == empleado:
            return True