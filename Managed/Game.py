from enum import Enum
import os
import pygame
from pygame.locals import *
from Managed.Mixer import Mixer

#region 游戏资源
chessBoard_img_path = './Resource/img/ChessBoard'
icon_path = './Resource/img/icon'
front_path = './Resource/front/FZLBJW.ttf'

chessBoard_img = 'chessboard.png'
backGround_img = 'background.jpg'
#team_tip_img = '走棋.png'    现在不用图片提示了
victory_tip_img = '获胜.png'
failed_tip_img = '败北.png'
save_img = 'save.png'
quit_img = 'quit.png'
remake_img = 'remake.png'
#endregion


#region 字体颜色
color_white = (255, 255, 255)
color_yellow = (255,255,0)
color_red = (255,0,0)
#endregion

#region 游戏设置
tipping_minutes = 1
warning_minutes = 2
log_capital = 5
log_delta_alpha = 40
#endregion


#region 视窗常量
# 游戏视窗大小
GAME_WIDTH,GAME_HEIGHT = 1200,780

#提示窗口大小
TIP_WIDTH,TIP_HEIGHT = 300,780
ACTION_TIP_ORI_BLACK,ACTION_TIP_ORI_RED = (60,240),(60,420)
ACTION_TIME_TIP_ORI_BLACK,ACTION_TIME_TIP_ORI_RED = (100,300),(100,480)

#棋盘窗口大小
CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT = 600, 660
GAMEOVER_TIP_ORI_RED,GAMEOVER_TIP_ORI_BLACK = (500,180),(500,480)
#棋盘窗口原点
CHESSBOARD_ORI = 300,60
#每个格子的大小
CHESS_SIZE_X,CHESS_SIZE_Y = 60,60
#游戏左上角到第一个棋子间的位置差
OFFSET_X,OFFSET_Y = 360,120

