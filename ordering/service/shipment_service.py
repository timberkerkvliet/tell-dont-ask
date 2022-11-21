from abc import ABCMeta, abstractmethod

from ordering.domain.order import Order


class ShipmentService(metaclass=ABCMeta):
    def __init(self):
        raise NotImplementedError

    @abstractmethod
    def ship(self, order: Order):
        pass
