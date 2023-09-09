from Managed.Game import Game
from Managed.Container import Container
import pygame

if __name__ == '__main__':
    pygame.init()
    game = Game()
    container = Container()
    game.setContainer(container)
    game.run()