import pygame
from database.database import FootballDB

class TeamView:
    def __init__(self, screen, font, team_id):
        self.screen = screen
        self.font = font
        self.team_id = team_id
        self.db = FootballDB()
        self.players = self.db.get_team_players(team_id)
        print(f"Number of players loaded: {len(self.players)}")  # Debug print
        if len(self.players) > 0:
            print(f"First player: {self.players[0]}")  # Debug print
        self.selected_index = 0
        self.scroll_offset = 0
        self.visible_players = 10
        self.spacing = 50  # Increased spacing for more stats

    def handle_input(self, key):
        if key == pygame.K_UP:
            if self.selected_index > 0:
                self.selected_index -= 1
                if self.selected_index < self.scroll_offset:
                    self.scroll_offset = self.selected_index
        elif key == pygame.K_DOWN:
            if self.selected_index < len(self.players) - 1:
                self.selected_index += 1
                if self.selected_index >= self.scroll_offset + self.visible_players:
                    self.scroll_offset = self.selected_index - self.visible_players + 1
        elif key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self):
        # Draw title
        title = self.font.render("TEAM SQUAD", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(title, title_rect)

        # Draw column headers
        headers = ["Name", "Pos", "Age", "Att", "Def", "Gk", "Sta", "Spd", "Mor"]
        header_x = 50
        header_y = 80
        for header in headers:
            text = self.font.render(header, True, (255, 255, 255))
            self.screen.blit(text, (header_x, header_y))
            if header == "Name":
                header_x += 200  # More space for name
            else:
                header_x += 60   # Fixed width for stats

        # Draw players
        if not self.players:
            # Display message if no players found
            no_players = self.font.render("No players found", True, (255, 255, 255))
            no_players_rect = no_players.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(no_players, no_players_rect)
            return

        # Draw scrolling indicators
        if self.scroll_offset > 0:
            up_arrow = self.font.render("↑", True, (255, 255, 255))
            self.screen.blit(up_arrow, (self.screen.get_width() // 2, 100))

        if self.scroll_offset + self.visible_players < len(self.players):
            down_arrow = self.font.render("↓", True, (255, 255, 255))
            self.screen.blit(down_arrow, (self.screen.get_width() // 2, 550))

        # Draw players
        start_y = 120
        end_index = min(self.scroll_offset + self.visible_players, len(self.players))
        
        for i in range(self.scroll_offset, end_index):
            player = self.players[i]
            x = 50
            y = start_y + ((i - self.scroll_offset) * self.spacing)
            
            # Highlight selected player
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)

            try:
                # Player name
                name = f"{player['first_name']} {player['last_name']}"
                text = self.font.render(name, True, color)
                self.screen.blit(text, (x, y))
                x += 200

                # Player stats
                stats = [
                    player['position'],
                    str(player['age']),
                    str(player['attacking']),
                    str(player['defending']),
                    str(player['goalkeeping']),
                    str(player['stamina']),
                    str(player['speed']),
                    str(player['morale'])
                ]
                
                for stat in stats:
                    text = self.font.render(stat, True, color)
                    self.screen.blit(text, (x, y))
                    x += 60
            except KeyError as e:
                print(f"Error accessing player data: {e}")
                print(f"Player data: {player}")

        # Draw navigation hint
        hint = self.font.render("ESC - Back", True, (255, 255, 255))
        hint_rect = hint.get_rect(bottomright=(self.screen.get_width() - 20, 
                                             self.screen.get_height() - 20))
        self.screen.blit(hint, hint_rect)
