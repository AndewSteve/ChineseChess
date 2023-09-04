import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 卒(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"兵.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"卒.png")
        super().init(position)
        
    def onSelected(self):
        drop_point_list=[(4,4)]
        Eatable = False

        
        chess_board:dict[(int,int),Chess] = {}
        for posi,chess in chess_board.items():
            if chess is Eatable:
                flag = True


        super().onSelected(drop_point_list)