import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
from Managed.Game import scale_img

class 将(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"帅.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"将.png")
        super().init(position)

    def onSelected(self):
        return super().onSelected()