from random import choice
from core.ship import Ship
from core.functions.check_border_coordinates import find_horizontal_oriented_ship_border_coordinates
from core.functions.check_border_coordinates import find_vertical_oriented_ship_border_coordinates
from core.functions.check_border_coordinates import find_one_deck_ship_border_coordinates


class Gameboard():

    def __init__(self):
        self.battlefield = {
            level: [[0 for cell in range(10)] for line in range(10)] for level in range(0, -11, -1)
        }
        self.board = self.battlefield[0]
        self.ships = (
            Ship(4, 'd4'),
            Ship(3, 'd3_1'),
            Ship(3, 'd3_2'),
            Ship(2, 'd2_1'),
            Ship(2, 'd2_2'),
            Ship(2, 'd2_3'),
            Ship(1, 'd1_1'),
            Ship(1, 'd1_2'),
            Ship(1, 'd1_3'),
            Ship(1, 'd1_4'))
        self.__dead_ships_counter = 0
        self.game_over = False

    def reset(self):
        self.__init__()

    def inspect_ship(self, name):
        for ship in self.ships:
            if ship.name == name:
                return ship.__str__()

    def ships_auto_arrangement(self):
        for ship in self.ships:
            self.__place_ship(ship)

    def check_hit(self, letter_index, digit):
        if self.board[digit - 1][letter_index] == 1:
            self.board[digit - 1][letter_index] = 2
            for ship in self.ships:
                if (digit - 1, letter_index) in ship.coordinates:
                    ship.take_damage(letter_index, digit)
                    if not ship.alive:
                        self.__dead_ships_counter += 1
                        for line, cell in ship.border_coordinates:
                            self.board[line][cell] = 3
            if self.__dead_ships_counter == 10:
                self.game_over = True
            return True
        elif self.board[digit - 1][letter_index] == 2:
            pass
        else:
            self.board[digit - 1][letter_index] = 3
            return False

    def __place_ship(self, ship):
        if ship.number_of_decks > 1:
            avaliable_coordinates = []
            for line_index, line in enumerate(self.board):
                for cell_index, cell in enumerate(line[:-(ship.number_of_decks - 1)]):
                    if cell == 0:
                        temp_ship = line[cell_index:cell_index + (ship.number_of_decks)]
                        if len(set(temp_ship)) == 1:
                            avaliable_coordinates.append(
                                [(line_index, cell_index + x) for x in range(ship.number_of_decks)]
                            )
            board_t = [list(x) for x in zip(*self.board)]
            for cell_index, cell in enumerate(board_t):
                for line_index, line in enumerate(cell[:-3]):
                    if line == 0:
                        temp_ship = cell[line_index:line_index + 4]
                        if len(set(temp_ship)) == 1:
                            avaliable_coordinates.append(
                                [(line_index + x, cell_index) for x in range(ship.number_of_decks)]
                            )
            coordinates = choice(avaliable_coordinates)
            orientation = 'horizontal' if coordinates[0][0] == coordinates[1][0] else 'vertical'
            ship.coordinates = coordinates
            ship.orientation = orientation
            for digit_index, letter_index in coordinates:
                self.board[digit_index][letter_index] = 1
            if orientation == 'horizontal':
                border_coordinates = find_horizontal_oriented_ship_border_coordinates(coordinates)
            else:
                border_coordinates = find_vertical_oriented_ship_border_coordinates(coordinates)
        else:
            avaliable_coordinates = []
            for line_index, line in enumerate(self.board):
                for cell_index, cell in enumerate(line):
                    if cell == 0:
                        avaliable_coordinates.append((line_index, cell_index))
            coordinates = choice(avaliable_coordinates)
            ship.coordinates = [coordinates]
            self.board[coordinates[0]][coordinates[1]] = 1
            border_coordinates = find_one_deck_ship_border_coordinates(coordinates)
        ship.border_coordinates = border_coordinates
        for line_index, cell_index in border_coordinates:
            self.board[line_index][cell_index] = 4
