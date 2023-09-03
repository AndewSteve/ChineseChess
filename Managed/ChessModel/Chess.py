import abc,pygame
from abc import abstractmethod,ABC
from enum import Enum

chess_img_path = "./Resource/img/Chess"

class ChessColor(Enum):
    RED = 1
    BLACK = 2

class Chess(ABC,pygame.sprite.Sprite):
    def __init__(self,color):
        self.color = color
        pygame.sprite.Sprite.__init__(self)
        self.rect:pygame.Rect = None

    @abstractmethod
    def init(self,position):
        self.x,self.y = position

    @abstractmethod
    def onSelected(self):
        pass 

    def onDestroyed(self):
        pass

    def move(self,new_posi):
        """_summary_

        Args:
            vector ((x,y)): TargetPosition

        Returns:
            Boolean: Move successfully
        """
        self.x,self.y = new_posi
        self.rectangle.center = new_posi
        return True

    








