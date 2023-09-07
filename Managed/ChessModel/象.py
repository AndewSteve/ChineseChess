import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 象(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"相.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"象.png")
        super().init(position)
        
    def onSelected(self,chess_board:dict[(int,int),Chess],BLACK_checkmate,RED_checkmate,to_checkmate = False):
        """具体子类逻辑

        Args:
            chess_board (dict[(int,int),Chess]): Container传给具体棋子类的棋盘信息
            BLACK_checkmate (Chess): Container传给父类的"将"信息
            RED_checkmate (Chess): Container传给父类的"帅"信息
            to_checkmate (bool, optional): 是否要截获落点数组. Defaults to False.

        Returns:
            list:tuple: 落点逻辑坐标数组
        """
        result = []

        top_max, button_max = 5, 9
        left_max, right_max = 0, 8
        self_posi = pygame.math.Vector2(self.x, self.y)
        if self.color == ChessColor.BLACK:
            top_max, button_max = 0, 4


        pre_select = [(self.x + 2, self.y + 2),
                      (self.x + 2, self.y - 2),
                      (self.x - 2, self.y + 2),
                      (self.x - 2, self.y - 2), ]

        for i in range(left_max, right_max + 1):
            for j in range(top_max, button_max + 1):
                if (i, j) in pre_select:
                    if chess_board.__contains__((int((self.x + i)/2)  , int((self.y + j)/2))) == True:
                        continue
                    elif chess_board.__contains__((int((self.x + i)/2)  , int((self.y + j)/2))) == False:
                        if chess_board.__contains__((i,j)) == True:
                            if chess_board[(i,j)].color == self.color:
                                continue
                            else:
                                result.append((i,j))
                        else:
                            result.append((i,j))


        if to_checkmate:
             return result
        else:
            super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate)