from enum import Enum
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



class ActionTeam(Enum):
    RED = 1
    BLACK = 2

class Game:
    Action_team :ActionTeam= None
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("中国象棋")  # 设置游戏名字
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.clock = pygame.time.Clock()
        self.Action_team  = ActionTeam.BLACK

    def setContainer(self,container):
        self.container :Container = container
        self.all_sprites.add(self.container.chess_sprite_group,layer = 2)

    def run(self):
        self.updateScreenScale()
        global WIDTH, HEIGHT,SQUARE_SIZE_X,SQUARE_SIZE_Y
        self.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.clickEvent()
                elif event.type == VIDEORESIZE:
                    WIDTH, HEIGHT = event.size[0], event.size[1]
                    update_global_val()
                    self.updateScreenScale()
                    self.update()
            self.clock.tick(60)
            pygame.display.flip()

    def clickEvent(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        if self.container.selected_chess == None:
            print("现在没有选中棋子")
            if self.container.check_and_select_chess((mouse_x,mouse_y),self.Action_team):
                selected_chess = self.container.selected_chess
                self.all_sprites.add(selected_chess.drop_sprite_group,layer = 3)
        else:
            self.container.check_and_drop_chess((mouse_x,mouse_y))
            if self.container.selected_chess == None:
                self.all_sprites.remove_sprites_of_layer(3)
                self.Action_team = (ActionTeam.RED if self.Action_team == ActionTeam.BLACK else ActionTeam.BLACK)
            elif self.container.selected_chess.rect.collidepoint(mouse_x,mouse_y):
                self.all_sprites.remove_sprites_of_layer(3)
                del self.container.selected_chess.drop_sprite_group
                del self.container.selected_chess
            elif self.container.check_and_select_chess((mouse_x,mouse_y),self.Action_team):
                self.all_sprites.remove_sprites_of_layer(3)
                selected_chess = self.container.selected_chess
                self.all_sprites.add(selected_chess.drop_sprite_group,layer = 3)

            

        self.update()

    def updateScreenScale(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.board_img = pygame.image.load(os.path.join(chessBoard_img_path,"棋盘.png"))
        self.board_img = pygame.transform.scale(self.board_img,(WIDTH, HEIGHT))
        self.screen.blit(self.board_img, (0, 0))
        self.container.update_abs_posi()

    def update(self):
        self.all_sprites.update()
        self.screen.blit(self.board_img, (0, 0))
        self.all_sprites.clear(self.screen,self.board_img)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


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