import pygame
from controllers.team_selection import TeamSelection
from database.database import FootballDB  # Add this import

class PlayerSelectionView:
    def __init__(self, screen, font, team_id):
        self.screen = screen
        self.font = font
        self.team_id = team_id
        self.selected_index = 0
        self.scroll_offset = 0
        self.visible_players = 8
        self.spacing = 50
        self.db = FootballDB()
        self.players = self.db.get_team_players(team_id)
        self.players.sort(key=lambda x: self.POSITION_PRIORITY.get(x['position'], 999))
        self.team_selection = TeamSelection()
        self.team_selection.load_selection(team_id)  # Load existing selection

    POSITION_PRIORITY = {
        'GK': 0,
        'DEF': 1,
        'MID': 2,
        'ATT': 3
    }

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
        elif key == pygame.K_SPACE:
            if self.players and len(self.players) > self.selected_index:
                self.team_selection.toggle_player(self.players[self.selected_index])
        elif key == pygame.K_RETURN:
            if self.team_selection.is_valid_selection():
                self.team_selection.save_selection(self.team_id)  # Save selection
                return "SELECTION_COMPLETE"
        elif key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self):
        # Draw title
        title = self.font.render("SELECT STARTING 11", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(title, title_rect)

        # Draw selection status
        selected_count = len(self.team_selection.selected_players)
        status = f"Selected: {selected_count}/11"
        status_text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(status_text, (50, 80))

        # Draw column headers
        headers = ["", "Name", "Pos", "Rating"]
        header_positions = [30, 50, 600, 800]
        for header, x_pos in zip(headers, header_positions):
            text = self.font.render(header, True, (255, 255, 255))
            self.screen.blit(text, (x_pos, 120))

        # Draw players
        start_y = 160
        end_index = min(self.scroll_offset + self.visible_players, len(self.players))
        
        for i in range(self.scroll_offset, end_index):
            player = self.players[i]
            y = start_y + ((i - self.scroll_offset) * self.spacing)
            
            # Determine text color
            if i == self.selected_index:
                color = (255, 255, 0)  # Yellow for cursor
            elif self.team_selection.is_selected(player['id']):
                color = (0, 255, 0)    # Green for selected
            else:
                color = (255, 255, 255) # White for unselected

            # Draw selection marker
            if self.team_selection.is_selected(player['id']):
                star = self.font.render("*", True, color)
                self.screen.blit(star, (30, y))

            # Draw player info
            name = f"{player['first_name']} {player['last_name']}"
            text = self.font.render(name, True, color)
            self.screen.blit(text, (50, y))

            text = self.font.render(player['position'], True, color)
            self.screen.blit(text, (600, y))

            rating = self.calculate_rating(player)
            text = self.font.render(str(rating), True, color)
            self.screen.blit(text, (800, y))

        # Draw navigation hints
        hints = ["SPACE - Select/Deselect", "RETURN - Confirm (when 11 selected)", "ESC - Back"]
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
