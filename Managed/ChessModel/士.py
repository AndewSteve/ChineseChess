import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 士(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"士.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"仕.png")
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

        possible = [(3,0),(5,0),(4,1),(3,2),(5,2)]

        if self.color == ChessColor.RED:
            for i in range(len(possible)):
                x,y = possible[i]
                possible[i] = x,y+7

        around = [(self.x+1,self.y+1),
                  (self.x+1,self.y-1),
                  (self.x-1,self.y+1),
                  (self.x-1,self.y-1),]

        for posi in around:
            if possible.__contains__(posi):
                if chess_board.__contains__(posi)==False or chess_board[posi].color!=self.color:
                        result.append(posi)


        if to_checkmate:
             return result
        else:
            super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate)