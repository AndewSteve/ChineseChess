import os
from .Chess import Chess,ChessColor,chess_img_path
class 马(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"马.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"馬.png")
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

        top_max, button_max = 0, 9
        left_max, right_max = 0, 8
        # if self.color == ChessColor.RED:
        #     top_max, button_max = 0, 4

        # ori = pygame.math.Vector2((left_max + right_max) / 2, (top_max + button_max) / 2)
        # self_magnitude = (ori - self_posi).length()

        pre_select1 = [(self.x + 1, self.y + 2),
                       (self.x - 1, self.y + 2),
                       ]
        pre_select2 = [(self.x + 1, self.y - 2),
                       (self.x - 1, self.y - 2),
                       ]
        pre_select3 = [(self.x + 2, self.y - 1),
                       (self.x + 2, self.y + 1),
                      ]
        pre_select4 = [(self.x - 2, self.y - 1),
                       (self.x - 2, self.y + 1),
                      ]
        for i in range(left_max, right_max + 1):
            for j in range(top_max, button_max + 1):
                if (i, j) in pre_select1:
                    if chess_board.__contains__((self.x,j - 1)) == True:
                        continue
                    elif chess_board.__contains__((i,j)) == True:
                        if chess_board[(i,j)].color == chess_board[(self.x,self.y)].color:
                            continue
                        else:
                            result.append((i,j))
                    elif chess_board.__contains__((self.x,j - 1)) == False:
                        result.append((i,j))
                if (i, j) in pre_select2:
                    if chess_board.__contains__((self.x,j + 1)) == True:
                        continue
                    elif chess_board.__contains__((i,j)) == True:
                        if chess_board[(i,j)].color == chess_board[(self.x,self.y)].color:
                            continue
                        else:
                            result.append((i,j))
                    elif chess_board.__contains__((self.x,j + 1)) == False:
                        result.append((i,j))
                if (i, j) in pre_select3:
                    if chess_board.__contains__((i - 1,self.y)) == True:
                        continue
                    elif chess_board.__contains__((i,j)) == True:
                        if chess_board[(i,j)].color == chess_board[(self.x,self.y)].color:
                            continue
                        else:
                            result.append((i,j))
                    elif chess_board.__contains__((i - 1,self.y)) == False:
                        result.append((i,j))
                if (i, j) in pre_select4:
                    if chess_board.__contains__((i + 1,self.y)) == True:
                        continue
                    elif chess_board.__contains__((i,j)) == True:
                        if chess_board[(i,j)].color == chess_board[(self.x,self.y)].color:
                            continue
                        else:
                            result.append((i,j))
                    elif chess_board.__contains__((i + 1,self.y)) == False:
                        result.append((i,j))

        if to_checkmate:
             return result
        else:
            super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate,to_checkmate)