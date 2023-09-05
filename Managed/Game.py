from enum import Enum
import os
import pygame
from pygame.locals import *

chessBoard_img_path = './Resource/img/ChessBoard'
icon_path = './Resource/img/icon'
chessBoard_img = 'chessboard.png'
backGround_img = 'background.jpg'
team_tip_img = '走棋.png'
victory_tip_img = '获胜.png'
failed_tip_img = '败北.png'
front_path = './Resource/front/LiuGongQuanBiaoZhunKaiShu-2.ttf'
# 视窗大小
GAME_WIDTH,GAME_HEIGHT = 1200,780

#提示窗口大小
TIP_WIDTH,TIP_HEIGHT = 300,780
TIP_TEAM_X,TIP_TEAM_Y_BLACK,TIP_TEAM_Y_RED = TIP_WIDTH//3,TIP_HEIGHT/1.5,TIP_HEIGHT//6
ACTION_TIP_ORI_BLACK,ACTION_TIP_ORI_RED = (TIP_TEAM_X,TIP_TEAM_Y_BLACK),(TIP_TEAM_X,TIP_TEAM_Y_RED)
TIP_TEAM_SIZE_X,TIP_TEAM_SIZE_Y = 180,120

#日志窗口大小
LOG_WIDTH,LOG_HEIGHT = TIP_WIDTH,TIP_HEIGHT
#日志窗口原点
LOG_ORI = 900,0

#棋盘窗口大小
CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT = 600, 660
GAMEOVER_TIP_SIZE_X,GAMEOVER_TIP_SIZE_Y = CHESSBOARD_WIDTH//5,CHESSBOARD_HEIGHT//4
GAMEOVER_TIP_ORI_RED,GAMEOVER_TIP_ORI_BLACK = (500,480),(500,120)
#棋盘窗口原点
CHESSBOARD_ORI = 300,60
#每个格子的大小
CHESS_SIZE_X,CHESS_SIZE_Y = 60,60
#游戏左上角到第一个棋子间的位置差
OFFSET_X,OFFSET_Y = 360,120

def update_global_val(game_WIDTH, game_HEIGHT):
    global GAME_WIDTH,GAME_HEIGHT,TIP_WIDTH,TIP_HEIGHT,LOG_WIDTH,LOG_HEIGHT,LOG_ORI,CHESSBOARD_ORI,OFFSET_X,OFFSET_Y
    GAME_WIDTH,GAME_HEIGHT = game_WIDTH, game_HEIGHT
    TIP_WIDTH,TIP_HEIGHT = (GAME_WIDTH - CHESSBOARD_WIDTH)//2,GAME_HEIGHT
    LOG_WIDTH,LOG_HEIGHT = TIP_WIDTH,TIP_HEIGHT
    LOG_ORI = (TIP_WIDTH + GAME_WIDTH),0
    CHESSBOARD_ORI = TIP_WIDTH,(GAME_HEIGHT-CHESSBOARD_HEIGHT)//2
    OFFSET_X,OFFSET_Y = (TIP_WIDTH + CHESS_SIZE_X),(GAME_HEIGHT-CHESSBOARD_HEIGHT)//2 + CHESS_SIZE_Y

#渲染图层
CHESS_LAYER = 4
DROP_POINT_LAYER = 3


class ActionTeam(Enum):
    RED = 1
    BLACK = 2

