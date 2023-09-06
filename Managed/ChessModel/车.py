import os,pygame
from .Chess import Chess,ChessColor,chess_img_path

class 车(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"车.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"車.png")
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
        if(self.color==ChessColor.RED):
            #向左走
            for i in range(self.x):
                if(chess_board.__contains__((self.x-i-1,self.y))==False ):
                    result.append(
                            (self.x-i-1,self.y),
                    )
                elif(chess_board[(self.x-i-1,self.y)].color==ChessColor.BLACK):
                    result.append(
                            (self.x-i-1,self.y),
                    )
                    break
                elif(chess_board[(self.x-i-1,self.y)].color==ChessColor.RED):
                    break
            #向右走
            for i in range(8-self.x):
                if(chess_board.__contains__((self.x+i+1,self.y))==False ):
                    result.append(
                            (self.x+i+1,self.y),
                    )
                elif(chess_board[(self.x+i+1,self.y)].color==ChessColor.BLACK):
                    result.append(
                            (self.x+i+1,self.y),
                    )
                    break
                elif(chess_board[(self.x+i+1,self.y)].color==ChessColor.RED):
                    break
            #向上走
            for i in range(self.y):
                if(chess_board.__contains__((self.x,self.y-i-1))==False ):
                    result.append(
                            (self.x,self.y-i-1),
                    )
                elif(chess_board[(self.x,self.y-i-1)].color==ChessColor.BLACK):
                    result.append(
                            (self.x,self.y-i-1),
                    )
                    break
                elif(chess_board[self.x,self.y-i-1].color==ChessColor.RED):
                    break
            #向下走
            for i in range(9-self.y):
                if(chess_board.__contains__((self.x,self.y+i+1))==False ):
                    result.append(
                            (self.x,self.y+i+1),
                    )
                elif(chess_board[(self.x,self.y+i+1)].color==ChessColor.BLACK):
                    result.append(
                            (self.x,self.y+i+1),
                    )
                    break
                elif(chess_board[self.x,self.y+i+1].color==ChessColor.RED):
                    break
        if(self.color==ChessColor.BLACK):
            #向左走
            for i in range(self.x):
                if(chess_board.__contains__((self.x-i-1,self.y))==False ):
                    result.append(
                            (self.x-i-1,self.y),
                    )
                elif(chess_board[(self.x-i-1,self.y)].color==ChessColor.RED):
                    result.append(
                            (self.x-i-1,self.y),
                    )
                    break
                elif(chess_board[(self.x-i-1,self.y)].color==ChessColor.BLACK):
                    break
            #向右走
            for i in range(8-self.x):
                if(chess_board.__contains__((self.x+i+1,self.y))==False ):
                    result.append(
                            (self.x+i+1,self.y),
                    )
                elif(chess_board[(self.x+i+1,self.y)].color==ChessColor.RED):
                    result.append(
                            (self.x+i+1,self.y),
                    )
                    break
                elif(chess_board[(self.x+i+1,self.y)].color==ChessColor.BLACK):
                    break
            #向上走
            for i in range(self.y):
                if(chess_board.__contains__((self.x,self.y-i-1))==False ):
                    result.append(
                            (self.x,self.y-i-1),
                    )
                elif(chess_board[(self.x,self.y-i-1)].color==ChessColor.RED):
                    result.append(
                            (self.x,self.y-i-1),
                    )
                    break
                elif(chess_board[self.x,self.y-i-1].color==ChessColor.BLACK):
                    break
            #向下走
            for i in range(9-self.y):
                if(chess_board.__contains__((self.x,self.y+i+1))==False ):
                    result.append(
                            (self.x,self.y+i+1),
                    )
                elif(chess_board[(self.x,self.y+i+1)].color==ChessColor.RED):
                    result.append(
                            (self.x,self.y+i+1),
                    )
                    break
                elif(chess_board[self.x,self.y+i+1].color==ChessColor.BLACK):
                    break     
        for posi in result:
            x,y = posi
            print(f"{x}_{y}")
            
        if to_checkmate:
             return result
        else:
            super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate)