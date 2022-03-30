import os
from time import sleep
from core.gameboard import Gameboard
from console.terminal_colors import t_yellow
from console.terminal_colors import t_green_bold
from console.terminal_constants import TERMINAL_WIDTH
from console.terminal_constants import TERMINAL_FIT_2_BOARDS_IN_ONE_ROW
from console.terminal_constants import SPACE_BETWEEN_BOARDS
from console.terminal_constants import DOUBLE_BOARD_ROW_DIVIDER
from console.terminal_constants import LITERALS_LINE
from console.terminal_constants import DOUBLE_LITERALS_LINE
from console.terminal_constants import EMPTY_CELL
from console.terminal_constants import HEALTHY_SHIP_CELL
from console.terminal_constants import BROKEN_SHIP_CELL
from console.terminal_constants import BOMB_CELL
from console.terminal_constants import EXPLODED_BOMB_CELL
from console.terminal_constants import MISSED_SHOT_CELL
from console.terminal_constants import BOARD_ROW_DIVIDER
from console.terminal_constants import GAME_TITLE
from console.terminal_constants import AUTHOR_LINE
from console.terminal_help import DOCUMENTATION


class Terminal():

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def divider(divider_type: str) -> str:
        return divider_type * TERMINAL_WIDTH

    @staticmethod
    def c_text(text: str) -> str:
        free_space_left = (TERMINAL_WIDTH - len(text)) // 2
        free_space_right = TERMINAL_WIDTH - free_space_left - len(text)
        return " " * free_space_left + text + " " * free_space_right

    @staticmethod
    def r_align_text(text: str) -> str:
        free_space_left = TERMINAL_WIDTH - len(text)
        return " " * free_space_left + text

    @staticmethod
    def display_players_line(player_1: str, player_2: str) -> str:
        screen_borders_tab_len = 4
        screen_borders_tab = " " * screen_borders_tab_len
        free_space = TERMINAL_WIDTH - len(player_2) - len(player_1) -\
            (2 * screen_borders_tab_len)
        return "\n" + screen_borders_tab + '\033[4m' + player_1 + '\033[0m' + \
            " " * free_space + '\033[4m' + player_2 + '\033[0m' + screen_borders_tab + "\n"

    @staticmethod
    def display_game_title() -> None:
        Terminal.clear_terminal()
        print(Terminal.divider('*'))
        print(Terminal.c_text(GAME_TITLE))
        print(Terminal.divider('-'))
        print(Terminal.r_align_text(AUTHOR_LINE))
        print(Terminal.divider('*'))

    @staticmethod
    def display_help():
        print(DOCUMENTATION)
        print(Terminal.divider('='))

    @staticmethod
    def choose_player_name():
        print("> Choose your username (leave balnk for 'Player')")
        player_name = input("> Username: ")
        if len(player_name.split()) == 0:
            player_name = 'Player'
        print(f"> Hello, {player_name}!")
        return player_name

    @staticmethod
    def ask_for_submarines():
        valid_response = False
        while not valid_response:
            print("> Do you want to play with Submarines? ('n' for no, 'y' or leave blank for yes)")
            submarines_response = input("> ")
            if submarines_response.lower() == 'y' or len(submarines_response.split()) == 0:
                valid_response = True
                print("> Submarines: ON")
                return True
            elif submarines_response.lower() == 'n':
                print("> Submarines: OFF")
                valid_response = True
                return False

    @staticmethod
    def ask_for_bombs():
        valid_response = False
        while not valid_response:
            print("> Do you want to place some bombs on the gameboard? ('n' for no, 'y' or leave blank for yes)")
            bombs_response = input("> ")
            if bombs_response.lower() == 'y' or len(bombs_response.split()) == 0:
                valid_response = True
                print("> Bombs: ON")
                return True
            elif bombs_response.lower() == 'n':
                print("> Bombs: OFF")
                valid_response = True
                return False

    @staticmethod
    def ask_for_command(player):
        return input(f"({player}) > ")

    @staticmethod
    def draw_gameboard_line(gameboard, line_index, is_enemy_gameboard, is_godmode):
        gameboard_line_cells = []
        for cell in gameboard[line_index]:
            if cell == Gameboard.empty_cell_code or \
                    cell == Gameboard.border_around_ship_cell_code:
                gameboard_line_cells.append(EMPTY_CELL)
            elif cell == Gameboard.healthy_floating_object_cell_code:
                if is_enemy_gameboard and not is_godmode:
                    gameboard_line_cells.append(EMPTY_CELL)
                else:
                    gameboard_line_cells.append(HEALTHY_SHIP_CELL)
            elif cell == Gameboard.broken_floating_object_cell_code:
                gameboard_line_cells.append(BROKEN_SHIP_CELL)
            elif cell == Gameboard.bomb_cell_code:
                if is_enemy_gameboard and not is_godmode:
                    gameboard_line_cells.append(EMPTY_CELL)
                else:
                    gameboard_line_cells.append(BOMB_CELL)
            elif cell == Gameboard.exploded_bomb_cell_code:
                gameboard_line_cells.append(EXPLODED_BOMB_CELL)
            else:
                gameboard_line_cells.append(MISSED_SHOT_CELL)
        gameboard_line_cells = '|'.join(gameboard_line_cells)
        return gameboard_line_cells

    @staticmethod
    def display_gameboards(display_data, level_to_display, command_response, winner, is_godmode):
        left_username, right_username,\
            left_gameboard, right_gameboard = display_data
        print(Terminal.r_align_text(f"Level: {level_to_display}") + '\n')
        if winner is not None:
            print(Terminal.c_text(t_green_bold(f"{winner} won this game!")))
        if TERMINAL_FIT_2_BOARDS_IN_ONE_ROW:
            print(Terminal.display_players_line(left_username, right_username))
            print(DOUBLE_LITERALS_LINE)
            print(DOUBLE_BOARD_ROW_DIVIDER)
            for line_index in range(10):
                chr_left = 4 if line_index < 9 else 3
                space_left = ' ' * chr_left + f'{line_index + 1}  |'
                left_gameboard_line_cells = Terminal.draw_gameboard_line(left_gameboard, line_index, False, is_godmode)
                right_gameboard_line_cells = Terminal.draw_gameboard_line(right_gameboard, line_index, True, is_godmode)
                print(space_left + left_gameboard_line_cells + '|' +
                      ' ' * SPACE_BETWEEN_BOARDS + space_left + right_gameboard_line_cells + '|')
                print(DOUBLE_BOARD_ROW_DIVIDER)
        else:
            print('\n' + Terminal.c_text(f'\033[4m{left_username}\033[0m') + '\n')
            print(LITERALS_LINE)
            print(BOARD_ROW_DIVIDER)
            for line in range(10):
                chr_left = 4 if line < 9 else 3
                space_left = ' ' * chr_left + f'{line + 1}  |'
                left_gameboard_line_cells = []
                for cell in left_gameboard[line]:
                    if cell == 0 or cell == 4:
                        left_gameboard_line_cells.append(EMPTY_CELL)
                    elif cell == 1:
                        left_gameboard_line_cells.append(HEALTHY_SHIP_CELL)
                    elif cell == 2:
                        left_gameboard_line_cells.append(BROKEN_SHIP_CELL)
                    else:
                        left_gameboard_line_cells.append(MISSED_SHOT_CELL)
                left_gameboard_line_cells = '|'.join(left_gameboard_line_cells)
                print(space_left + left_gameboard_line_cells + '|')
                print(BOARD_ROW_DIVIDER)
            print('\n' + Terminal.c_text(f'\033[4m{right_username}\033[0m') + '\n')
            print(LITERALS_LINE)
            print(' ' * 7 + '--' * 20 + '-')
            for line in range(10):
                chr_left = 4 if line < 9 else 3
                space_left = ' ' * chr_left + f'{line + 1}  |'
                right_gameboard_line_cells = []
                for cell in right_gameboard[line]:
                    if cell == 0 or cell == 1 or cell == 4:
                        right_gameboard_line_cells.append(EMPTY_CELL)
                    elif cell == 2:
                        right_gameboard_line_cells.append(BROKEN_SHIP_CELL)
                    else:
                        right_gameboard_line_cells.append(MISSED_SHOT_CELL)
                right_gameboard_line_cells = '|'.join(right_gameboard_line_cells)
                print(space_left + right_gameboard_line_cells + '|')
                print(' ' * 7 + '--' * 20 + '-')
        print('\n' + Terminal.r_align_text('========================'))
        print(Terminal.r_align_text("Type in 'help' for help"))
        print(Terminal.divider('='))
        if command_response is not None:
            print(t_yellow(command_response))
            print(Terminal.divider("-"))

    @staticmethod
    def ai_atack_animation():
        for i in range(2):
            print(t_yellow(' Ai atack \\'), end='\r')
            sleep(1)
            print(t_yellow(' Ai atack /'), end='\r')
            sleep(1)
