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
