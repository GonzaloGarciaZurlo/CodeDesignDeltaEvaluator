from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def on_class_found(self, class_name):
        """Evento que se dispara cuando se encuentra una clase."""
        pass

    @abstractmethod
    def on_relation_found(self, class1, class2, relation):
        """Evento que se dispara cuando se encuentra una relación."""
        pass
