from ChessModel import Chess,ChessColor,卒,象,士,炮,马,将,车
import json
#from Game import game
class Container():
    chess_board:dict[(int,int),Chess] = {}
    def __init__(self):
        pass
    
    def load_chess_board(self,filename = "../save/__init__.json"):
        with open(filename, "r") as file:
            self.chess_board = json.load(file)

    def save_chess_board(self,filename = "../save/save00.json"):
        with open(filename, "w") as file:
            json.dump(self.chess_board, file)

#共享单例
container = Container()

if __name__ =='__main__':
    board = container.chess_board
    board[(0, 0)] = 车(ChessColor.RED)
    board[(0, 1)] = 马(ChessColor.RED)
    board[(0, 2)] = 象(ChessColor.RED)
    board[(0, 3)] = 士(ChessColor.RED)

    board[(0, 4)] = 将(ChessColor.RED)

    board[(0, 5)] = 士(ChessColor.RED)
    board[(0, 6)] = 象(ChessColor.RED)
    board[(0, 7)] = 马(ChessColor.RED)
    board[(0, 0)] = 车(ChessColor.RED)
    print(board.__contains__((0,3)))
    print(container.chess_board.__contains__((0,3)))
