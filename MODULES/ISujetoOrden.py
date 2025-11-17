from abc import ABC, abstractmethod


class ISujetoOrden(ABC):
    @abstractmethod
    def suscribir(self, observadores):
        pass

    @abstractmethod
    def desuscribir(self, observadores):
        pass

    @abstractmethod
    def obtener_observadores(self):
        pass
