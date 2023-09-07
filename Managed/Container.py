import pygame
from Managed.ChessModel import Chess,DropPoint,ChessColor,卒,象,士,炮,马,将,车
import json
from Managed.Game import Dict_to_Abs_posi
from Managed.Mixer import Mixer
game_init_path = "./save/__init__.json"
game_save_path = "./save/save00.json"
game_load_path = "./save/save00.json"

class Container:
    chess_board:dict[(int,int),Chess] = {}
    selected_chess:Chess = None
    RED_checkmate:Chess = None
    BLACK_checkmate:Chess = None
    checkmated_Team:ChessColor = None
    mixer:Mixer = None
    def __init__(self):
        self.chess_sprite_group = pygame.sprite.Group()
        self.load_chess_board()
        self.initChessBoard()
    
    def setMixer(self,mixer):
        self.mixer = mixer

    def initChessBoard(self):
        """初始化棋子图片,记录将帅位置
        """
        for posi,chess in self.chess_board.items():
            chess.init(posi)
            self.chess_sprite_group.add(chess)
            if isinstance(chess,将):
                if chess.color == ChessColor.RED:
                    self.RED_checkmate = chess
                elif chess.color == ChessColor.BLACK:
                    self.BLACK_checkmate = chess
        print("初始化棋子")

    def check_and_drop_chess(self,abs_posi):
        """对当前选中的棋子落点碰撞检测,点中落点后会删除选中棋子的引用


        Args:
            abs_posi (tuple): 鼠标位置
        """
        abs_x,abs_y = abs_posi
        for dict_posi,drop_sprite in self.selected_chess.drop_point_dict.items():
            if drop_sprite.rect.collidepoint(abs_x,abs_y):
                x,y = dict_posi

                if not self.checkmated_Team == None:
                    if self.Guard(self.selected_chess,dict_posi,self.selected_chess.color):
                        del self.checkmated_Team
                    else:
                        return False
                elif not self.Guard(self.selected_chess,dict_posi,self.selected_chess.color):
                    return False

                if self.chess_board.__contains__(dict_posi):
                    chess_destroyed = self.chess_board[dict_posi]
                    self.updateChess(chess_destroyed,(-10,-10))
                    chess_destroyed.move((-10,-10))
                    self.mixer.play("吃子声")
                    #print(f"棋子{chess_destroyed.__class__.__name__}被吃掉了")
                    if chess_destroyed is self.BLACK_checkmate:
                        self.BLACK_checkmate = None
                    elif chess_destroyed is self.RED_checkmate:
                        self.RED_checkmate = None

                self.updateChess(self.selected_chess,dict_posi)
                self.selected_chess.move(dict_posi)

                if self.checkmate(self.selected_chess):
                    self.checkmated_Team = (ChessColor.RED if self.selected_chess.color == ChessColor.BLACK else ChessColor.BLACK)


                del self.selected_chess.drop_point_dict
                #print(f"棋子{self.selected_chess.__class__.__name__}落到{x}_{y}")
                del self.selected_chess.drop_sprite_group
                del self.selected_chess
        return True


    
    

    def check_and_select_chess(self,posi,action_team):
        """对棋盘所有棋子碰撞检测,点中行动方棋子会添加selected_chess引用

        Args:
            posi (_type_): 鼠标位置
            action_team (_type_): 当前行动方

        Returns:
            Boolean: 是否有选中棋子
        """
        x,y =posi
        for dict_posi,chess in self.chess_board.items():
            dict_x,dict_y = dict_posi
            if chess.rect.collidepoint(x,y):
                #print(f"现在碰撞的棋子是{chess.__class__.__name__},阵营是{chess.color},正在行动的阵营是{action_team},两者是否相等：{chess.color.value == action_team.value}")
                if not chess.color.value == action_team.value:
                    continue
                if not self.selected_chess == None:
                    del self.selected_chess.drop_sprite_group
                    del self.selected_chess
                #print(f"点击到棋子{chess.__class__.__name__}:({dict_x},{dict_y})")
                self.selected_chess = chess
                chess.onSelected(self.chess_board,self.BLACK_checkmate,self.RED_checkmate,to_checkmate = False)
                return True
        return False

    def checkmate(self,chess:Chess):
        target = (self.RED_checkmate if chess.color == ChessColor.BLACK else self.BLACK_checkmate)
        pre_drops = chess.onSelected(self.chess_board,self.BLACK_checkmate,self.RED_checkmate,to_checkmate = True)
        for pre_drop in pre_drops:
            if self.chess_board.__contains__(pre_drop) and self.chess_board[pre_drop] is target:
                return True
        return False
    
    def Guard(self,chess:Chess,pre_drop,guard_team):
        result = True

        ori_posi = chess.x,chess.y

        destroyed_spawn = self.chess_board.__contains__(pre_drop)
        temp_chess_destroyed = None

        if destroyed_spawn:
            temp_chess_destroyed = self.chess_board[pre_drop]
            self.chess_board.pop(pre_drop)
            temp_chess_destroyed.move((-10,-10))
        self.updateChess(chess,pre_drop)

        for _,enemy in self.chess_board.items():
            if not enemy.color == guard_team:
                if self.checkmate(enemy):
                    result = False
                    break


        if self.chess_board.__contains__(pre_drop):
            self.chess_board.pop(pre_drop)
        self.chess_board[ori_posi] = chess

        if destroyed_spawn:
            temp_chess_destroyed.move(pre_drop)
            self.updateChess(temp_chess_destroyed,pre_drop)

        return result


    def update_abs_posi(self):
        """更新所有棋子的屏幕坐标
        """
        for posi,chess in self.chess_board.items():
            abs_posi = Dict_to_Abs_posi(posi)
            chess.rect.center = abs_posi

    def updateChess(self,chess:Chess,new_posi):
        """更新棋盘字典

        Args:
            chess (Chess): 棋子对象
            new_posi (tuple): 新的逻辑坐标
        """
        old_posi = (chess.x,chess.y)
        if self.chess_board.__contains__(old_posi):
            self.chess_board.pop(old_posi)
        self.chess_board[new_posi] = chess


    def deleteChess(self,posi):
        """删除字典中的棋子(未使用)

        Args:
            posi (tuple): 棋子逻辑位置
        """
        if self.chess_board.__contains__(posi):
            chess = self.chess_board[posi]
            self.chess_board.pop(posi)
            chess.onDestroyed()
        

    def load_chess_board(self,remake = False,filename = game_load_path):
        """从json文件中加载存档

        Args:
            filename (str, optional): 默认加载save00.json. Defaults to game_load_path.
        """
        self.chess_board={}
        self.chess_sprite_group.empty()
        self.selected_chess = None
        if remake:
            filename = game_init_path
        with open(filename, "r") as file:
            saved_dict = json.load(file)
            for saved_key, saved_value in saved_dict.items():
                x,y = map(int, saved_key.split('_'))
                class_name,chess_color = saved_value.split('_')
                chess_class = globals()[class_name]
                self.chess_board[(x,y)] = chess_class(ChessColor(int(chess_color)))
        self.initChessBoard()
        print(f"导入存档:{filename}")

    def save_chess_board(self,filename = game_save_path):
        """保存存档到json文件

        Args:
            filename (str, optional): 默认保存到save00. Defaults to game_save_path.
        """
        with open(filename, "w") as file:
            new_dict = {}
            for key, value in self.chess_board.items():
                x,y = key
                new_key = f"{x}_{y}"
                new_value = f"{value.__class__.__name__}_{value.color.value}"
                new_dict[new_key] = new_value
            json.dump(new_dict, file,indent=4,ensure_ascii=False)
        print(f"保存存档:{filename}")
        return True


def initMap(board):
    """自定义棋盘
    """
    board:dict[(int,int),Chess] = {}
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

    # container.chess_board = board()
    # container.initChessBoard()
    # container.save_chess_board("./save/__init__.json")




# if __name__ =='__main__':
#     #共享单例
#     container = Container()
#     container.load_chess_board()
#     print("导入存档:save00.json")
