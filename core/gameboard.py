from random import choice
from random import randrange
from core.ship import Ship
from core.submarine import Submarine
from core.submerged_objects import Bomb
from core.functions.check_border_coordinates import find_horizontal_oriented_ship_border_coordinates
from core.functions.check_border_coordinates import find_vertical_oriented_ship_border_coordinates
from core.functions.check_border_coordinates import find_one_deck_ship_border_coordinates
from core.functions.conversion import convert_coordinates


class Gameboard():
    empty_cell_code = 0
    healthy_floating_object_cell_code = 1
    broken_floating_object_cell_code = 2
    missed_shot_cell_code = 3
    border_around_ship_cell_code = 4
    bomb_cell_code = 5
    exploded_bomb_cell_code = 6

    ship_codes = (
        ('d4', 4), ('d3_1', 3), ('d3_2', 3), ('d2_1', 2), ('d2_2', 2),
        ('d2_3', 2), ('d1_1', 1), ('d1_2', 1), ('d1_3', 1), ('d1_4', 1)
    )

    def __init__(self):
        self.battlefield = {
            level: [[0 for cell in range(10)] for line in range(10)]
            for level in range(0, -11, -1)
        }
        self.ships = {
            code: Ship(number_of_decks, code)
            for code, number_of_decks in self.ship_codes
        }
        self.submarines = {
            f"sub_{code}": Submarine(number_of_decks, f"sub_{code}")
            for code, number_of_decks in self.ship_codes
        }
        self.bombs = {
            f"bomb_{code}": Bomb(f"bomb_{code}") for code in range(randrange(8))
        }
        self.board = self.battlefield[0]
        self.state = {
            "game_over": False,
            "dead_ships_counter": 0,
            "dead_submarines_counter": 0,
            "board_level": {
                level: {
                    letter: {
                        digit: {
                            'cell_state': 0,
                            'object': None
                        } for digit in range(1, 11)
                    } for letter in 'ABCDEFGHIJ'
                } for level in range(0, -11, -1)
            }
        }

    def reset(self):
        self.__init__()

    def inspect(self, code):
        if code.lower().startswith('sub'):
            return self.__inspect_object(self.submarines, code)
        elif code.lower().startswith('bomb'):
            return self.__inspect_object(self.bombs, code)
        else:
            return self.__inspect_object(self.ships, code)

    def ships_auto_arrangement(self):
        for code in self.ship_codes:
            ship_object = self.ships[code[0]]
            self.__place_object(
                self.board,
                ship_object
            )
            self.__add_object_to_state(0, ship_object)

    def submarines_auto_arrangement(self):
        for code in self.ship_codes:
            level = randrange(0, -11, -1)
            submarine_object = self.submarines[f'sub_{code[0]}']
            submarine_object.level = level
            self.__place_object(
                self.battlefield[level],
                submarine_object
            )
            self.__add_object_to_state(level, submarine_object)

    def bombs_auto_arrangement(self):
        for bomb in self.bombs:
            bomb_object = self.bombs[bomb]
            self.__place_object(
                self.board,
                bomb_object
            )
            self.__add_object_to_state(0, bomb_object)

    def attack_cell(self, letter, digit, level, submarines_mode):
        cell_state = self.state["board_level"][level][letter][int(digit)]["cell_state"]
        cell_object = self.state["board_level"][level][letter][int(digit)]["object"]
        letter_index = 'abcdefghij'.index(letter.lower())
        digit_index = int(digit) - 1
        if cell_object is None:
            self.state["board_level"][level][letter][int(digit)]["cell_state"] = \
                self.missed_shot_cell_code
            self.battlefield[level][digit_index][letter_index] = self.missed_shot_cell_code
            return {
                'target': f'{letter}:{digit}:{level}',
                'successful_attack': False,
                'bomb': False,
                'object': None,
                'game_over': self.state["game_over"]
            }
        elif cell_object.type == 'Ship' or cell_object.type == 'Submarine':
            if cell_state == self.healthy_floating_object_cell_code:
                self.state["board_level"][level][letter][int(digit)]["cell_state"] = \
                    self.broken_floating_object_cell_code
                self.battlefield[level][digit_index][letter_index] = self.broken_floating_object_cell_code
                if cell_object.type == 'Submarine':
                    cell_object.take_damage(letter, digit, level)
                else:
                    cell_object.take_damage(letter, digit)
                if not cell_object.alive:
                    for d_index, l_index in cell_object.border_coordinates:
                        self.battlefield[level][d_index][l_index] = self.missed_shot_cell_code
                    if cell_object.type == 'Ship':
                        self.state["dead_ships_counter"] += 1
                    else:
                        self.state["dead_submarines_counter"] += 1
                    self.__check_game_over(submarines_mode)
                return {
                    'target': f'{letter}:{digit}:{level}',
                    'successful_attack': True,
                    'bomb': False,
                    'object': cell_object.name,
                    'game_over': self.state["game_over"]
                }
            else:
                return {
                    'target': f'{letter}:{digit}:{level}',
                    'successful_attack': False,
                    'bomb': False,
                    'object': cell_object.name,
                    'game_over': self.state["game_over"]
                }
        elif cell_object.type == 'Bomb':
            exploded = True if cell_state == self.exploded_bomb_cell_code else False
            self.state["board_level"][level][letter][int(digit)]["cell_state"] = self.exploded_bomb_cell_code
            self.battlefield[level][digit_index][letter_index] = self.exploded_bomb_cell_code
            return {
                'target': f'{letter}:{digit}:{level}',
                'successful_attack': False,
                'bomb': True,
                'exploded': exploded,
                'object': cell_object.code,
                'game_over': self.state["game_over"]
            }

    def __check_game_over(self, submarines_mode):
        if self.state["dead_ships_counter"] == 10:
            self.state["game_over"] = True
            if submarines_mode and not self.state["dead_submarines_counter"] == 10:
                self.state["game_over"] = False

    def __inspect_object(self, object_dict, code):
        try:
            return object_dict[code].__str__()
        except Exception as e:
            return str(e)

    def __add_object_to_state(self, level, object_to_add):
        object_coordinates = convert_coordinates(object_to_add.coordinates)
        for coordinates in object_coordinates:
            letter = coordinates[0]
            digit = coordinates[2:]
            self.state["board_level"][level][letter][int(digit)]["object"] = object_to_add
            if object_to_add.type == 'Ship' or object_to_add.type == 'Submarine':
                self.state["board_level"][level][letter][int(digit)]["cell_state"] = \
                    self.healthy_floating_object_cell_code
            elif object_to_add.type == 'Bomb':
                self.state["board_level"][level][letter][int(digit)]["cell_state"] = \
                    self.bomb_cell_code

    def __place_object(self, board, object_to_place):
        if object_to_place.type == 'Ship' or object_to_place.type == 'Submarine':
            if object_to_place.number_of_decks > 1:
                available_indexed_coordinates = \
                    self.__find_list_of_avaliable_indexed_coordinates_for_multiple_cells_object(
                        board,
                        object_to_place.number_of_decks
                    )
                chosen_indexed_coordinates = choice(available_indexed_coordinates)
                orientation = 'horizontal' \
                    if chosen_indexed_coordinates[0][0] == chosen_indexed_coordinates[1][0] \
                    else 'vertical'
                object_to_place.coordinates = chosen_indexed_coordinates
                object_to_place.orientation = orientation
                for digit_index, letter_index in chosen_indexed_coordinates:
                    board[digit_index][letter_index] = self.healthy_floating_object_cell_code
                if orientation == 'horizontal':
                    border_coordinates = find_horizontal_oriented_ship_border_coordinates(chosen_indexed_coordinates)
                else:
                    border_coordinates = find_vertical_oriented_ship_border_coordinates(chosen_indexed_coordinates)
                object_to_place.border_coordinates = border_coordinates
            else:
                available_indexed_coordinates = \
                    self.__find_list_of_avaliable_indexed_coordinates_for_single_cell_object(board)
                coordinates = choice(available_indexed_coordinates)
                object_to_place.coordinates = [coordinates]
                board[coordinates[0]][coordinates[1]] = self.healthy_floating_object_cell_code
                border_coordinates = find_one_deck_ship_border_coordinates(coordinates)
            object_to_place.border_coordinates = border_coordinates
            for line_index, cell_index in border_coordinates:
                board[line_index][cell_index] = self.border_around_ship_cell_code
        elif object_to_place.type == 'Bomb':
            available_indexed_coordinates = \
                self.__find_list_of_avaliable_indexed_coordinates_for_single_cell_object(board)
            coordinates = choice(available_indexed_coordinates)
            object_to_place.coordinates = [coordinates]
            board[coordinates[0]][coordinates[1]] = self.bomb_cell_code

    def __find_list_of_avaliable_indexed_coordinates_for_multiple_cells_object(self, board, cells_qty):
        available_indexed_coordinates = []
        # horizontal oriented objects
        for digit_index, line in enumerate(board):
            for letter_index, cell in enumerate(line[:-(cells_qty - 1)]):
                if cell == self.empty_cell_code:
                    temp_object = line[letter_index:letter_index + cells_qty]
                    if len(set(temp_object)) == 1:
                        available_indexed_coordinates.append(
                            [(digit_index, letter_index + x) for x in range(cells_qty)]
                        )
        # vertical oriented objects
        board_t = [list(x) for x in zip(*board)]
        for letter_index, cell in enumerate(board_t):
            for digit_index, line in enumerate(cell[:-(cells_qty - 1)]):
                if line == 0:
                    temp_object = cell[digit_index:digit_index + (cells_qty)]
                    if len(set(temp_object)) == self.empty_cell_code:
                        available_indexed_coordinates.append(
                            [(digit_index + x, letter_index) for x in range(cells_qty)]
                        )
        return available_indexed_coordinates

    def __find_list_of_avaliable_indexed_coordinates_for_single_cell_object(self, board):
        available_indexed_coordinates = []
        for digit_index, line in enumerate(board):
            for letter_index, cell in enumerate(line):
                if cell == 0:
                    available_indexed_coordinates.append((digit_index, letter_index))
        return available_indexed_coordinates
