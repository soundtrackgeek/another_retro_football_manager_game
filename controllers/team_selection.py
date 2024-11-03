from database.database import FootballDB

class TeamSelection:
    def __init__(self):
        self.selected_players = {}
        self.db = FootballDB()
        
    def load_selection(self, team_id: int):
        """Load existing selection from database"""
        players = self.db.get_team_players(team_id)
        self.selected_players = {
            p['id']: p for p in players if p['is_selected']
        }
        
    def save_selection(self, team_id: int):
        """Save current selection to database"""
        self.db.save_team_selection(team_id, list(self.selected_players.keys()))
        
    def can_select_player(self, player) -> bool:
        # Check if we can select this player
        if len(self.selected_players) >= 11:
            return False
            
        # If it's a goalkeeper
        if player['position'] == 'GK':
            # Count current goalkeepers
            gk_count = sum(1 for p in self.selected_players.values() 
                          if p['position'] == 'GK')
            return gk_count == 0
            
        # For other positions, just check total count
        return True
        
    def toggle_player(self, player) -> bool:
        player_id = player['id']
        
        # If player is already selected, always allow deselection
        if player_id in self.selected_players:
            del self.selected_players[player_id]
            return True
            
        # Check if we can select this player
        if self.can_select_player(player):
            self.selected_players[player_id] = player  # Store the whole player object
            return True
            
        return False
        
    def is_valid_selection(self) -> bool:
        if len(self.selected_players) != 11:
            return False
            
        # Check if we have exactly one goalkeeper
        gk_count = sum(1 for p in self.selected_players.values() 
                      if p['position'] == 'GK')
        return gk_count == 1
        
    def is_selected(self, player_id: int) -> bool:
        return player_id in self.selected_players

    def get_player_rating(self, player) -> float:
        """Calculate overall rating for a player based on position"""
        if player['position'] == 'GK':
            return player['goalkeeping']
        elif player['position'] == 'DEF':
            return (player['defending'] * 0.7 + 
                   player['stamina'] * 0.2 + 
                   player['speed'] * 0.1)
        elif player['position'] == 'MID':
            return (player['attacking'] * 0.4 + 
                   player['defending'] * 0.4 + 
                   player['stamina'] * 0.1 + 
                   player['speed'] * 0.1)
        elif player['position'] == 'ATT':
            return (player['attacking'] * 0.7 + 
                   player['speed'] * 0.2 + 
                   player['stamina'] * 0.1)
        return 0

    def auto_select_team(self, team_id: int):
        """Automatically select best 11 players in a 4-4-2 formation"""
        # Clear current selection
        self.selected_players = {}
        
        # Get all players from the team
        all_players = self.db.get_team_players(team_id)
        if not all_players:
            return False

        # Group players by position
        players_by_position = {
            'GK': [],
            'DEF': [],
            'MID': [],
            'ATT': []
        }

        # Sort players into positions and calculate their ratings
        for player in all_players:
            pos = player['position']
            if pos in players_by_position:
                players_by_position[pos].append(player)

        # Sort each position group by rating
        for pos in players_by_position:
            players_by_position[pos].sort(
                key=lambda p: self.get_player_rating(p),
                reverse=True
            )

        # Select players according to 4-4-2 formation
        formation = {
            'GK': 1,
            'DEF': 4,
            'MID': 4,
            'ATT': 2
        }

        # Select best players for each position
        for pos, count in formation.items():
            available_players = players_by_position[pos]
            for i in range(min(count, len(available_players))):
                player = available_players[i]
                self.selected_players[player['id']] = player

        # Check if we have a valid selection (11 players)
        if self.is_valid_selection():
            # Save the selection to database
            self.save_selection(team_id)
            return True
        return False
