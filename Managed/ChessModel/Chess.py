import abc,pygame
import os
from abc import abstractmethod,ABC
from enum import Enum
from Managed.Game import Dict_to_Abs_posi,scale_chess_img
chess_img_path = "./Resource/img/Chess"
#dropPoint_img_path = "./Resource/img/Chess"
drop_point_img = "提示.png"
eatable_img = "可击杀.png"


class DropPointKind(Enum):
    TIP = 1
    EATABLE = 2

class ChessColor(Enum):
    RED = 1
    BLACK = 2

class Chess(ABC,pygame.sprite.Sprite):
    def __init__(self,color):
        self.color = color
        super().__init__()
        self.rect:pygame.Rect = None

    @abstractmethod
    def init(self,dict_posi):
        self.image = pygame.image.load(self.chess_img_path)
        self.image = scale_chess_img(self.image)
        self.rect = self.image.get_rect()
        self.x,self.y = dict_posi
        #self.rect.center = Dict_to_Abs_posi(dict_posi)  游戏开始时会刷新屏幕，Container会给所有棋子摆正

    @abstractmethod
    def onSelected(self,drop_point_list,chess_board):
        self.drop_point_dict:dict[(int,int),pygame.sprite.Sprite] = {}
        self.drop_sprite_group:pygame.sprite.Group = pygame.sprite.Group()
        for drop_point_posi in drop_point_list:
            if chess_board.__contains__(drop_point_posi):
                drop_point_sprite = DropPoint(DropPointKind.EATABLE,drop_point_posi)
            else:
                drop_point_sprite = DropPoint(DropPointKind.TIP,drop_point_posi)
            self.drop_point_dict[drop_point_posi] = drop_point_sprite
            self.drop_sprite_group.add(drop_point_sprite)

    # def draw_drop_points(self,screen):
    #     self.drop_sprite_group.update()
    #     self.drop_sprite_group.draw(screen)

    # def clear_drop_points(self,screen,board):
    #     self.drop_sprite_group.update()
    #     self.drop_sprite_group.clear(screen,board)
    #     self.drop_sprite_group.draw(screen)


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
    
class DropPoint(pygame.sprite.Sprite):
    def __init__(self,kind:DropPointKind,dict_posi):
        super().__init__()
        if kind == DropPointKind.TIP:
            image = drop_point_img
        else:
            image = eatable_img
        self.image = pygame.image.load(os.path.join(chess_img_path,image))
        self.image = scale_chess_img(self.image)
        self.rect = self.image.get_rect()
        abs_x,abs_y = Dict_to_Abs_posi(dict_posi)
        self.rect.center = (abs_x,abs_y)

    








