from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def on_class_found(self, class_name: str) -> None:
        """Evento que se dispara cuando se encuentra una clase."""
        pass

    @abstractmethod
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        """Evento que se dispara cuando se encuentra una relación."""
        pass
