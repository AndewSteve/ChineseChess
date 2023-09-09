import abc,pygame
import os
from abc import abstractmethod,ABC
from enum import Enum
from .ChessColor import ChessColor


#region 游戏资源
chess_img_path = "./Resource/img/Chess"
#dropPoint_img_path = "./Resource/img/Chess"
drop_point_img = "提示.png"
eatable_red_img = "可击杀_红色_底色.png"
eatable_black_img = "可击杀_黑色_底色.png"
selected_img = "selected.png"
#endregion

#region 常量
eatable_enlarge = 1.1
selected_enlarge = 1.5
#endregion


class DropPointKind(Enum):
    TIP = 1
    EATABLE_BLACK = 2
    EATABLE_RED = 3
    SELECTED = 4



class Chess(ABC,pygame.sprite.Sprite):
    def __init__(self,color):
        self.color:ChessColor = color
        super().__init__()
        self.rect:pygame.Rect = None

    @abstractmethod
    def init(self,dict_posi):
        from Managed.Window import scale_chess_img
        """加载图片

        Args:
            dict_posi (tuple): 逻辑位置,用于定位屏幕位置
        """
        self.image = pygame.image.load(self.chess_img_path)
        self.image = scale_chess_img(self.image)
        self.rect = self.image.get_rect()
        self.x,self.y = dict_posi
        #self.rect.center = Dict_to_Abs_posi(dict_posi)  游戏开始时会刷新屏幕，Container会给所有棋子摆正

    @abstractmethod
    def onSelected(self,drop_point_list,chess_board,BLACK_checkmate,RED_checkmate,to_checkmate = False):
        """展示落点

        Args:
            drop_point_list (list:tuple): 具体棋子类传给父类的落点数组,由父类处理
            chess_board (dict[(int,int),Chess]): Container传给具体棋子类的棋盘信息
            BLACK_checkmate (Chess): Container传给父类的"将"信息
            RED_checkmate (Chess): Container传给父类的"帅"信息
            to_checkmate (bool, optional): 是否要截获落点数组. Defaults to False.
        """

        if to_checkmate:
             return drop_point_list

        #将帅不相见
        drop_point_list = self.check_king_opposite(drop_point_list,chess_board,BLACK_checkmate,RED_checkmate)
        

        self.drop_point_dict:dict[(int,int),pygame.sprite.Sprite] = {}
        self.drop_sprite_group:pygame.sprite.Group = pygame.sprite.Group()
        self.drop_sprite_group.add(DropPoint(DropPointKind.SELECTED,(self.x,self.y)))
        for drop_point_posi in drop_point_list:
            if chess_board.__contains__(drop_point_posi):#可吃子
                chess_color = chess_board[drop_point_posi].color
                if chess_color == ChessColor.BLACK:
                    drop_point_sprite = DropPoint(DropPointKind.EATABLE_RED,drop_point_posi)
                else:
                    drop_point_sprite = DropPoint(DropPointKind.EATABLE_BLACK,drop_point_posi)
            else:
                drop_point_sprite = DropPoint(DropPointKind.TIP,drop_point_posi)#落子提示
            self.drop_point_dict[drop_point_posi] = drop_point_sprite
            self.drop_sprite_group.add(drop_point_sprite)


    def check_king_opposite(self,drop_point_list,chess_board,BLACK_checkmate,RED_checkmate):
        """将帅不相见
        """
        fileted_list = []
        target_colum_empty = True
        if (self is BLACK_checkmate) or (self is RED_checkmate):
            if (abs(BLACK_checkmate.x - RED_checkmate.x)==1) or (BLACK_checkmate.x == RED_checkmate.x):
                target = (BLACK_checkmate if (self is RED_checkmate) else RED_checkmate)
                temp_x = target.x
                for temp_y in range(BLACK_checkmate.y,RED_checkmate.y+1):
                    if chess_board.__contains__((temp_x,temp_y)) and (not(chess_board[(temp_x,temp_y)] is self)) and (not(chess_board[(temp_x,temp_y)] is target)):
                        if drop_point_list.__contains__((temp_x,temp_y)):
                            fileted_list.append((temp_x,temp_y))
                        else:
                            target_colum_empty = False
                        break
                if target_colum_empty:
                    for drop_point in drop_point_list:
                        x,_ = drop_point
                        if x == target.x:
                            fileted_list.append(drop_point)
        elif (self.x == BLACK_checkmate.x) and (BLACK_checkmate.x == RED_checkmate.x):
            temp_x = BLACK_checkmate.x
            for temp_y in range(BLACK_checkmate.y+1,RED_checkmate.y):
                if chess_board.__contains__((temp_x,temp_y)):
                    if not (chess_board[(temp_x,temp_y)] is self):
                        target_colum_empty = False
                        break
            if target_colum_empty:
                for drop_point in drop_point_list:
                    x,_ = drop_point
                    if not x == self.x:
                        fileted_list.append(drop_point)
        for drop_point in fileted_list:
            if drop_point_list.__contains__(drop_point):
                drop_point_list.remove(drop_point)
        return drop_point_list

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
        from Managed.Window import Dict_to_Abs_posi
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
        from Managed.Window import Dict_to_Abs_posi,scale_chess_img
        super().__init__()
        enlargeSize = 1
        if kind == DropPointKind.TIP:
            image = drop_point_img
        elif kind == DropPointKind.EATABLE_BLACK:
            image = eatable_black_img
            enlargeSize = eatable_enlarge
        elif kind == DropPointKind.EATABLE_RED:
            image = eatable_red_img
            enlargeSize = eatable_enlarge
        else:
            image = selected_img
            enlargeSize = selected_enlarge
        self.image = pygame.image.load(os.path.join(chess_img_path,image))
        self.image = scale_chess_img(self.image,enlargeSize)
        self.rect = self.image.get_rect()
        abs_x,abs_y = Dict_to_Abs_posi(dict_posi)
        self.rect.center = (abs_x,abs_y)

    








