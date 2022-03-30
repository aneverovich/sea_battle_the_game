from random import randint
from random import randrange
from core.journal import Journal
from core.player import Player
from core.gameboard import Gameboard
from console.terminal import Terminal


class Game():

    def __init__(self, mode='terminal'):
        self.journal = Journal()
        self.mode = mode
        self.over = False
        self.winner = None
        self.godmode = False
        self.show_help = False
        self.level_to_display = 0
        self.command_response = None
        self.player_move = True
        self.player_freeze_move_qty = 0
        self.ai_player_freeze_move_qty = 0
        self.__display_game_title()
        self.submarines_mode = self.__ask_for_submarines()
        self.bombs_allowed = self.__ask_for_bombs()
        self.player_gameboard = Gameboard()
        self.ai_gameboard = Gameboard()
        self.player = Player(
            name=self.__choose_player_name(),
            gameboard=self.player_gameboard,
            enemy_gameboard=self.ai_gameboard,
            journal=self.journal
        )
        self.ai_player = Player(
            name='ArtificalIntelligence',
            gameboard=self.ai_gameboard,
            enemy_gameboard=self.player_gameboard,
            journal=self.journal
        )
        self.player_gameboard.ships_auto_arrangement()
        self.ai_gameboard.ships_auto_arrangement()
        if self.submarines_mode:
            self.player_gameboard.submarines_auto_arrangement()
            self.ai_gameboard.submarines_auto_arrangement()
        if self.bombs_allowed:
            self.player_gameboard.bombs_auto_arrangement()
            self.ai_gameboard.bombs_auto_arrangement()

    def restart(self):
        self.__init__()

    def play(self):
        self.__display_game_title()
        if self.show_help:
            self.__display_help()
        else:
            self.__display_gameboards()
        self.command_response = None
        if self.player_move:
            command = self.__ask_for_command()
            command_execution_result = self.__execute_command(command)
            self.__check_command_execution_result(command, command_execution_result)
        else:
            ai_attack_response = self.__ai_attack()
            self.__check_ai_attack_response(ai_attack_response)

    def __execute_command(self, command):
        if command[0].lower() in 'abcdefghij' and command[1] == ':':
            return self.__player_attack_command_handler(command)
        elif command.lower().split()[0] == 'inspect':
            return self.__inspect_command_handler(command)
        elif command.lower() == 'help':
            return self.__help_command_handler()
        elif command.lower() == 'back':
            return self.__back_command_handler()
        elif command.lower() == 'export history':
            return self.__export_history_command_handler()
        elif command.lower() == 'level up':
            return self.__level_up_command_handler()
        elif command.lower() == 'level down':
            return self.__level_down_command_handler()
        elif command.lower() == 'godmode on':
            return self.__godmode_on_command_handler()
        elif command.lower() == 'godmode off':
            return self.__godmode_off_command_handler()
        elif command.lower() == 'restart':
            return self.__restart_command_handler()
        elif command.lower() == 'exit':
            return self.__exit_command_handler()
        else:
            return self.__invalid_command_handler()

    def __player_attack_command_handler(self, command):
        splited_command = command.split(':')
        letter = splited_command[0].upper()
        digit = int(splited_command[1])
        level = 0
        if len(splited_command) == 3:
            level = int(splited_command[2])
        attack_response = self.player.attack(letter, digit, level, self.submarines_mode)
        if attack_response["bomb"] and not attack_response["exploded"]:
            self.player_freeze_move_qty += 1
        if attack_response["game_over"]:
            self.winner = self.player.name
        return self.__dict_response(
            valid_command=True,
            player_move=attack_response["successful_attack"]
        )

    def __inspect_command_handler(self, command):
        object_code = command.lower().split()[1]
        try:
            self.command_response = self.player.gameboard.inspect(object_code)
            return self.__dict_response(valid_command=True, player_move=True)
        except Exception as e:
            self.command_response = str(e)
            return self.__dict_response(valid_command=False, player_move=True)

    def __export_history_command_handler(self):
        try:
            self.journal.export_game_history_json()
            self.command_response = "History exported"
            return self.__dict_response(valid_command=True, player_move=True)
        except Exception as e:
            self.command_response = str(e)
            return self.__dict_response(valid_command=False, player_move=True)

    def __help_command_handler(self):
        self.show_help = True
        return self.__dict_response(valid_command=True, player_move=True)

    def __back_command_handler(self):
        self.show_help = False
        return self.__dict_response(valid_command=True, player_move=True)

    def __invalid_command_handler(self):
        self.level_to_display += 1 if self.level_to_display < 0 else 0
        return self.__dict_response(valid_command=False, player_move=False)

    def __level_up_command_handler(self):
        self.level_to_display += 1 if self.level_to_display < 0 else 0
        return self.__dict_response(valid_command=True, player_move=True)

    def __level_down_command_handler(self):
        self.level_to_display -= 1 if self.level_to_display > -10 else 0
        return self.__dict_response(valid_command=True, player_move=True)

    def __godmode_on_command_handler(self):
        self.godmode = True
        return self.__dict_response(valid_command=True, player_move=True)

    def __godmode_off_command_handler(self):
        self.godmode = False
        return self.__dict_response(valid_command=True, player_move=True)

    def __restart_command_handler(self):
        self.restart()
        return self.__dict_response(valid_command=True, player_move=True)

    def __exit_command_handler(self):
        self.over = True
        return self.__dict_response(valid_command=True, player_move=True)

    def __check_command_execution_result(self, command, command_execution_result):
        if not command_execution_result["valid_command"]:
            self.command_response = f"invalid command: {command}"
        else:
            if not command_execution_result["player_move"]:
                if self.ai_player_freeze_move_qty == 0:
                    self.player_move = False
                else:
                    self.ai_player_freeze_move_qty -= 1

    def __ai_attack(self):
        if self.mode == 'terminal':
            Terminal.ai_atack_animation()
        letter_index = randint(0, 9)
        letter_target = 'ABCDEFGHIJ'[letter_index]
        digit_target = randint(1, 10)
        level = 0
        if self.submarines_mode:
            level = randrange(0, -10, -1)
        return self.ai_player.attack(letter_target, digit_target, level, self.submarines_mode)

    def __check_ai_attack_response(self, ai_attack_response):
        if ai_attack_response["successful_attack"]:
            if ai_attack_response["game_over"]:
                self.winner = self.ai_player.name
                self.player_move = True
        else:
            if ai_attack_response["bomb"]:
                self.ai_player_freeze_move_qty += 1
            if self.player_freeze_move_qty == 0:
                self.player_move = True
            else:
                self.player_freeze_move_qty -= 1

    def __display_game_title(self):
        if self.mode == 'terminal':
            Terminal.display_game_title()
        else:
            pass

    def __display_gameboards(self):
        if self.mode == 'terminal':
            Terminal.display_gameboards(
                (self.player.name,
                 self.ai_player.name,
                 self.player_gameboard.battlefield[self.level_to_display],
                 self.ai_player.gameboard.battlefield[self.level_to_display]),
                self.level_to_display,
                self.command_response,
                self.winner,
                self.godmode
            )
        else:
            pass

    def __display_help(self):
        if self.mode == 'terminal':
            Terminal.display_help()
        else:
            pass

    def __choose_player_name(self):
        if self.mode == 'terminal':
            return Terminal.choose_player_name()
        else:
            pass

    def __ask_for_submarines(self):
        if self.mode == 'terminal':
            return Terminal.ask_for_submarines()
        else:
            pass

    def __ask_for_bombs(self):
        if self.mode == 'terminal':
            return Terminal.ask_for_bombs()
        else:
            pass

    def __ask_for_command(self):
        if self.mode == 'terminal':
            return Terminal.ask_for_command(self.player.name)
        else:
            pass

    def __dict_response(self, valid_command, player_move):
        return {
            'valid_command': valid_command,
            'player_move': player_move
        }
