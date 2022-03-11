from console.config import TERMINAL_WIDTH


def divider(divider_type: str) -> str:
    return divider_type * TERMINAL_WIDTH


def c_text(text: str) -> str:
    free_space_left = (TERMINAL_WIDTH - len(text)) // 2
    free_space_right = TERMINAL_WIDTH - free_space_left - len(text)
    return " " * free_space_left + text + " " * free_space_right


def r_align_text(text: str) -> str:
    free_space_left = TERMINAL_WIDTH - len(text)
    return " " * free_space_left + text


def display_players_line(player_1: str, player_2: str) -> str:
    screen_borders_tab_len = 4
    screen_borders_tab = " " * screen_borders_tab_len
    free_space = TERMINAL_WIDTH - len(player_2) - len(player_1) -\
        (2 * screen_borders_tab_len)
    return "\n" + screen_borders_tab + '\033[4m' + player_1 + '\033[0m' + \
        " " * free_space + '\033[4m' + player_2 + '\033[0m' + screen_borders_tab + "\n"
