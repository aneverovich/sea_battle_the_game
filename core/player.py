class Player():

    def __init__(self, name, gameboard, enemy_gameboard, journal):
        self.gameboard = gameboard
        self.enemy_gameboard = enemy_gameboard
        self.winner = False
        self.journal = journal
        self.name = name

    def attack(self, letter, digit, level, submarines_mode):
        attack_response = self.enemy_gameboard.attack_cell(letter, digit, level, submarines_mode)
        self.journal.add_event(self.name, attack_response)
        return attack_response
