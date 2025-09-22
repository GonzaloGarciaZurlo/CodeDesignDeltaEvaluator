from abc import ABC, abstractmethod
from typing import override


class Example(ABC):
    @abstractmethod
    def method(self):
        pass

    @abstractmethod
    def another_method(self):
        pass

    @abstractmethod
    def yet_another_method(self):
        pass


class AnotherExample(Example):
    @override
    def method(self):
        pass

    @override
    def another_method(self):
        pass

    @override
    def yet_another_method(self):
        pass