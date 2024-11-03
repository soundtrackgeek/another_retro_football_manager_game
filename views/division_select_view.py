import pygame
from database.database import FootballDB

class DivisionSelectView:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.db = FootballDB()
        self.selected_index = 0
        self.divisions = [
            "Premier League",
            "Championship",
            "League One",
            "League Two"
        ]

    def handle_input(self, key):
        if key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.divisions)
        elif key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.divisions)
        elif key == pygame.K_RETURN:
            return self.selected_index + 1  # Division IDs start from 1
        return None

    def draw(self):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        spacing = 50

        # Draw title
        title = self.font.render("SELECT DIVISION", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, center_y - 150))
        self.screen.blit(title, title_rect)

        # Draw divisions
        for i, division in enumerate(self.divisions):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(division, True, color)
            text_rect = text.get_rect(center=(center_x, center_y - 50 + i * spacing))
            self.screen.blit(text, text_rect)
