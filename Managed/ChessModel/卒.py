import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 卒(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"兵.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"卒.png")
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
        if(self.color==ChessColor.BLACK):
            if(self.y>4):
                if(self.x==0 and self.y==9):
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )
                elif(self.x==8 and self.y==9):
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                        )
                elif(self.x==0):
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )
                    if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x+1,self.y+1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y+1),
                        )
                elif(self.x==8):
                    if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x+1,self.y+1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y+1),
                        )
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                        )
                elif(self.y==9):
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                        )
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )        
                else:
                    if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x-1,self.y),
                        )
                    if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.RED):
                            result.append(
                                (self.x+1,self.y),
                        )  
                    if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x,self.y+1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y+1),
                        )
            else:
                if(chess_board.__contains__((self.x,self.y+1))==False or chess_board[(self.x,self.y+1)].color==ChessColor.RED):
                            result.append(
                                (self.x,self.y+1),
                        )
        elif(self.color==ChessColor.RED):
            if(self.y<5):
                    if(self.x==self.y==0):
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )
                    elif(self.x==8 and self.y==0):
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                            )
                    elif(self.x==0):
                        if(chess_board.__contains__((self.x,self.y-1))==False or chess_board[(self.x,self.y-1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y-1),
                            )
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )
                    elif(self.x==8):
                        if(chess_board.__contains__((self.x,self.y-1))==False or chess_board[(self.x,self.y-1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y-1),
                            )
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                            )
                    elif(self.y==0):
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                            )
                    else:
                        if(chess_board.__contains__((self.x+1,self.y))==False or chess_board[(self.x+1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x+1,self.y),
                        )
                        if(chess_board.__contains__((self.x-1,self.y))==False or chess_board[(self.x-1,self.y)].color==ChessColor.BLACK):
                            result.append(
                                (self.x-1,self.y),
                            )
                        if(chess_board.__contains__((self.x,self.y-1))==False or chess_board[(self.x,self.y-1)].color==ChessColor.BLACK):
                            result.append(
                                (self.x,self.y-1),
                            )                     
            else:   
                result.append(
                      (self.x,self.y-1),
                )

                
        if to_checkmate:
             return result
        else:
            super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate,to_checkmate)