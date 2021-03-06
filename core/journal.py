import json
from datetime import datetime


class Journal():

    def __init__(self):
        self.game_history = {'history': []}

    def add_event(self, player_name, event):
        self.game_history["history"].append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'player': player_name,
            'event': event
        })

    def export_game_history_json(self):
        with open(f'core/game_history/{datetime.now().strftime("%H%M%S")}_game_history.json', 'w') as json_file:
            json.dump(self.game_history, json_file, allow_nan=False)
