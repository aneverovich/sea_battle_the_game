import os
from console.terminal_colors import t_green, t_red_bold, t_yellow_bold

VERSION = "0.2"
GAME_TITLE = f"Sea Battle the Game | OOP python based version (v.{VERSION})"
AUTHOR_LINE = "by Anton Neviarovich"

LITERALS = '  A   B   C   D   E   F   G   H   I   J'

HEALTHY_SHIP_CELL = t_green('[#]')
EMPTY_CELL = '   '
BROKEN_SHIP_CELL = t_red_bold('[X]')
BOMB_CELL = t_red_bold('[B]')
EXPLODED_BOMB_CELL = t_yellow_bold('[B]')
MISSED_SHOT_CELL = t_yellow_bold(' * ')

# Check the terminal width (columns) and height (rows)
columns, rows = os.get_terminal_size()
TERMINAL_WIDTH = int(columns)

GAMEBOARD_WIDTH = 54
LEFT_TAB = ' ' * 7
BOARD_ROW_DIVIDER = LEFT_TAB + '--' * 20 + '-'
TERMINAL_FIT_2_BOARDS_IN_ONE_ROW = TERMINAL_WIDTH // GAMEBOARD_WIDTH >= 2
if TERMINAL_FIT_2_BOARDS_IN_ONE_ROW:
    SPACE_BETWEEN_BOARDS = TERMINAL_WIDTH - GAMEBOARD_WIDTH * 2  # COLUMNS
    DOUBLE_BOARD_ROW_DIVIDER = BOARD_ROW_DIVIDER + ' ' * SPACE_BETWEEN_BOARDS + BOARD_ROW_DIVIDER
else:
    SPACE_BETWEEN_BOARDS = 3  # ROWS
    DOUBLE_BOARD_ROW_DIVIDER = None

LITERALS_LINE = LEFT_TAB + LITERALS
DOUBLE_LITERALS_LINE = LEFT_TAB + LITERALS + ' ' * SPACE_BETWEEN_BOARDS + ' ' * 9 + LITERALS
