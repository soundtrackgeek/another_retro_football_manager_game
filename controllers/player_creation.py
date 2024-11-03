import random
import csv
import os

class PlayerCreator:
    def __init__(self):
        self.first_names, self.last_names = self.load_player_names()

    def load_player_names(self):
        first_names = []
        last_names = []
        file_path = os.path.join('database', 'playernames.csv')
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    first_names.append(row[0])
                    last_names.append(row[1])
        return first_names, last_names

    def generate_player(self, team_id, position):
        # Base stats with position-specific adjustments
        base_stats = {
            'GK':  {'attacking': (30, 50), 'defending': (40, 60), 'goalkeeping': (60, 95)},
            'DEF': {'attacking': (30, 65), 'defending': (60, 95), 'goalkeeping': (20, 40)},
            'MID': {'attacking': (50, 85), 'defending': (50, 85), 'goalkeeping': (20, 40)},
            'ATT': {'attacking': (60, 95), 'defending': (30, 65), 'goalkeeping': (20, 40)}
        }

        stats = base_stats[position]
        return {
            'first_name': random.choice(self.first_names),
            'last_name': random.choice(self.last_names),
            'team_id': team_id,
            'age': random.randint(16, 35),
            'position': position,
            'attacking': random.randint(*stats['attacking']),
            'defending': random.randint(*stats['defending']),
            'goalkeeping': random.randint(*stats['goalkeeping']),
            'stamina': random.randint(50, 100),
            'speed': random.randint(50, 100),
            'morale': random.randint(60, 100),
            'value': random.randint(100000, 15000000),
            'wages': random.randint(1000, 100000),
            'contract_years': random.randint(1, 5)
        }

    def generate_squad(self, team_id):
        squad = []
        # Generate specific number of players for each position
        positions = {
            'GK': 3,   # 3 Goalkeepers
            'DEF': 6,  # 6 Defenders
            'MID': 6,  # 6 Midfielders
            'ATT': 5   # 5 Attackers
        }
        
        for position, count in positions.items():
            for _ in range(count):
                squad.append(self.generate_player(team_id, position))
                
        return squad
