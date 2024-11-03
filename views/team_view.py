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
        self.visible_players = 8
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
        elif key == pygame.K_RETURN:
            if self.players and len(self.players) > self.selected_index:
                return ("SHOW_PLAYER", self.players[self.selected_index])
        return None

    def draw(self):
        # Draw title
        title = self.font.render("TEAM SQUAD", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(title, title_rect)

        # Draw column headers with wider spacing
        headers = ["Name", "Pos", "Rating"]
        header_positions = [50, 600, 800]  # Adjusted x positions for headers
        header_y = 120  # Moved down from 80
        
        for header, x_pos in zip(headers, header_positions):
            text = self.font.render(header, True, (255, 255, 255))
            self.screen.blit(text, (x_pos, header_y))

        # Draw players
        if not self.players:
            no_players = self.font.render("No players found", True, (255, 255, 255))
            no_players_rect = no_players.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(no_players, no_players_rect)
            return

        # Draw scrolling indicators
        if self.scroll_offset > 0:
            up_arrow = self.font.render("↑", True, (255, 255, 255))
            self.screen.blit(up_arrow, (self.screen.get_width() // 2, 60))  # Moved down from 100

        if self.scroll_offset + self.visible_players < len(self.players):
            down_arrow = self.font.render("↓", True, (255, 255, 255))
            self.screen.blit(down_arrow, (self.screen.get_width() // 2, 550))

        # Draw players with wider spacing
        start_y = 160  # Moved down from 120
        end_index = min(self.scroll_offset + self.visible_players, len(self.players))
        
        for i in range(self.scroll_offset, end_index):
            player = self.players[i]
            y = start_y + ((i - self.scroll_offset) * self.spacing)
            
            # Highlight selected player
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)

            try:
                # Player name (left aligned)
                name = f"{player['first_name']} {player['last_name']}"
                text = self.font.render(name, True, color)
                self.screen.blit(text, (50, y))

                # Position (center aligned at its column)
                text = self.font.render(player['position'], True, color)
                pos_rect = text.get_rect(x=600, y=y)
                self.screen.blit(text, pos_rect)

                # Rating (center aligned at its column)
                rating = self.calculate_rating(player)
                text = self.font.render(str(rating), True, color)
                rating_rect = text.get_rect(x=800, y=y)
                self.screen.blit(text, rating_rect)

            except KeyError as e:
                print(f"Error accessing player data: {e}")

        # Draw navigation hints
        hints = ["ESC - Back", "RETURN - View Details"]
        y = self.screen.get_height() - 30
        for hint in hints:
            text = self.font.render(hint, True, (255, 255, 255))
            text_rect = text.get_rect(bottom=y)
            text_rect.x = 20
            self.screen.blit(text, text_rect)
            y -= 30

    def calculate_rating(self, player):
        if player['position'] == 'GK':
            return player['goalkeeping']
        elif player['position'] == 'DEF':
            return (player['defending'] * 2 + player['speed']) // 3
        elif player['position'] == 'MID':
            return (player['attacking'] + player['defending'] + player['speed']) // 3
        else:  # ATT
            return (player['attacking'] * 2 + player['speed']) // 3
