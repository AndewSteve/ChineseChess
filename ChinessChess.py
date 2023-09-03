from Managed.Game import Game
from Managed.Container import Container


if __name__ == '__main__':
    game = Game()
    container = Container()
    game.setContainer(container)
    game.setSpriteGroup(container.sprite_group)
    game.run()