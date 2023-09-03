
from Container import container #获取Container单例

class Game:
    def __init__(self):
        self._container = container
        pass


#共享单例
game = Game()