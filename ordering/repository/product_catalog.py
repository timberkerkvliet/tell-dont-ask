from abc import ABC, abstractmethod


class ProductCatalog(ABC):
    @abstractmethod
    def get_by_name(self, name: str):
        pass
