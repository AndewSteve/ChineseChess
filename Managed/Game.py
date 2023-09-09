from enum import Enum
import os
import pygame
from pygame.locals import *
from Managed.Mixer import Mixer
from Managed.ChessModel.ChessColor import ChessColor



#region 视窗常量
#渲染图层
CHESS_LAYER = 4#棋子层
DROP_POINT_LAYER = 3#落点层
#endregion



class Game:
    def __init__(self):
        self.mixer = Mixer()
        pygame.display.set_caption("中国象棋")  # 设置游戏名字
        self.game_running = True

    def setContainer(self,container):
        from Managed.Container import Container
        self.container :Container = container
        self.container.setMixer(self.mixer)

    def setWindow(self,window):
        from Managed.Window import Window
        self.window :Window = window

    def run(self):
        self.window.init_Screen()
        while self.game_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_posi = pygame.mouse.get_pos()
                    if self.window.log_surface_rect.collidepoint(mouse_posi):
                        self.MenuClickEven(mouse_posi)
                    elif not self.window.game_over:
                        self.ChessBoardClickEvent(mouse_posi)
            self.window.blit_Screen()
        pygame.quit()

    def ChessBoardClickEvent(self,mouse_posi):
        if not self.container.selected_chess:#在没有选中棋子的情况下
            if self.container.check_and_select_chess(mouse_posi,self.window.Action_team):#选择到棋子
                selected_chess = self.container.selected_chess
                self.window.all_sprites.add(selected_chess.drop_sprite_group,layer = DROP_POINT_LAYER)#添加落点展示

        else:#在已经有选中的棋子的情况下
            if self.container.selected_chess.rect.collidepoint(mouse_posi):#如果点击到当前选中的棋子，取消选择
                self.window.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                del self.container.selected_chess.drop_sprite_group
                del self.container.selected_chess

            elif not self.container.check_and_drop_chess(mouse_posi):#落点失败的情况
                if not self.container.checkmated_Team == None:
                    self.window.log_info(f"{self.container.checkmated_Team.name}正在被将军")
                    self.window.log_info(f"请先防守")
                else:
                    self.window.log_info(f"不能自杀")
            elif not self.container.selected_chess:#落点成功的情况
                self.window.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)#清空落点
                if self.container.RED_checkmate == None or self.container.BLACK_checkmate == None:#有将死
                    self.window.game_over = True
                    self.window.log_info(f"游戏结束，{self.window.Action_team.name}胜利")
                    print(f"游戏结束，{self.window.Action_team}胜利")
                    self.window.game_saved = True
                    self.mixer.play("Apex")
                else:
                    if self.container.checkmated_Team:#有一方被将军
                        self.window.checkmated_team = self.container.checkmated_Team
                        self.window.log_info(f"{self.window.checkmated_team.name}被将军")

                    self.window.Action_team = (ChessColor.RED if self.window.Action_team == ChessColor.BLACK else ChessColor.BLACK)#换手
                    self.window.action_timer = 0
                    self.window.log_info(f"现在是{self.window.Action_team.name}的回合")
                    self.window.game_saved = False
            
            elif self.container.check_and_select_chess(mouse_posi,self.window.Action_team):#重新选择友方棋子
                self.window.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                selected_chess = self.container.selected_chess
                self.window.all_sprites.add(selected_chess.drop_sprite_group,layer = DROP_POINT_LAYER)


    #右侧菜单
    def MenuClickEven(self,mouse_posi):
        if self.window.icon_dict["save"].rect.collidepoint(mouse_posi):
            if (not self.window.game_over) and (self.container.save_chess_board(action_team=self.window.Action_team)):
                self.window.game_saved = True
                self.window.log_info("已将存档保存到save00")
            else:
                self.window.log_info("不允许保存死局,或发生文件错误")
        elif self.window.icon_dict["quit"].rect.collidepoint(mouse_posi):
            if not self.window.game_saved:
                self.window.log_info("游戏未保存,是否要退出?")
                self.window.log_info("(退出请直接结束程序)")
            else:
                self.game_running = False
        elif self.window.icon_dict["remake"].rect.collidepoint(mouse_posi):
            self.container.load_chess_board(remake= True)
            self.window.all_sprites.remove_sprites_of_layer(CHESS_LAYER)
            self.window.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
            self.window.all_sprites.empty()
            self.window.all_sprites.add(self.container.chess_sprite_group,layer = CHESS_LAYER)
            self.window.init_Screen()
            self.window.Action_team = ChessColor.RED
            self.window.log_info(f"现在是{self.window.Action_team.name}的回合")
            self.window.action_timer = 0
            self.window.game_over = False
            
