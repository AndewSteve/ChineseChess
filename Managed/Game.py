import pygame
from pygame.locals import *

chessBoard_img_path = './Resource/img/ChessBoard'

# 定义一些常量
WIDTH, HEIGHT = 600, 660
ROWS, COLS = 10, 9
SQUARE_SIZE = WIDTH // COLS

# 定义一些颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    sprite_group:pygame.sprite.Group() = None
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("中国象棋")  # 设置游戏名字
        self.board_img = pygame.image.load('./Resource/img/ChessBoard/棋盘.png')
        self.board_img = pygame.transform.scale(self.board_img, (WIDTH, HEIGHT))
        self.screen.blit(self.board_img, (0, 0))
        self.clock = pygame.time.Clock()

    def setContainer(self,container):
        self.container = container

    def setSpriteGroup(self,sprite_group):
        self.sprite_group = sprite_group

    def run(self):
        self.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == VIDEORESIZE:
                    WIDTH, HEIGHT = event.size[0], event.size[1]
                    self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        self.sprite_group.update()
        self.sprite_group.draw(self.screen)

def scale_img(image):
    return pygame.transform.scale(image,(SQUARE_SIZE, SQUARE_SIZE))

def Dict_to_Abs_posi(dict_posi):
    x,y = dict_posi
    x = x * SQUARE_SIZE + SQUARE_SIZE // 2
    y = y * SQUARE_SIZE + SQUARE_SIZE // 2
    return (x,y)

if __name__ =='__main__':
    from Container import Container
    container = Container()
    game = Game()
    game.setContainer(container)
    game.setSpriteGroup(container.sprite_group)
    game.run()