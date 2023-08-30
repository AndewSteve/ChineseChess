from . import ChessModel
class Container():
    chess_boar:dict[(int,int),Chess] = {}
    def __init__(self):
        pass

#共享单例
container = Container()