class Game:
    Action_team :ActionTeam= None
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(front_path, 20)
        pygame.display.set_caption("中国象棋")  # 设置游戏名字
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.clock = pygame.time.Clock()
        self.Action_team  = ActionTeam.BLACK
        self.game_over = False

    def setContainer(self,container):
        self.container :Container = container
        self.all_sprites.add(self.container.chess_sprite_group,layer = CHESS_LAYER)

    def run(self):
        self.updateScreenScale()
        self.log_info(f"现在是{self.Action_team.name}的回合")
        self.update()
        while True:
            if self.game_over:
                self.update(self.game_over)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if not self.game_over:
                        self.clickEvent()
                elif event.type == VIDEORESIZE:
                    temp_WIDTH, temp_HEIGHT = event.size[0], event.size[1]
                    if temp_WIDTH>900 and temp_HEIGHT>660:
                        update_global_val(temp_WIDTH, temp_HEIGHT)
                        self.updateScreenScale()
                        self.update()
            self.clock.tick(60)
            pygame.display.flip()

    def clickEvent(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        if self.container.selected_chess == None:#现在没有选中棋子
            if self.container.check_and_select_chess((mouse_x,mouse_y),self.Action_team):
                selected_chess = self.container.selected_chess
                self.all_sprites.add(selected_chess.drop_sprite_group,layer = 3)#添加落点展示
        else:
            self.container.check_and_drop_chess((mouse_x,mouse_y))
            if self.container.selected_chess == None:
                self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                if self.container.RED_checkmate == None or self.container.BLACK_checkmate == None:
                    self.game_over = True
                    self.log_info(f"游戏结束，{self.Action_team.name}胜利")
                    print(f"游戏结束，{self.Action_team}胜利")
                else:
                    self.Action_team = (ActionTeam.RED if self.Action_team == ActionTeam.BLACK else ActionTeam.BLACK)
                    self.log_info(f"现在是{self.Action_team.name}的回合")

            elif self.container.selected_chess.rect.collidepoint(mouse_x,mouse_y):
                self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                del self.container.selected_chess.drop_sprite_group
                del self.container.selected_chess
            elif self.container.check_and_select_chess((mouse_x,mouse_y),self.Action_team):
                self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                selected_chess = self.container.selected_chess
                self.all_sprites.add(selected_chess.drop_sprite_group,layer = DROP_POINT_LAYER)

        self.update()

    def update(self,GAME_OVER = False):
        self.screen.blit(self.background_img, (0, 0))
        self.chessBoard_surface.blit(self.board_img,(0,0))
        self.screen.blit(self.chessBoard_surface, CHESSBOARD_ORI)

        self.screen.blit(self.log_surface,LOG_ORI)
        
        self.display_action(self.Action_team)
        self.screen.blit(self.tip_surface,(0,0))

        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        if GAME_OVER:
            self.display_winner()
        pygame.display.flip()


    def updateScreenScale(self):
        #背景图片
        background_img = pygame.image.load(os.path.join(chessBoard_img_path,backGround_img))
        self.background_img = pygame.transform.scale(background_img,(GAME_WIDTH, GAME_HEIGHT))
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
        self.screen.blit(self.background_img, (0, 0))

        #棋盘版
        board_img = pygame.image.load(os.path.join(chessBoard_img_path,chessBoard_img))
        self.board_img = pygame.transform.scale(board_img,(CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT))
        self.chessBoard_surface = pygame.Surface((CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT))
        self.chessBoard_surface.blit(self.board_img,(0,0))

        self.failed_img = pygame.image.load(os.path.join(icon_path,victory_tip_img))
        self.victory_img = pygame.image.load(os.path.join(icon_path,failed_tip_img))

        #信息版
        teamTip_img = pygame.image.load(os.path.join(icon_path,team_tip_img))
        self.team_tip_img = pygame.transform.scale(teamTip_img,(TIP_TEAM_SIZE_X, TIP_TEAM_SIZE_Y))
        self.tip_surface = pygame.Surface((TIP_WIDTH, TIP_HEIGHT), pygame.SRCALPHA)
        self.display_action(ActionTeam.BLACK)

        #日志版
        self.log_surface = pygame.Surface((LOG_WIDTH, LOG_HEIGHT), pygame.SRCALPHA)
        self.log_surface.fill((0, 0, 0, 0))

        #加载到屏幕
        self.screen.blit(self.log_surface,LOG_ORI)
        self.screen.blit(self.chessBoard_surface, CHESSBOARD_ORI)
        self.screen.blit(self.tip_surface,(0,0))
        self.container.update_abs_posi()
        pygame.display.flip()


    #信息版
    def display_action(self,action_team):
        self.tip_surface.fill((0, 0, 0, 0))
        if action_team == ActionTeam.RED:
            self.tip_surface.blit(self.team_tip_img,ACTION_TIP_ORI_RED)
        else:
            self.tip_surface.blit(self.team_tip_img,ACTION_TIP_ORI_BLACK)
    def display_winner(self):
        if self.Action_team == ActionTeam.RED:
            self.screen.blit(self.victory_img,GAMEOVER_TIP_ORI_RED)
            self.screen.blit(self.failed_img,GAMEOVER_TIP_ORI_BLACK)
        else:
            self.screen.blit(self.victory_img,GAMEOVER_TIP_ORI_BLACK)
            self.screen.blit(self.failed_img,GAMEOVER_TIP_ORI_RED)


    #日志版
    text_color = (255, 255, 255)
    def log_info(self,text):
        self.log_surface.fill((0, 0, 0, 0))
        text_sub_surface = self.font.render(text,True,self.text_color)
        text_x = (LOG_WIDTH - text_sub_surface.get_width()) // 2
        text_y = (LOG_HEIGHT - text_sub_surface.get_height()) // 2
        self.log_surface.blit(text_sub_surface,(0,0))

def scale_chess_img(image,enlargeSize = 1):
    return pygame.transform.scale(image,(CHESS_SIZE_X*enlargeSize, CHESS_SIZE_Y*enlargeSize))

def Dict_to_Abs_posi(dict_posi):
    x,y = dict_posi
    x = x * CHESS_SIZE_X + OFFSET_X
    y = y * CHESS_SIZE_Y + OFFSET_Y
    return (x,y)

def Abs_to_Dict_posi(abs_posi):
    x, y = abs_posi
    x = (x - OFFSET_X) // CHESS_SIZE_X
    y = (y - OFFSET_Y) // CHESS_SIZE_Y
    return (x, y)

if __name__ =='__main__':
    from Container import Container
    container = Container()
    game = Game()
    game.setContainer(container)
    game.run()