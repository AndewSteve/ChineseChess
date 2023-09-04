import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 马(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"马.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"馬.png")
        super().init(position)
        
    def onSelected(self):
        return super().onSelected()