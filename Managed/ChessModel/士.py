import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 士(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"士.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"仕.png")
        super().init(position)
        
    def onSelected(self,chess_board:dict[(int,int),Chess]):
        result = []

        top_max ,button_max = 7,9
        left_max,right_max = 3,5
        self_posi = pygame.math.Vector2(self.x,self.y)
        if self.color == ChessColor.RED:
            top_max ,button_max = 0,2

        ori = pygame.math.Vector2((left_max+right_max)/2,(top_max+button_max)/2)
        self_magnitude = (ori-self_posi).length()
    
        pre_select = [(self.x+1,self.y+1),
                      (self.x+1,self.y),
                      (self.x+1,self.y-1),
                      (self.x,self.y+1),
                      (self.x,self.y-1),
                      (self.x-1,self.y+1),
                      (self.x-1,self.y),
                      (self.x-1,self.y-1),]


        for i in range(left_max,right_max+1):
            for j in range(top_max,button_max+1):
                if (i,j) in pre_select:
                    pre_magnitude = (ori-pygame.math.Vector2(i,j)).length()
                    if pre_magnitude == self_magnitude:
                        continue
                    if chess_board.__contains__((i,j))==False or chess_board[(i,j)].color!=self.color:
                        result.append((i,j))


        super().onSelected(result,chess_board)