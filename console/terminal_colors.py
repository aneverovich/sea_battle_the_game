HIGHLIGHT_FG__PURPLE = '\033[95m'
HIGHLIGHT_FG__BLUE = '\033[94m'
HIGHLIGHT_FG__GREEN = '\033[92m'
HIGHLIGHT_FG__YELLOW = '\033[93m'
HIGHLIGHT_FG__RED = '\033[91m'

HIGHLIGHT__CLEAR = '\033[0m'
HIGHLIGHT__BOLD = '\033[1m'


def t_red(text: str) -> str:
    return f'{HIGHLIGHT_FG__RED}{text}{HIGHLIGHT__CLEAR}'


def t_red_bold(text: str) -> str:
    return f'{HIGHLIGHT_FG__RED}{HIGHLIGHT__BOLD}{text}{HIGHLIGHT__CLEAR}'


def t_green(text: str) -> str:
    return f'{HIGHLIGHT_FG__GREEN}{text}{HIGHLIGHT__CLEAR}'


def t_green_bold(text: str) -> str:
    return f'{HIGHLIGHT_FG__GREEN}{HIGHLIGHT__BOLD}{text}{HIGHLIGHT__CLEAR}'


def t_purple(text: str) -> str:
    return f'{HIGHLIGHT_FG__PURPLE}{text}{HIGHLIGHT__CLEAR}'


def t_purple_bold(text: str) -> str:
    return f'{HIGHLIGHT_FG__PURPLE}{HIGHLIGHT__BOLD}{text}{HIGHLIGHT__CLEAR}'


def t_yellow(text: str) -> str:
    return f'{HIGHLIGHT_FG__YELLOW}{text}{HIGHLIGHT__CLEAR}'


def t_yellow_bold(text: str) -> str:
    return f'{HIGHLIGHT_FG__YELLOW}{HIGHLIGHT__BOLD}{text}{HIGHLIGHT__CLEAR}'


def t_blue(text: str) -> str:
    return f'{HIGHLIGHT_FG__BLUE}{text}{HIGHLIGHT__CLEAR}'


def t_blue_bold(text: str) -> str:
    return f'{HIGHLIGHT_FG__BLUE}{HIGHLIGHT__BOLD}{text}{HIGHLIGHT__CLEAR}'
