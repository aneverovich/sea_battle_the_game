from core.functions.conversion import convert_coordinates


class Ship():

    def __init__(self, number_of_decks, name):
        self.type = 'Ship'
        self.name = name
        self.number_of_decks = number_of_decks
        self.coordinates = []
        self.border_coordinates = []
        self.damaged_coordinates = []
        self.orientation = None
        self.alive = True
        self.lives = number_of_decks

    def take_damage(self, letter_index, digit_index):
        if (digit_index - 1, letter_index) in self.damaged_coordinates:
            pass
        else:
            self.damaged_coordinates.append((digit_index - 1, letter_index))
            if self.alive:
                self.lives -= 1
                self.alive = False if self.lives == 0 else True

    def __str__(self):
        coordinates = convert_coordinates(self.coordinates)
        damaged_coordinates = convert_coordinates(self.damaged_coordinates)
        level_str = f" level: {self.level} |" if hasattr(self, 'level') else ''
        return f"{self.type}: {self.name} | Health: {self.lives}/{self.number_of_decks} |" + \
            f"{level_str} Coordinates: {coordinates} | Damaged coordinates: {damaged_coordinates}"
