from abc import ABC, abstractmethod


class QueuingSystem(ABC):

    @abstractmethod
    def P0(self):
        pass

    @abstractmethod
    def Pj(self, j: int):
        pass

    @abstractmethod
    def n_o(self):
        pass

    @abstractmethod
    def k3(self):
        pass

    @abstractmethod
    def j(self):
        pass

    @abstractmethod
    def t_wait(self):
        pass

    @abstractmethod
    def t_sys(self):
        pass
