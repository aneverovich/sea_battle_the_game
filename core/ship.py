class Ship():

    def __init__(self, number_of_decks, name):
        self.name = name
        self.number_of_decks = number_of_decks
        self.coordinates = []
        self.border_coordinates = []
        self.damaged_coordinates = []
        self.orientation = None
        self.alive = True
        self.lives = number_of_decks

    def take_damage(self, letter_index, digit_index):
        if (letter_index, digit_index) in self.damaged_coordinates:
            pass
        else:
            self.damaged_coordinates.append((letter_index, digit_index))
            if self.alive:
                self.lives -= 1
                self.alive = False if self.lives == 0 else True

    def __str__(self):
        coordinates = []
        damaged_coordinates = []
        for x in self.coordinates:
            coordinates.append(f"{'ABCDEFGHIJ'[x[1]]}:{x[0] + 1}")
        for x in self.damaged_coordinates:
            damaged_coordinates.append(f"{'ABCDEFGHIJ'[x[1]]}:{x[0] + 1}")
        return f"Ship: {self.name} | Health: {self.lives}/{self.number_of_decks} |" + \
            f" Coordinates: {coordinates} | Damaged coordinates: {damaged_coordinates}"
