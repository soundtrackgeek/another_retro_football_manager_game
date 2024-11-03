import pygame
from database.database import FootballDB

class TeamView:
    POSITION_PRIORITY = {
        'GK': 0,
        'DEF': 1,
        'MID': 2,
        'ATT': 3
    }

    def __init__(self, screen, font, team_id):
        self.screen = screen
        self.font = font
        self.team_id = team_id
        self.db = FootballDB()
        self.players = self.db.get_team_players(team_id)
        # Sort players by position
        self.players.sort(key=lambda x: self.POSITION_PRIORITY.get(x['position'], 999))
        print(f"Number of players loaded: {len(self.players)}")  # Debug print
        if len(self.players) > 0:
            print(f"First player: {self.players[0]}")  # Debug print
        self.selected_index = 0
        self.scroll_offset = 0
        self.visible_players = 8
        self.spacing = 50  # Increased spacing for more stats
        self.max_selected_visible = 4  # Maximum number of visible selected players
        self.max_others_visible = 4    # Maximum number of visible other players
        self.others_scroll_offset = 0  # Separate scroll offset for unselected players

    def handle_input(self, key):
        selected_players = [p for p in self.players if p['is_selected']]
        other_players = [p for p in self.players if not p['is_selected']]

        if key == pygame.K_UP:
            if self.selected_index > 0:
                self.selected_index -= 1
                # Adjust scroll offset based on whether we're in selected or other players section
                if self.selected_index < len(selected_players):
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset = self.selected_index
                else:
                    other_index = self.selected_index - len(selected_players)
                    if other_index < self.others_scroll_offset:
                        self.others_scroll_offset = other_index

        elif key == pygame.K_DOWN:
            if self.selected_index < len(self.players) - 1:
                self.selected_index += 1
                # Adjust scroll offset based on whether we're in selected or other players section
                if self.selected_index < len(selected_players):
                    if self.selected_index >= self.scroll_offset + self.max_selected_visible:
                        self.scroll_offset = self.selected_index - self.max_selected_visible + 1
                else:
                    other_index = self.selected_index - len(selected_players)
                    if other_index >= self.others_scroll_offset + self.max_others_visible:
                        self.others_scroll_offset = other_index - self.max_others_visible + 1

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

        # Draw section headers
        selected_text = self.font.render("SELECTED SQUAD (First 11)", True, (255, 255, 0))
        self.screen.blit(selected_text, (50, 80))
        
        others_text = self.font.render("OTHER SQUAD PLAYERS", True, (255, 255, 0))
        self.screen.blit(others_text, (50, 400))

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

        # Split players into selected and other groups
        selected_players = [p for p in self.players if p['is_selected']]
        other_players = [p for p in self.players if not p['is_selected']]

        # Draw selected players (with scrolling)
        selected_y = 160
        visible_selected = selected_players[self.scroll_offset:self.scroll_offset + self.max_selected_visible]
        
        for i, player in enumerate(visible_selected):
            y = selected_y + (i * self.spacing)
            color = (0, 255, 0)  # Green for selected
            if self.players.index(player) == self.selected_index:
                color = (255, 255, 0)  # Yellow for cursor

            self.draw_player_row(player, y, color)

        # Draw other players (with separate scrolling)
        others_y = 440
        visible_others = other_players[self.others_scroll_offset:self.others_scroll_offset + self.max_others_visible]
        
        for i, player in enumerate(visible_others):
            y = others_y + (i * self.spacing)
            color = (255, 255, 255)  # White for non-selected
            if self.players.index(player) == self.selected_index:
                color = (255, 255, 0)  # Yellow for cursor

            self.draw_player_row(player, y, color)

        # Draw scroll indicators for selected players
        if self.scroll_offset > 0:
            up_arrow = self.font.render("↑", True, (255, 255, 255))
            self.screen.blit(up_arrow, (self.screen.get_width() // 2, 140))

        if self.scroll_offset + self.max_selected_visible < len(selected_players):
            down_arrow = self.font.render("↓", True, (255, 255, 255))
            self.screen.blit(down_arrow, (self.screen.get_width() // 2, 350))

        # Draw scroll indicators for other players
        if self.others_scroll_offset > 0:
            up_arrow = self.font.render("↑", True, (255, 255, 255))
            self.screen.blit(up_arrow, (self.screen.get_width() // 2, 420))

        if self.others_scroll_offset + self.max_others_visible < len(other_players):
            down_arrow = self.font.render("↓", True, (255, 255, 255))
            self.screen.blit(down_arrow, (self.screen.get_width() // 2, 630))

        # Draw navigation hints
        hints = ["ESC - Back", "RETURN - View Details"]
        y = self.screen.get_height() - 30
        for hint in hints:
            text = self.font.render(hint, True, (255, 255, 255))
            text_rect = text.get_rect(bottom=y)
            text_rect.x = 20
            self.screen.blit(text, text_rect)
            y -= 30

    def draw_player_row(self, player, y, color):
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

    def calculate_rating(self, player):
        if player['position'] == 'GK':
            return player['goalkeeping']
        elif player['position'] == 'DEF':
            return (player['defending'] * 2 + player['speed']) // 3
        elif player['position'] == 'MID':
            return (player['attacking'] + player['defending'] + player['speed']) // 3
        else:  # ATT
            return (player['attacking'] * 2 + player['speed']) // 3
