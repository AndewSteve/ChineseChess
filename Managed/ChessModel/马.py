import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 马(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"马.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"馬.png")
        super().init(position)
        
    def onSelected(self,chess_board:dict[(int,int),Chess],BLACK_checkmate,RED_checkmate):

        result = []

        top_max, button_max = 0, 9
        left_max, right_max = 0, 8
        self_posi = pygame.math.Vector2(self.x, self.y)
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

        super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate)