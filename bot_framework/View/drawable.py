from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def remove(self):
        pass
