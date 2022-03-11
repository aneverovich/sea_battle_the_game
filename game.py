from core.player import ConsolePlayer
from core.player import AiPlayer
from core.journal import Journal
from core.gameboard import Gameboard
from console.actions import game_initialisation
from console.actions import refresh_screen
from console.actions import show_help
from console.actions import execute_command
from console.actions import ai_atack


if __name__ == '__main__':
    journal = Journal()
    game_initialisation()
    player_gameboard = Gameboard()
    ai_gameboard = Gameboard()
    player = ConsolePlayer(gameboard=player_gameboard, enemy_gameboard=ai_gameboard, journal=journal)
    ai_player = AiPlayer(gameboard=ai_gameboard, enemy_gameboard=player_gameboard, journal=journal)
    while True:
        player_gameboard.ships_auto_arrangement()
        ai_gameboard.ships_auto_arrangement()
        winner_name = None
        display_data = (
            player.name,
            ai_player.name,
            player_gameboard.board,
            ai_gameboard.board
        )
        while winner_name is None:
            # Player atack
            valid_command = False
            command_response = None
            succesful_atack = False
            while True:
                refresh_screen(display_data, command_response, winner_name)
                command = input(f'({player.name}) > ')
                if command.lower() == 'help':
                    while command != 'back':
                        show_help()
                        command = input(f'({player.name}) > ')
                else:
                    valid_command, command_response, succesful_atack = \
                        execute_command(player, command, journal, game_over=False)
                    if not valid_command:
                        continue
                    if not succesful_atack:
                        break
                if ai_gameboard.game_over:
                    winner_name = player.name
                    break
            if ai_gameboard.game_over:
                break
            # Ai atack
            refresh_screen(display_data, command_response, winner_name)
            ai_atack(ai_player, journal)
            if player_gameboard.game_over:
                winner_name = ai_player.name
        valid_command = False
        while not valid_command:
            refresh_screen(display_data, command_response, winner_name)
            command = input(f"({player.name})> ")
            if command == "restart":
                player.winner, ai_player.winner = False, False
                player_gameboard.reset()
                ai_gameboard.reset()
                break
            elif command == 'help':
                while command != 'back':
                    show_help()
                    command = input(f'({player.name}) > ')
            elif command == 'exit':
                exit()
            else:
                pass
