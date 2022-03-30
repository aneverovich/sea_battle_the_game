from core.ship import Ship


class Submarine(Ship):

    def __init__(self, number_of_decks, name):
        super().__init__(number_of_decks, name)
        self.type = 'Submarine'
        self.level = None

    def take_damage(self, letter_index, digit_index, level):
        if level == self.level:
            super().take_damage(letter_index, digit_index)
