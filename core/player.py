from datetime import datetime


class Player():

    def __init__(self, gameboard, enemy_gameboard, journal):
        self.gameboard = gameboard
        self.enemy_gameboard = enemy_gameboard
        self.winner = False
        self.journal = journal

    def atack(self, literal_index, digit):
        successful_atack = self.enemy_gameboard.check_hit(literal_index, digit)
        literal = 'ABCDEFGHIJ'[literal_index]
        self.journal.game_history['history'].append({
            self.name: {'target': f"{literal}:{digit}", 'successful_atack': successful_atack},
            'time': datetime.now().strftime("%H:%M:%S")
        })
        return successful_atack


class ConsolePlayer(Player):

    def __init__(self, gameboard, enemy_gameboard, journal):
        super().__init__(gameboard=gameboard, enemy_gameboard=enemy_gameboard, journal=journal)
        print("> Choose your username (leave balnk for 'Player')")
        self.name = input("> Username: ")
        if self.name.strip() == "":
            self.name = "Player"


class AiPlayer(Player):

    def __init__(self, gameboard, enemy_gameboard, journal):
        super().__init__(gameboard=gameboard, enemy_gameboard=enemy_gameboard, journal=journal)
        self.name = "ArtificalIntelligence"
