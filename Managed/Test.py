from ChessModel import Chess,卒,士


zu = 卒()
shi = 士()

chesses:list[Chess] = [zu,shi]


for chess in chesses:
    chess.move()