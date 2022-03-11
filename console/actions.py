import os
from time import sleep
from random import randint
from console.terminal_colors import t_yellow
from console.terminal_colors import t_green_bold
from console.str_format import divider
from console.str_format import c_text
from console.str_format import r_align_text
from console.str_format import display_players_line
from console.config import TERMINAL_FIT_2_BOARDS_IN_ONE_ROW
from console.config import SPACE_BETWEEN_BOARDS
from console.config import DOUBLE_BOARD_ROW_DIVIDER
from console.config import LITERALS_LINE
from console.config import DOUBLE_LITERALS_LINE
from console.config import EMPTY_CELL
from console.config import HEALTHY_SHIP_CELL
from console.config import BROKEN_SHIP_CELL
from console.config import MISSED_SHOT_CELL
from core.constants import GAME_TITLE
from core.constants import AUTHOR_LINE


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_game_title() -> None:
    print(divider('*'))
    print(c_text(GAME_TITLE))
    print(divider('-'))
    print(r_align_text(AUTHOR_LINE))
    print(divider('*'))


def game_initialisation():
    clear_terminal()
    show_game_title()


def instructions():
    print('\n' + r_align_text('========================'))
    print(r_align_text("Type in 'help' for help"))
    print(divider('='))


def show_help():
    game_initialisation()
    print("Type in target coordinates to shot | (Player) > C:3")
    print("Type in 'inspect <ship_name>' to get ship info | " +
          "avaliable ship names: d4, d3_1, d3_2, d2_1, d2_2, d2_3, d1_1, d1_2, d1_3, d1_4")
    print("Type in 'exprort history' to export game history in JSON")
    print(divider('-'))
    print("Type in 'back' to get back to the game")
    print(divider('='))


def execute_command(player: object, command: str, journal: object, game_over: bool) -> bool:
    if not game_over:
        if command[0].lower() in 'abcdefghij' \
            and command[1] == ':' \
                and command[2:] in (str(x) for x in range(1, 11)):
            literal_index = 'abcdefghij'.index(command[0].lower())
            digit = int(command[2:])
            successful_atack = player.atack(literal_index=literal_index, digit=digit)
            return (True, None, successful_atack)
        if command.lower().split()[0] == 'inspect':
            ship_name = command.lower().split()[1]
            try:
                ship_info = player.gameboard.inspect_ship(ship_name)
                return(True, ship_info, True)
            except Exception as e:
                return (False, str(e), True)
        if command.lower() == 'export history':
            try:
                journal.export_game_history_json()
                return (True, "History exported", True)
            except Exception as e:
                return (True, str(e), True)
    if command.lower() == 'help':
        return (True, 'help', None)
    if command.lower() == 'exit':
        exit()
    if command.lower() == 'restart':
        pass
    return (False, f'Invalid command: {command}', None)


def draw_gameboard_line(gameboard, line_index, is_enemy_gameboard):
    gameboard_line_cells = []
    for cell in gameboard[line_index]:
        if cell == 0 or cell == 4:
            gameboard_line_cells.append(EMPTY_CELL)
        elif cell == 1:
            if is_enemy_gameboard:
                gameboard_line_cells.append(EMPTY_CELL)
            else:
                gameboard_line_cells.append(HEALTHY_SHIP_CELL)
        elif cell == 2:
            gameboard_line_cells.append(BROKEN_SHIP_CELL)
        else:
            gameboard_line_cells.append(MISSED_SHOT_CELL)
    gameboard_line_cells = '|'.join(gameboard_line_cells)
    return gameboard_line_cells


def refresh_screen(display_data: tuple, command_response: str, winner: str) -> None:
    left_username, right_username,\
        left_gameboard, right_gameboard = display_data
    clear_terminal()
    show_game_title()
    if winner is not None:
        print(c_text(t_green_bold(f"{winner} won this game!")))
    if TERMINAL_FIT_2_BOARDS_IN_ONE_ROW:
        print(display_players_line(left_username, right_username))
        print(DOUBLE_LITERALS_LINE)
        print(DOUBLE_BOARD_ROW_DIVIDER)
        for line_index in range(10):
            chr_left = 4 if line_index < 9 else 3
            space_left = ' ' * chr_left + f'{line_index + 1}  |'
            left_gameboard_line_cells = draw_gameboard_line(left_gameboard, line_index, False)
            right_gameboard_line_cells = draw_gameboard_line(right_gameboard, line_index, True)
            print(space_left + left_gameboard_line_cells + '|' +
                  ' ' * SPACE_BETWEEN_BOARDS + space_left + right_gameboard_line_cells + '|')
            print(DOUBLE_BOARD_ROW_DIVIDER)
    else:
        print('\n' + c_text(f'\033[4m{left_username}\033[0m') + '\n')
        print(LITERALS_LINE)
        print(' ' * 7 + '--' * 20 + '-')
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
            print(' ' * 7 + '--' * 20 + '-')
        print('\n' + c_text(f'\033[4m{right_username}\033[0m') + '\n')
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
    instructions()
    if command_response is not None:
        print(t_yellow(command_response))
        print(divider("-"))


def ai_atack_animation():
    for i in range(2):
        print(t_yellow(' Ai atack \\'), end='\r')
        sleep(1)
        print(t_yellow(' Ai atack /'), end='\r')
        sleep(1)


def ai_atack(ai_player: object, journal: object) -> None:
    ai_atack_animation()
    literal_target = randint(0, 9)
    digit_target = randint(0, 9)
    ai_player.atack(literal_target, digit_target)
