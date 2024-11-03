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

    def handle_input(self, key):
        if key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.teams)
        elif key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.teams)
        elif key == pygame.K_RETURN:
            return self.teams[self.selected_index]['id']
        elif key == pygame.K_ESCAPE:
            return -1  # Signal to go back
        return None

    def draw(self):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        spacing = 30

        # Draw title
        title = self.font.render("SELECT TEAM", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 50))
        self.screen.blit(title, title_rect)

        # Draw teams
        start_y = 150
        for i, team in enumerate(self.teams):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(team['name'], True, color)
            text_rect = text.get_rect(center=(center_x, start_y + i * spacing))
            self.screen.blit(text, text_rect)

        # Draw navigation hint
        hint = self.font.render("ESC - Back", True, (255, 255, 255))
        hint_rect = hint.get_rect(bottomright=(self.screen.get_width() - 20, self.screen.get_height() - 20))
        self.screen.blit(hint, hint_rect)
