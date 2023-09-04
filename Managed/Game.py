import os
import pygame
from pygame.locals import *

chessBoard_img_path = './Resource/img/ChessBoard'

# 定义一些常量
WIDTH, HEIGHT = 600, 660
ROWS, COLS = 10, 9

SQUARE_SIZE_X = WIDTH // COLS
SQUARE_SIZE_Y = HEIGHT // ROWS
OFFSET_X = SQUARE_SIZE_X // 2
OFFSET_Y = SQUARE_SIZE_Y // 2

def update_global_val():
    global WIDTH, HEIGHT,SQUARE_SIZE_X,SQUARE_SIZE_Y,OFFSET_X,OFFSET_Y
    SQUARE_SIZE_X = WIDTH // COLS
    SQUARE_SIZE_Y = HEIGHT // ROWS
    OFFSET_X = SQUARE_SIZE_X // 2
    OFFSET_Y = SQUARE_SIZE_Y // 2
# 定义一些颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    Action_team = None
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("中国象棋")  # 设置游戏名字
        self.clock = pygame.time.Clock()

    def setContainer(self,container):
        self.container :Container = container

    def run(self):
        global WIDTH, HEIGHT,SQUARE_SIZE_X,SQUARE_SIZE_Y
        self.updateScreen()
        self.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.clickEvent(event)
                elif event.type == VIDEORESIZE:
                    WIDTH, HEIGHT = event.size[0], event.size[1]
                    update_global_val()
                    self.updateScreen()
                    self.update()
            pygame.display.flip()
            self.clock.tick(60)

    def clickEvent(self,event):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        selected_chess = self.container.selected_chess
        if selected_chess == None:
            self.container.select_chess((mouse_x,mouse_y))
            self.container.selected_chess.draw_drop_points(self.screen)
        else:
            for drop_sprite in selected_chess.drop_sprite_group.sprites():
                if drop_sprite.rect.collidepoint(mouse_x,mouse_y):
                    pass


    def updateScreen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.board_img = pygame.image.load(os.path.join(chessBoard_img_path,"棋盘.png"))
        self.board_img = pygame.transform.scale(self.board_img,(WIDTH, HEIGHT))
        self.screen.blit(self.board_img, (0, 0))
        self.container.update_abs_posi()

    def update(self):
        self.container.chess_sprite_group.update()
        self.container.chess_sprite_group.draw(self.screen)


def scale_chess_img(image):
    return pygame.transform.scale(image,(SQUARE_SIZE_X, SQUARE_SIZE_Y))

def Dict_to_Abs_posi(dict_posi):
    x,y = dict_posi
    x = x * SQUARE_SIZE_X + OFFSET_X
    y = y * SQUARE_SIZE_Y + OFFSET_Y
    return (x,y)

def Abs_to_Dict_posi(abs_posi):
    x, y = abs_posi
    x = (x - OFFSET_X) // SQUARE_SIZE_X
    y = (y - OFFSET_Y) // SQUARE_SIZE_Y
    return (x, y)

if __name__ =='__main__':
    from Container import Container
    container = Container()
    game = Game()
    game.setContainer(container)
    game.run()