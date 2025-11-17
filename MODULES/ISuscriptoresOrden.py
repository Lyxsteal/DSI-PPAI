from abc import ABC, abstractmethod


class ISuscriptoresOrden(ABC):
    @abstractmethod
    def publicarNotificacion(self, idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios):
        pass
