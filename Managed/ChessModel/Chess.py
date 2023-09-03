import abc,pygame
from abc import abstractmethod,ABC
from enum import Enum
from Managed.Game import Dict_to_Abs_posi,scale_img
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
    def init(self,dict_posi):
        self.image = pygame.image.load(self.chess_img_path)
        self.image = scale_img(self.image)
        self.rect = self.image.get_rect()
        self.x,self.y = dict_posi
        #self.rect.center = Dict_to_Abs_posi(dict_posi)  游戏开始时会刷新屏幕，Container会给所有棋子摆正

    @abstractmethod
    def onSelected(self):
        pass 

    def onDestroyed(self):
        pass

    def move(self,dict_posi):
        """_summary_

        Args:
            vector ((x,y)): TargetPosition

        Returns:
            Boolean: Move successfully
        """
        self.x,self.y = dict_posi
        self.rect.center = Dict_to_Abs_posi(dict_posi)
        return True

    








