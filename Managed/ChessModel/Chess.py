import abc,pygame
import os
from abc import abstractmethod,ABC
from enum import Enum
from Managed.Game import Dict_to_Abs_posi,scale_chess_img
chess_img_path = "./Resource/img/Chess"
#dropPoint_img_path = "./Resource/img/Chess"
drop_point_img = "提示.png"
eatable_red_img = "可击杀_红色_底色.png"
eatable_black_img = "可击杀_黑色_底色.png"
selected_img = "selected.png"

class DropPointKind(Enum):
    TIP = 1
    EATABLE_BLACK = 2
    EATABLE_RED = 3
    SELECTED = 4

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
    def onSelected(self,drop_point_list,chess_board,BLACK_checkmate,RED_checkmate):


        #将帅不相见
        if (abs(BLACK_checkmate.x - RED_checkmate.x)==1) and ((self is BLACK_checkmate) or (self is RED_checkmate)):
            target = (BLACK_checkmate if self is RED_checkmate else RED_checkmate)
            target_colum_empty = True
            temp_min,temp_max = min(target.y,self.y),max(target.y,self.y)
            temp_x = target.x
            for temp_y in range(temp_min+1,temp_max):
                if chess_board.__contains__((temp_x,temp_y)):
                    target_colum_empty = False
                    break
            if target_colum_empty:
                temp_list = []
                for drop_point in drop_point_list:
                    x,_ = drop_point
                    if x == target.x:
                        temp_list.append(drop_point)
                for drop_point in temp_list:
                        drop_point_list.remove(drop_point)
        elif (BLACK_checkmate.x == RED_checkmate.x) and (self.x == BLACK_checkmate.x):
            flag = True
            temp_x = BLACK_checkmate.x
            for temp_y in range(RED_checkmate.y+1,self.y):
                if chess_board.__contains__((temp_x,temp_y)):
                    flag = False
                    break
            if flag:
                for temp_y in range(self.y+1,BLACK_checkmate.y):
                    if chess_board.__contains__((temp_x,temp_y)):
                        flag = False
                        break
            if flag:
                temp_list = []
                for drop_point in drop_point_list:
                    _,y = drop_point
                    if y == self.y:
                        temp_list.append(drop_point)
                for drop_point in temp_list:
                    drop_point_list.remove(drop_point)
        

        self.drop_point_dict:dict[(int,int),pygame.sprite.Sprite] = {}
        self.drop_sprite_group:pygame.sprite.Group = pygame.sprite.Group()
        self.drop_sprite_group.add(DropPoint(DropPointKind.SELECTED,(self.x,self.y)))
        for drop_point_posi in drop_point_list:
            if chess_board.__contains__(drop_point_posi):
                chess_color = chess_board[drop_point_posi].color
                if chess_color == ChessColor.BLACK:
                    drop_point_sprite = DropPoint(DropPointKind.EATABLE_RED,drop_point_posi)
                else:
                    drop_point_sprite = DropPoint(DropPointKind.EATABLE_BLACK,drop_point_posi)
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
        enlargeSize = 1
        if kind == DropPointKind.TIP:
            image = drop_point_img
        elif kind == DropPointKind.EATABLE_BLACK:
            image = eatable_black_img
            enlargeSize = 1.3
        elif kind == DropPointKind.EATABLE_RED:
            image = eatable_red_img
            enlargeSize = 1.3
        else:
            image = selected_img
            enlargeSize = 1.5
        self.image = pygame.image.load(os.path.join(chess_img_path,image))
        self.image = scale_chess_img(self.image,enlargeSize)
        self.rect = self.image.get_rect()
        abs_x,abs_y = Dict_to_Abs_posi(dict_posi)
        self.rect.center = (abs_x,abs_y)

    








