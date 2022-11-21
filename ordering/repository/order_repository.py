from abc import ABC, abstractmethod

from ordering.domain.order import Order


class OrderRepository(ABC):
    def __init(self):
        raise NotImplementedError

    @abstractmethod
    def save(self, order: Order):
        pass

    @abstractmethod
    def get_by_id(self, order_id: int):
        pass
