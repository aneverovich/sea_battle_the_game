from core.game import Game

if __name__ == '__main__':
    game = Game()
    while not game.over:
        game.play()
