import abc
from abc import abstractmethod,ABC
from enum import Enum

class ChessColor(Enum):
    RED = 1
    BLACK = 2
class Chess(ABC):
    def move(self,vector):
        """_summary_

        Args:
            vector ((x,y)): TargetPosition

        Returns:
            Boolean: Move successfully
        """
        x,y = vector
        return True

    @abstractmethod
    def onSelected(self):
        pass
    
    def onDestroyed(self):
        pass

    def init(self,position):
        self.x,self.y = position


    def __init__(self,color):
        self.color = color



