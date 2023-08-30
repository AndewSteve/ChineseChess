import abc
from abc import abstractmethod,ABC

class Chess(ABC):

    @abc.abstractmethod
    def move(self,vector):
        """_summary_

        Args:
            vector ((x,y)): TargetPosition

        Returns:
            Boolean: Move successfully
        """
        x,y = vector
        return True
    
    @abc.abstractmethod
    def onSelected(self):
        pass
    
    @abstractmethod
    def onDestroyed(self):
        pass

    def __init__(self) -> None:
        pass


