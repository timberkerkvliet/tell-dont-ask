from abc import ABC, abstractmethod

from ordering.domain.order import Order


class ShipmentService(ABC):
    @abstractmethod
    def ship(self, order: Order):
        pass
