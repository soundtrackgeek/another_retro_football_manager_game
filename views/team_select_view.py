import pygame
from database.database import FootballDB

class TeamSelectView:
    def __init__(self, screen, font, division_id):
        self.screen = screen
        self.font = font
        self.db = FootballDB()
        self.division_id = division_id
        self.selected_index = 0
        self.teams = self.db.get_teams_in_division(division_id)
        self.scroll_offset = 0
        self.visible_teams = 15  # Number of teams visible at once
        self.spacing = 30

    def handle_input(self, key):
        if key == pygame.K_UP:
            if self.selected_index > 0:  # Only move up if not at first team
                self.selected_index -= 1
                # Adjust scroll if selection goes above visible area
                if self.selected_index < self.scroll_offset:
                    self.scroll_offset = self.selected_index
        elif key == pygame.K_DOWN:
            if self.selected_index < len(self.teams) - 1:  # Only move down if not at last team
                self.selected_index += 1
                # Adjust scroll if selection goes below visible area
                if self.selected_index >= self.scroll_offset + self.visible_teams:
                    self.scroll_offset = self.selected_index - self.visible_teams + 1
        elif key == pygame.K_RETURN:
            return self.teams[self.selected_index]['id']
        elif key == pygame.K_ESCAPE:
            return -1
        return None

    def draw(self):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        # Draw title
        title = self.font.render("SELECT TEAM", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 50))
        self.screen.blit(title, title_rect)

        # Draw teams (only visible portion)
        start_y = 150
        visible_range = range(self.scroll_offset, 
                            min(self.scroll_offset + self.visible_teams, len(self.teams)))
        
        # Draw scroll up indicator if needed
        if self.scroll_offset > 0:
            up_arrow = self.font.render("↑", True, (255, 255, 255))
            self.screen.blit(up_arrow, (center_x - 10, start_y - 60))  # Changed from -25 to -60

        # Draw visible teams
        for i, team_index in enumerate(visible_range):
            color = (255, 255, 0) if team_index == self.selected_index else (255, 255, 255)
            text = self.font.render(self.teams[team_index]['name'], True, color)
            text_rect = text.get_rect(center=(center_x, start_y + i * self.spacing))
            self.screen.blit(text, text_rect)

        # Draw scroll down indicator if needed
        if self.scroll_offset + self.visible_teams < len(self.teams):
            down_arrow = self.font.render("↓", True, (255, 255, 255))
            self.screen.blit(down_arrow, 
                           (center_x - 10, start_y + (self.visible_teams - 1) * self.spacing + 40))  # Changed from +25 to +40

        # Draw navigation hint
        hint = self.font.render("ESC - Back", True, (255, 255, 255))
        hint_rect = hint.get_rect(bottomright=(self.screen.get_width() - 20, self.screen.get_height() - 20))
        self.screen.blit(hint, hint_rect)
