import os
import pygame
from pygame.locals import *
from Managed.ChessModel.ChessColor import ChessColor
from Managed.icon import icon as Icon

chessBoard_img_path = './Resource/img/ChessBoard'
Icon_Asset_path = './Resource/img/icon'
front_path = './Resource/front/FZLBJW.ttf'
chessBoard_img = 'chessboard.png'
backGround_img = 'background.jpg'

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
GAMEOVER_TIP_ORI_RED,GAMEOVER_TIP_ORI_BLACK = (500,480),(500,180)
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


class Window:
    icon_dict:dict[str,Icon]={}
    all_sprites = pygame.sprite.LayeredUpdates()
    container = None
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.action_timer = 0
        self.last_frame_time = 0
        self.checkmated_team:ChessColor = None
        self.game_over = False
        self.game_saved = True
        self.game_running = True
        self.loadIconAssets()
        self.loadTextAssets()

    def setContainer(self,container):
        from Managed.Container import Container
        self.container :Container = container
        self.Action_team :ChessColor = self.container.action_team_save
        self.message = [f"现在是{self.Action_team.name}的回合"]
        self.all_sprites.add(self.container.chess_sprite_group,layer = CHESS_LAYER)

    def blit_Screen(self):#更新屏幕
        self.blit_BackGround_Surface()
        self.blit_Tip_Surface()
        self.blit_ChessBoard_Surface()
        self.blit_Log_Surface()
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.display_winner()
        pygame.display.flip()

    def init_Screen(self):#初始化资源
        self.init_BackGround_Surface()
        self.init_Tip_Surface()
        self.init_ChessBoard_Surface()
        self.init_Log_Surface()
        self.container.update_abs_posi()
        self.blit_Screen()

    def loadTextAssets(self):#加载字体资源
        self.font = pygame.font.Font(front_path, 32)
        self.team_tip_font = pygame.font.Font(front_path, 60)
        self.time_font = pygame.font.Font(front_path, 60)

    def loadIconAssets(self):#加载标志图资源
        for filename in os.listdir(Icon_Asset_path):
            if filename.endswith(".png"):
                icon_name = os.path.splitext(filename)[0]
                icon_path = os.path.join(Icon_Asset_path,filename)
                icon = Icon(icon_path)
                self.icon_dict[icon_name] = icon

    #region 背景板
    def init_BackGround_Surface(self):
        background_img = pygame.image.load(os.path.join(chessBoard_img_path,backGround_img))
        self.background_img = pygame.transform.scale(background_img,(GAME_WIDTH, GAME_HEIGHT))
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

    def blit_BackGround_Surface(self):
        self.screen.blit(self.background_img, (0, 0))
    #endregion

    #region 左侧提示板
    def init_Tip_Surface(self):
        self.tip_surface = pygame.Surface((TIP_WIDTH, TIP_HEIGHT), pygame.SRCALPHA)
        self.teamTipRed_sub_surface = self.team_tip_font.render("红方走棋",True,color_white)
        self.teamTipBlack_sub_surface = self.team_tip_font.render("黑方走棋",True,color_white)

    def blit_Tip_Surface(self,action_team:ChessColor= None):
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
        if action_team == ChessColor.RED:
            self.tip_surface.blit(self.teamTipRed_sub_surface,ACTION_TIP_ORI_RED)
            self.tip_surface.blit(time_sub_surface,ACTION_TIME_TIP_ORI_RED)
        else:
            self.tip_surface.blit(self.teamTipBlack_sub_surface,ACTION_TIP_ORI_BLACK)
            self.tip_surface.blit(time_sub_surface,ACTION_TIME_TIP_ORI_BLACK)
        #endregion
        self.screen.blit(self.tip_surface,(0,0))
    #endregion

    #region 棋盘板
    def init_ChessBoard_Surface(self):
        self.chessBoard_surface = pygame.Surface((CHESSBOARD_WIDTH, CHESSBOARD_HEIGHT))
        self.board_img = pygame.image.load(os.path.join(chessBoard_img_path,chessBoard_img))

    def blit_ChessBoard_Surface(self):
        self.chessBoard_surface.blit(self.board_img,(0,0))
        self.screen.blit(self.chessBoard_surface, CHESSBOARD_ORI)
    #endregion

    #region 右侧日志板
    def init_Log_Surface(self):
        self.log_surface = pygame.Surface((TIP_WIDTH, TIP_HEIGHT), pygame.SRCALPHA)
        self.log_surface_rect = self.log_surface.get_rect()
        self.log_surface_rect.center = TIP_WIDTH + TIP_WIDTH/2 + CHESSBOARD_WIDTH,TIP_HEIGHT/2

        self.icon_dict["remake"].set_topleft((TIP_WIDTH + CHESSBOARD_WIDTH + REMAKE_ORI[0],REMAKE_ORI[1]))
        self.icon_dict["quit"].set_topleft((TIP_WIDTH + CHESSBOARD_WIDTH + QUIT_ORI[0],QUIT_ORI[1]))
        self.icon_dict["save"].set_topleft((TIP_WIDTH + CHESSBOARD_WIDTH + SAVE_ORI[0],SAVE_ORI[1]))

    def log_info(self,text=""):
        if not text == "":
            if len(self.message)>log_capital:
                self.message.pop(0)
            self.message.append(text)

    def blit_Log_Surface(self):
        """在日志版上输出信息
        
        Args:
            text (str, optional): 默认输出上一条信息
        """

        self.log_surface.fill((0, 0, 0, 0))

        self.log_surface.blit(self.icon_dict["save"].image,SAVE_ORI)
        self.log_surface.blit(self.icon_dict["quit"].image,QUIT_ORI)
        self.log_surface.blit(self.icon_dict["remake"].image,REMAKE_ORI)

        y = TIP_HEIGHT - self.font.get_height()
        for depth in range(len(self.message)):
            color = (255-log_delta_alpha*depth,255-log_delta_alpha*depth,255-log_delta_alpha*depth)
            text_sub_surface = self.font.render(self.message[len(self.message)-1-depth],True,color)
            self.log_surface.blit(text_sub_surface,(0,y))
            y -= self.font.get_height()
        self.screen.blit(self.log_surface,LOG_ORI)
    #endregion

    #region 覆盖在游戏屏幕上的胜利提示
    def display_winner(self):
        """展示结束图片
        """
        if self.Action_team == ChessColor.RED:
            self.screen.blit(self.icon_dict["获胜"].image,GAMEOVER_TIP_ORI_RED)
            self.screen.blit(self.icon_dict["败北"].image,GAMEOVER_TIP_ORI_BLACK)
        else:
            self.screen.blit(self.icon_dict["获胜"].image,GAMEOVER_TIP_ORI_BLACK)
            self.screen.blit(self.icon_dict["败北"],GAMEOVER_TIP_ORI_RED)
    #endregion

def scale_chess_img(image,enlargeSize = 1):#将棋子素材缩放到合适比例
    return pygame.transform.smoothscale(image, (CHESS_SIZE_X*enlargeSize, CHESS_SIZE_Y*enlargeSize))
    #return pygame.transform.scale(image,(CHESS_SIZE_X*enlargeSize, CHESS_SIZE_Y*enlargeSize))

def Dict_to_Abs_posi(dict_posi):#将逻辑坐标转化为屏幕坐标
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