#日志窗口原点
LOG_ORI = 900,0
SAVE_ORI = (TIP_WIDTH//2-140,TIP_HEIGHT//2-77*5)
QUIT_ORI = (TIP_WIDTH//2-140,TIP_HEIGHT//2-77*3)
REMAKE_ORI = (TIP_WIDTH//2-140,TIP_HEIGHT//2-77)

#渲染图层
CHESS_LAYER = 4#棋子层
DROP_POINT_LAYER = 3#落点层

def update_global_val(game_WIDTH, game_HEIGHT):
    global GAME_WIDTH,GAME_HEIGHT,TIP_WIDTH,TIP_HEIGHT,LOG_ORI,CHESSBOARD_ORI,OFFSET_X,OFFSET_Y
    global GAMEOVER_TIP_ORI_RED,GAMEOVER_TIP_ORI_BLACK,ACTION_TIP_ORI_BLACK,ACTION_TIP_ORI_RED
    global ACTION_TIME_TIP_ORI_BLACK,ACTION_TIME_TIP_ORI_RED,SAVE_ORI,QUIT_ORI,REMAKE_ORI
    
    GAME_WIDTH,GAME_HEIGHT = game_WIDTH, game_HEIGHT
    TIP_WIDTH,TIP_HEIGHT = (GAME_WIDTH - CHESSBOARD_WIDTH)//2,GAME_HEIGHT
    LOG_ORI = (TIP_WIDTH + CHESSBOARD_WIDTH),0
    CHESSBOARD_ORI = TIP_WIDTH,(GAME_HEIGHT-CHESSBOARD_HEIGHT)//2
    OFFSET_X,OFFSET_Y = (TIP_WIDTH + CHESS_SIZE_X),(GAME_HEIGHT-CHESSBOARD_HEIGHT)//2 + CHESS_SIZE_Y
    GAMEOVER_TIP_ORI_BLACK = (TIP_WIDTH+CHESSBOARD_WIDTH//3,OFFSET_Y+CHESS_SIZE_Y*6)
    GAMEOVER_TIP_ORI_RED = (TIP_WIDTH+CHESSBOARD_WIDTH//3,OFFSET_Y+CHESS_SIZE_Y)
    ACTION_TIP_ORI_BLACK,ACTION_TIP_ORI_RED = (TIP_WIDTH//5,OFFSET_Y+CHESS_SIZE_Y*2),(TIP_WIDTH//5,OFFSET_Y+CHESS_SIZE_Y*5)
    ACTION_TIME_TIP_ORI_BLACK,ACTION_TIME_TIP_ORI_RED = (TIP_WIDTH/3,OFFSET_Y+CHESS_SIZE_Y*3),(TIP_WIDTH/3,OFFSET_Y+CHESS_SIZE_Y*6)
    SAVE_ORI = (TIP_WIDTH//2-140,TIP_HEIGHT//2-77*5)
    QUIT_ORI = (TIP_WIDTH//2-140,TIP_HEIGHT//2-77*3)
    REMAKE_ORI = (TIP_WIDTH//2-140,TIP_HEIGHT//2-77)


#endregion


class ActionTeam(Enum):
    RED = 1
    BLACK = 2


class Game:
    Action_team :ActionTeam= None
    def __init__(self):

        
        self.mixer = Mixer()
        self.font = pygame.font.Font(front_path, 32)
        self.team_tip_font = pygame.font.Font(front_path, 60)
        self.time_font = pygame.font.Font(front_path, 60)
        pygame.display.set_caption("中国象棋")  # 设置游戏名字
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.clock = pygame.time.Clock()
        self.Action_team  = ActionTeam.RED
        self.action_timer = 0
        self.last_frame_time = 0
        self.message = [f"现在是{self.Action_team.name}的回合"]
        self.checkmated_team:ActionTeam = None
        self.game_over = False
        self.game_saved = True
        self.game_running = True

    def setContainer(self,container):
        self.container :Container = container
        self.all_sprites.add(self.container.chess_sprite_group,layer = CHESS_LAYER)
        self.container.setMixer(self.mixer)

    def run(self):
        self.init_screen()
        self.update()
        while self.game_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_posi = pygame.mouse.get_pos()
                    if self.log_surface_rect.collidepoint(mouse_posi):
                        self.MenuClickEven(mouse_posi)
                    elif not self.game_over:
                        self.ChessBoardClickEvent(mouse_posi)
                elif event.type == VIDEORESIZE:
                    temp_WIDTH, temp_HEIGHT = event.size[0], event.size[1]
                    if temp_WIDTH>1000 and temp_HEIGHT>700:
                        update_global_val(temp_WIDTH, temp_HEIGHT)
                        self.init_screen()
                        self.update()
            self.update()
            self.clock.tick(60)
        pygame.quit()

    def ChessBoardClickEvent(self,mouse_posi):
        if self.container.selected_chess == None:#现在没有选中棋子
            if self.container.check_and_select_chess(mouse_posi,self.Action_team):#选择到棋子
                selected_chess = self.container.selected_chess
                self.all_sprites.add(selected_chess.drop_sprite_group,layer = DROP_POINT_LAYER)#添加落点展示
        else:
            if not self.container.check_and_drop_chess(mouse_posi):#检查是否点击到落点
                self.mixer.play("提示音")
                if not self.container.checkmated_Team == None:
                    self.log_info(f"{self.checkmated_team.name}正在被将军")
                    self.log_info(f"请先防守")
                else:
                    self.log_info(f"不能自杀")
            if self.container.selected_chess == None:#点击到落点
                self.mixer.play("落子声")
                self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)#清空落点
                if self.container.RED_checkmate == None or self.container.BLACK_checkmate == None:#有将死
                    self.game_over = True
                    self.mixer.play("绝杀声")
                    self.log_info(f"游戏结束，{self.Action_team.name}胜利")
                    print(f"游戏结束，{self.Action_team}胜利")
                    self.game_saved = True
                else:
                    if not self.container.checkmated_Team == None:
                        self.checkmated_team = ActionTeam.RED if self.container.checkmated_Team.value == ActionTeam.RED.value else ActionTeam.BLACK
                        if self.checkmated_team == ActionTeam.RED:
                            self.mixer.play("将军")
                        else:
                            self.mixer.play("checkmate")
                        self.log_info(f"{self.checkmated_team.name}被将军")
                    self.Action_team = (ActionTeam.RED if self.Action_team == ActionTeam.BLACK else ActionTeam.BLACK)#换手
                    self.action_timer = 0
                    self.log_info(f"现在是{self.Action_team.name}的回合")
                    self.game_saved = False

            elif self.container.selected_chess.rect.collidepoint(mouse_posi):#点击到当前选中的棋子，取消选择
                self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                del self.container.selected_chess.drop_sprite_group
                del self.container.selected_chess
            elif self.container.check_and_select_chess(mouse_posi,self.Action_team):#重新选择友方棋子
                self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
                selected_chess = self.container.selected_chess
                self.all_sprites.add(selected_chess.drop_sprite_group,layer = DROP_POINT_LAYER)


    def update(self):
        """刷新屏幕

        Args:
            GAME_OVER (bool, optional): 是否展示结束画面. Defaults to False.
        """
        self.chessBoard_surface.blit(self.board_img,(0,0))
        self.display_action()

        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.chessBoard_surface, CHESSBOARD_ORI)
        self.screen.blit(self.tip_surface,(0,0))
        self.screen.blit(self.log_surface,LOG_ORI)

        self.log_info()
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        if self.game_over:
            self.display_winner()
        pygame.display.flip()


    #初始化屏幕、加载图片
    def init_screen(self):
        #背景图片
        background_img = pygame.image.load(os.path.join(chessBoard_img_path,backGround_img))
        self.background_img = pygame.transform.scale(background_img,(GAME_WIDTH, GAME_HEIGHT))
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)

        #棋盘版
        self.board_img = pygame.image.load(os.path.join(chessBoard_img_path,chessBoard_img))
        self.chessBoard_surface = pygame.Surface((CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT))
        self.chessBoard_surface.blit(self.board_img,(0,0))

        #信息版
        self.teamTipRed_sub_surface = self.team_tip_font.render("红方走棋",True,color_white)
        self.teamTipBlack_sub_surface = self.team_tip_font.render("黑方走棋",True,color_white)
        #self.team_tip_img = pygame.image.load(os.path.join(icon_path,team_tip_img))
        self.tip_surface = pygame.Surface((TIP_WIDTH, TIP_HEIGHT), pygame.SRCALPHA)
        self.display_action()
        #胜利图片
        self.failed_img = pygame.image.load(os.path.join(icon_path,victory_tip_img))
        self.failed_img = pygame.transform.smoothscale(self.failed_img, (210, 95))
        self.victory_img = pygame.image.load(os.path.join(icon_path,failed_tip_img))
        self.victory_img = pygame.transform.smoothscale(self.victory_img, (210, 95))

        #日志版
        self.save_img = pygame.image.load(os.path.join(icon_path,save_img))
        self.save_img = pygame.transform.smoothscale(self.save_img, (186, 102))
        self.save_img_rect = self.save_img.get_rect()
        self.save_img_rect.center = TIP_WIDTH + TIP_WIDTH/2 + CHESSBOARD_WIDTH,TIP_HEIGHT/2-77*4
        self.quit_img = pygame.image.load(os.path.join(icon_path,quit_img))
        self.quit_img = pygame.transform.smoothscale(self.quit_img, (186, 102))
        self.quit_img_rect = self.quit_img.get_rect()
        self.quit_img_rect.center = TIP_WIDTH + TIP_WIDTH/2 + CHESSBOARD_WIDTH,TIP_HEIGHT/2-77*2
        self.remake_img = pygame.image.load(os.path.join(icon_path,remake_img))
        self.remake_img = pygame.transform.smoothscale(self.remake_img, (186, 102))
        self.remake_img_rect = self.remake_img.get_rect()
        self.remake_img_rect.center = TIP_WIDTH + TIP_WIDTH/2 + CHESSBOARD_WIDTH,TIP_HEIGHT/2
        self.log_surface = pygame.Surface((TIP_WIDTH, TIP_HEIGHT), pygame.SRCALPHA)
        
        self.log_surface.fill((0, 0, 0, 0))
        self.log_surface_rect = self.log_surface.get_rect()
        self.log_surface_rect.center = TIP_WIDTH + TIP_WIDTH/2 + CHESSBOARD_WIDTH,TIP_HEIGHT/2

        #加载到屏幕
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.log_surface,LOG_ORI)
        self.screen.blit(self.chessBoard_surface, CHESSBOARD_ORI)
        self.screen.blit(self.tip_surface,(0,0))
        self.log_info()
        self.container.update_abs_posi()
        pygame.display.flip()

    #左侧信息版
    def display_action(self,action_team:ActionTeam= None):
        """展示行动方和计时

        Args:
            action_team (_type_, optional): 默认展示当前行动方. Defaults to None.
        """
        if action_team == None:
            action_team = self.Action_team

        #region 计时器
        if not self.game_over:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_frame_time  # 计算帧间隔
            self.last_frame_time = current_time

            self.action_timer += delta_time
        seconds = self.action_timer // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        color = color_white
        if minutes >=tipping_minutes :
            color = (color_red if minutes >=warning_minutes else color_yellow)
        formatted_time = f"{minutes:02}:{seconds:02}"
        time_sub_surface = self.time_font.render(formatted_time,True,color)
        #endregion

        #region 行动方指示
        self.tip_surface.fill((0, 0, 0, 0))
        if action_team == ActionTeam.RED:
            self.tip_surface.blit(self.teamTipRed_sub_surface,ACTION_TIP_ORI_RED)
            self.tip_surface.blit(time_sub_surface,ACTION_TIME_TIP_ORI_RED)
        else:
            self.tip_surface.blit(self.teamTipBlack_sub_surface,ACTION_TIP_ORI_BLACK)
            self.tip_surface.blit(time_sub_surface,ACTION_TIME_TIP_ORI_BLACK)
        #endregion

    #展示结束图片
    def display_winner(self):
        """展示结束图片
        """
        if self.Action_team == ActionTeam.RED:
            self.screen.blit(self.victory_img,GAMEOVER_TIP_ORI_RED)
            self.screen.blit(self.failed_img,GAMEOVER_TIP_ORI_BLACK)
        else:
            self.screen.blit(self.victory_img,GAMEOVER_TIP_ORI_BLACK)
            self.screen.blit(self.failed_img,GAMEOVER_TIP_ORI_RED)


    #日志版
    def log_info(self,text = ""):
        """在日志版上输出信息
        
        Args:
            text (str, optional): 默认输出上一条信息
        """
        if not text == "":
            if len(self.message)>log_capital:
                self.message.pop(0)
            self.message.append(text)

        self.log_surface.fill((0, 0, 0, 0))

        self.log_surface.blit(self.save_img,SAVE_ORI)
        self.log_surface.blit(self.quit_img,QUIT_ORI)
        self.log_surface.blit(self.remake_img,REMAKE_ORI)


        y = TIP_HEIGHT - self.font.get_height()
        for depth in range(len(self.message)):
            color = (255-log_delta_alpha*depth,255-log_delta_alpha*depth,255-log_delta_alpha*depth)
            text_sub_surface = self.font.render(self.message[len(self.message)-1-depth],True,color)
            self.log_surface.blit(text_sub_surface,(0,y))
            y -= self.font.get_height()



    #右侧菜单
    def MenuClickEven(self,mouse_posi):
        if self.save_img_rect.collidepoint(mouse_posi):
            if (not self.game_over) and (self.container.save_chess_board()):
                self.game_saved = True
                self.log_info("已将存档保存到save00")
            else:
                self.log_info("不允许保存死局,或发生文件错误")
        elif self.quit_img_rect.collidepoint(mouse_posi):
            if not self.game_saved:
                self.log_info("游戏未保存,是否要退出?")
                self.log_info("(退出请直接结束程序)")
            else:
                self.game_running = False
        elif self.remake_img_rect.collidepoint(mouse_posi):
            self.container.load_chess_board(remake= True)
            self.all_sprites.remove_sprites_of_layer(CHESS_LAYER)
            self.all_sprites.remove_sprites_of_layer(DROP_POINT_LAYER)
            self.all_sprites.empty()
            container = self.container
            self.setContainer(container)
            self.init_screen()
            self.Action_team = ActionTeam.RED
            self.action_timer = 0
            self.game_over = False
            


def scale_chess_img(image,enlargeSize = 1):#将棋子素材缩放到合适比例
    return pygame.transform.smoothscale(image, (CHESS_SIZE_X*enlargeSize, CHESS_SIZE_Y*enlargeSize))
    #return pygame.transform.scale(image,(CHESS_SIZE_X*enlargeSize, CHESS_SIZE_Y*enlargeSize))

def Dict_to_Abs_posi(dict_posi):
    """将逻辑坐标转化为屏幕坐标

    Args:
        dict_posi (tuple): 逻辑坐标元组(dict_x,dict_y)
    Returns:
        tuple: 屏幕坐标元组(abs_x,abs_y)
    """
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