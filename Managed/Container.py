import pygame
from Managed.ChessModel import Chess,ChessColor,卒,象,士,炮,马,将,车
import json
from Managed.Game import Dict_to_Abs_posi
class Container:
    chess_board:dict[(int,int),Chess] = {}

    def __init__(self):
        self.sprite_group = pygame.sprite.Group()
        self.load_chess_board()
        self.initChessBoard()
    
    def initChessBoard(self):
        for posi,chess in self.chess_board.items():
            abs_posi = Dict_to_Abs_posi(posi)
            chess.init(abs_posi)
            self.sprite_group.add(chess)
        print("初始化棋子")

    def update_abs_posi(self):
        for posi,chess in self.chess_board.items():
            abs_posi = Dict_to_Abs_posi(posi)
            chess.move(abs_posi)

    def updateChess(self,old_posi,new_posi,chess):
        if self.chess_board.__contains__(old_posi):
            if not chess:
                chess = self.chess_board[old_posi]
            self.chess_board.pop(old_posi)
        self.chess_board[new_posi] = chess


    def deleteChess(self,posi,chess):
        if self.chess_board.__contains__(posi):
            if not chess:
                chess = self.chess_board[posi]
            self.chess_board.pop(posi)
        chess.onDestroyed()
        

    def load_chess_board(self,filename = "./save/save00.json"):
        self.chess_board={}
        with open(filename, "r") as file:
            saved_dict = json.load(file)
            for saved_key, saved_value in saved_dict.items():
                x,y = map(int, saved_key.split('_'))
                class_name,chess_color = saved_value.split('_')
                chess_class = globals()[class_name]
                self.chess_board[(x,y)] = chess_class(ChessColor(int(chess_color)))
        self.initChessBoard()
        print(f"导入存档:{filename}")

    def save_chess_board(self,filename = "./save/save00.json"):
        with open(filename, "w") as file:
            new_dict = {}
            for key, value in self.chess_board.items():
                x,y = key
                new_key = f"{x}_{y}"
                new_value = f"{value.__class__.__name__}_{value.color.value}"
                new_dict[new_key] = new_value
            json.dump(new_dict, file,indent=4,ensure_ascii=False)
        print(f"保存存档:{filename}")


def custom_encoder(obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            if isinstance(key, tuple):
                key_list = list(key)
                new_dict[key_list] = value
            else:
                new_dict[key] = value
        return new_dict
def custom_decoder(obj):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            if isinstance(key, list):
                key_tuple = tuple(key)
                new_dict[key_tuple] = value
            else:
                new_dict[key] = value
        return new_dict
    

def initMap(board):
    board[(0, 0)] = 车(ChessColor.RED)
    board[(1, 0)] = 马(ChessColor.RED)
    board[(2, 0)] = 象(ChessColor.RED)
    board[(3, 0)] = 士(ChessColor.RED)

    board[(4, 0)] = 将(ChessColor.RED)

    board[(5, 0)] = 士(ChessColor.RED)
    board[(6, 0)] = 象(ChessColor.RED)
    board[(7, 0)] = 马(ChessColor.RED)
    board[(8, 0)] = 车(ChessColor.RED)

    board[(0, 3)] = 卒(ChessColor.RED)
    board[(1, 2)] = 炮(ChessColor.RED)
    board[(2, 3)] = 卒(ChessColor.RED)
    board[(4, 3)] = 卒(ChessColor.RED)
    board[(6, 3)] = 卒(ChessColor.RED)
    board[(7, 2)] = 炮(ChessColor.RED)
    board[(8, 3)] = 卒(ChessColor.RED)


    board[(0, 6)] = 卒(ChessColor.BLACK)
    board[(1, 7)] = 炮(ChessColor.BLACK)
    board[(2, 6)] = 卒(ChessColor.BLACK)
    board[(4, 6)] = 卒(ChessColor.BLACK)
    board[(6, 6)] = 卒(ChessColor.BLACK)
    board[(7, 7)] = 炮(ChessColor.BLACK)
    board[(8, 6)] = 卒(ChessColor.BLACK)


    board[(0, 9)] = 车(ChessColor.BLACK)
    board[(1, 9)] = 马(ChessColor.BLACK)
    board[(2, 9)] = 象(ChessColor.BLACK)
    board[(3, 9)] = 士(ChessColor.BLACK)

    board[(4, 9)] = 将(ChessColor.BLACK)

    board[(5, 9)] = 士(ChessColor.BLACK)
    board[(6, 9)] = 象(ChessColor.BLACK)
    board[(7, 9)] = 马(ChessColor.BLACK)
    board[(8, 9)] = 车(ChessColor.BLACK)

    # container.save_chess_board("./save/__init__.json")




# if __name__ =='__main__':
#     #共享单例
#     container = Container()
#     container.load_chess_board()
#     print("导入存档:save00.json")
