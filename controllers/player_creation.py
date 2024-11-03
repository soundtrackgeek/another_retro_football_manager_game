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
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        first_names.append(row[0].strip())
                        last_names.append(row[1].strip())
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        first_names.append(row[0].strip())
                        last_names.append(row[1].strip())
        return first_names, last_names

    def get_stat_range(self, base_range, reputation):
        """Adjust stat range based on team reputation"""
        min_val, max_val = base_range
        # Reputation is 50-92, normalize it to -20 to +20 adjustment
        rep_adjust = ((reputation - 70) / 20) * 15
        
        new_min = max(1, min(99, min_val + rep_adjust))
        new_max = max(1, min(99, max_val + rep_adjust))
        return (int(new_min), int(new_max))

    def generate_player(self, team_id, position, reputation):
        # Base stats with position-specific adjustments
        base_stats = {
            'GK':  {'attacking': (20, 40), 'defending': (30, 50), 'goalkeeping': (50, 85)},
            'DEF': {'attacking': (20, 55), 'defending': (50, 85), 'goalkeeping': (15, 35)},
            'MID': {'attacking': (40, 75), 'defending': (40, 75), 'goalkeeping': (15, 35)},
            'ATT': {'attacking': (50, 85), 'defending': (20, 55), 'goalkeeping': (15, 35)}
        }

        stats = base_stats[position]
        
        # Adjust stats based on reputation
        adjusted_stats = {
            key: self.get_stat_range(value, reputation) 
            for key, value in stats.items()
        }

        # Calculate value range based on reputation (exponential scaling)
        base_value = reputation * 50000
        max_value_multiplier = (reputation / 50) ** 2  # Exponential growth for higher reputation
        value_range = (
            int(base_value * 0.7),
            int(base_value * max_value_multiplier)
        )

        # Calculate wages range (roughly 2% of value per year)
        wages_range = (
            int(value_range[0] * 0.02 / 52),  # Weekly wage
            int(value_range[1] * 0.02 / 52)
        )

        # Generate player age with bias based on reputation
        # Higher reputation teams tend to have more prime-age players
        if reputation > 85:
            age = random.randint(23, 32)
        elif reputation > 75:
            age = random.randint(20, 33)
        else:
            age = random.randint(17, 35)

        return {
            'first_name': random.choice(self.first_names),
            'last_name': random.choice(self.last_names),
            'team_id': team_id,
            'age': age,
            'position': position,
            'attacking': random.randint(*adjusted_stats['attacking']),
            'defending': random.randint(*adjusted_stats['defending']),
            'goalkeeping': random.randint(*adjusted_stats['goalkeeping']),
            'stamina': random.randint(max(50, reputation-20), min(99, reputation+10)),
            'speed': random.randint(max(50, reputation-20), min(99, reputation+10)),
            'morale': random.randint(60, 100),
            'value': random.randint(*value_range),
            'wages': random.randint(*wages_range),
            'contract_years': random.randint(1, 5)
        }

    def generate_squad(self, team_id, reputation):
        squad = []
        # Generate specific number of players for each position
        positions = {
            'GK': 3,
            'DEF': 6,
            'MID': 6,
            'ATT': 5
        }
        
        for position, count in positions.items():
            for _ in range(count):
                squad.append(self.generate_player(team_id, position, reputation))
                
        return squad
