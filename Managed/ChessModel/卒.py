import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 卒(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"兵.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"卒.png")
        super().init(position)
        
    def onSelected(self,chess_board:dict[(int,int),Chess]):
        drop_point_list=[(4,4)]
        Eatable = False
        for posi,chess in chess_board.items():
            if chess is Eatable:
                flag = True
        chess_board.__contains__

        result = []
        
        top_max ,button_max = 0,9
        left_max,right_max = 0,8
        self_posi = pygame.math.Vector2(self.x,self.y)
        
        pre_selectred = [(self.x+1,self.y),
                      (self.x,self.y+1),
                      (self.x-1,self.y)]
        
        pre_selectblack = [(self.x+1,self.y),
                      (self.x,self.y-1),
                      (self.x-1,self.y)]
        
        if(self.color==ChessColor.RED):
            if(self.y>4):
                if(self.x==0 and self.y==9):
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )
                elif(self.x==8 and self.y==9):
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                        )
                elif(self.x==0):
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )
                    if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x+1,self.y+1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y+1),
                        )
                elif(self.x==8):
                    if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x+1,self.y+1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y+1),
                        )
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                        )
                elif(self.y==9):
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                        )
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )        
                else:
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                        )
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )  
                    if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x+1,self.y+1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y+1),
                        )
            else:
                if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x+1,self.y+1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y+1),
                        )
        elif(self.color==ChessColor.BLACK):
            if(self.y<5):
                    if(self.x==self.y==0):
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )
                    elif(self.x==8 and self.y==0):
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                            )
                    elif(self.x==0):
                        if(chess_board.__contains__((self.x,self.y-1))==False or chess_board[(self.x,self.y-1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y-1),
                            )
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )
                    elif(self.x==8):
                        if(chess_board.__contains__((self.x,self.y-1))==False or chess_board[(self.x,self.y-1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y-1),
                            )
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                            )
                    elif(self.y==0):
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                            )
                    else:
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                            )
                        if(chess_board.__contains__((self.x,self.y-1))==False or chess_board[(self.x,self.y-1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y-1),
                            )                     
            else:   
                result.append(
                      (self.x,self.y-1),
                )

        for posi in result:
            x,y = posi
            print(f"{x}_{y}")


        super().onSelected(result,chess_board)