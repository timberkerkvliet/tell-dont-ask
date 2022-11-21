from abc import ABC, abstractmethod

from ordering.domain.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass

    @abstractmethod
    def get_by_id(self, order_id: int):
        pass
