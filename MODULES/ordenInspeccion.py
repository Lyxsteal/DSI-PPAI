from typing import Optional
from MODULES.estacionSismo import EstacionSismologica  # Adjust the import according to your project structure

# Import or define EstacionSismologica before using it
# from .estacionSismologica import EstacionSismologica  # Uncomment and adjust if you have this module

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
        estacion: Optional["EstacionSismologica"] = None,  # Use forward reference if not yet defined
        
    ):
        self.numeroOrden             = numeroOrden
        self.__fechaHoraInicio       = fechaHoraInicio
        self.__fechaHoraCierre       = fechaHoraCierre
        self.__fechaHoraFinalizacion = fechaHoraFinalizacion
        self.__observacionCierre     = observacionCierre
        self.__empleado              = empleado
        self.__estado                = estado
        self.__estacionSismo         = estacion

    def sosCompletamenteRealizada(self):
        if self.__estado is not None:
            return self.__estado.sosCompletamenteRealizada()
        return False
    
    def getNroOrden(self):
        return self.numeroOrden

    def getfechaHoraFinalizacion(self):
        return self.__fechaHoraFinalizacion
    
    def getIdentificadorSismografo(self):
        if self.__estacionSismo is None:
            return "SIN_ESTACION"
        return self.__estacionSismo.getIdentificadorSismografo()
    
    def getNombreEstacion(self):
        if self.__estacionSismo is None:
            return "SIN_ESTACION"
        return self.__estacionSismo.getNombreEstacion()
    
    def sosDeEmpleado(self, empleado):
        # Si self.__empleado es string (nombre), compara por nombre
        if isinstance(empleado, str):
            return self.__empleado == empleado
        # Si es objeto Empleado, compara por nombre
        return self.__empleado == empleado.nombre