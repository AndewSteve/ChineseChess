from Managed.Game import Game
from Managed.Container import Container
from Managed.Window import Window
import pygame

if __name__ == '__main__':
    pygame.init()
    container = Container()
    game = Game()
    window = Window()
    game.setContainer(container)
    game.setWindow(window)
    window.setContainer(container)
    game.run()