import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
from Managed.Game import scale_img
class 炮(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"砲.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"炮.png")
        self.image = pygame.image.load(self.chess_img_path)
        self.image = scale_img(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.x,self.y = position
        
    def onSelected(self):
        return super().onSelected()