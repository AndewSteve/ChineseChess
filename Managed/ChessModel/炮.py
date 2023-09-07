import os,pygame
from .Chess import Chess,ChessColor,chess_img_path
class 炮(Chess):
    def init(self, position):
        if(self.color==ChessColor.RED):
            self.chess_img_path = os.path.join(chess_img_path,"砲.png")
        else:
            self.chess_img_path = os.path.join(chess_img_path,"炮.png")
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

        top_max, button_max = 0, 9
        left_max, right_max = 0, 8
        self_posi = pygame.math.Vector2(self.x, self.y)
        # if self.color == ChessColor.RED:
        #     top_max, button_max = 0, 4

        ori = pygame.math.Vector2((left_max + right_max) / 2, (top_max + button_max) / 2)
        self_magnitude = (ori - self_posi).length()
        pre_select = []
        if self.y < 8:
          for i in range(self.y + 1 , 9): #中到下
            if chess_board.__contains__((self.x,i)) == False: #路上无子
                if i < 8:
                 result.append((self.x, i))
                if i == 8 and chess_board.__contains__((self.x, 9)) == False:
                    result.append((self.x, 9))
                    result.append((self.x, 8))
                elif  i == 8 and chess_board.__contains__((self.x, 9)) == True:
                    result.append((self.x, 8))

            elif chess_board.__contains__((self.x,i)) == True: #路上有子
                for j in range(i + 1, 10):
                    if chess_board.__contains__((self.x,j)) == True : #路上有第二子
                        if chess_board[(self.x,j)].color == self.color: #第二子为友方
                            break
                        elif chess_board[(self.x,j)].color != self.color: #第二子为敌方
                            result.append((self.x,j))
                            break
                    elif chess_board.__contains__((self.x,j)) == False: #路上无第二子
                        continue
                break


        elif self.y == 8:
            if chess_board.__contains__((self.x,9)) == False:
                result.append((self.x,9))
        if self.y > 1:
          for i in range(self.y - 1 , 0 , -1): #中到上

            if chess_board.__contains__((self.x,i)) == False: #路上无子
                if i > 1:
                    result.append((self.x,i))
                if i == 1 and chess_board.__contains__((self.x, 0)) == False:
                    result.append((self.x, 0))
                    result.append((self.x, 1))
                elif i == 1 and chess_board.__contains__((self.x, 0)) == True:
                    result.append((self.x, 1))
            elif chess_board.__contains__((self.x,i)) == True: #路上有子
                for j in range(i - 1, -1, -1):
                    if chess_board.__contains__((self.x,j)) == True : #路上有第二子
                        if chess_board[(self.x,j)].color == self.color: #第二子为友方
                            break
                        elif chess_board[(self.x,j)].color != self.color: #第二子为敌方
                            result.append((self.x,j))
                            break
                    elif chess_board.__contains__((self.x,j)) == False: #路上无第二子
                        continue
                break

        elif self.y == 1:
            if chess_board.__contains__((self.x,0)) == False:
                result.append((self.x,0))

        if self.x > 1:
          for i in range(self.x - 1 , 0 , -1): #中到左
            if chess_board.__contains__((i,self.y)) == False: #路上无子
                if i > 1:
                    result.append((i, self.y))
                if i == 1 and chess_board.__contains__((0, self.y)) == False:
                    result.append((1, self.y))
                    result.append((0, self.y))
                elif i == 1 and chess_board.__contains__((0, self.y)) == True:
                    result.append((1, self.y))
            elif chess_board.__contains__((i,self.y)) == True: #路上有子
                for j in range(i - 1, -1, -1):
                    if chess_board.__contains__((j,self.y)) == True : #路上有第二子
                        if chess_board[(j,self.y)].color == self.color: #第二子为友方
                            break
                        elif chess_board[(j,self.y)].color != self.color: #第二子为敌方
                            result.append((j,self.y))
                            break
                    elif chess_board.__contains__((j,self.y)) == False: #路上无第二子
                        continue
                break

        elif self.x == 1:
            if chess_board.__contains__((0,self.y)) == False:
                result.append((0,self.y))
        if self.x < 7:
          for i in range(self.x + 1 , 8): #中到右
            if chess_board.__contains__((i,self.y)) == False: #路上无子
                if i<7:
                  result.append((i,self.y))
                if i==7 and chess_board.__contains__((8,self.y)) == False:
                    result.append((7,self.y))
                    result.append((8,self.y))
                elif i==7 and chess_board.__contains__((8,self.y)) == True:
                    result.append((7,self.y))

            elif chess_board.__contains__((i,self.y)) == True: #路上有子
                for j in range(i + 1, 9):
                    if chess_board.__contains__((j,self.y)) == True : #路上有第二子
                        if chess_board[(j,self.y)].color == self.color: #第二子为友方
                            break
                        elif chess_board[(j,self.y)].color != self.color: #第二子为敌方
                            result.append((j,self.y))
                            break
                    elif chess_board.__contains__((j,self.y)) == False: #路上无第二子
                        continue
                break
        elif self.x == 7:
            if chess_board.__contains__((8,self.y)) == False:
                result.append((8,self.y))


        if to_checkmate:
             return result
        else:
            super().onSelected(result,chess_board,BLACK_checkmate,RED_checkmate,to_checkmate)