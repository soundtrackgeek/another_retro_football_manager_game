import pygame

class PlayerView:
    def __init__(self, screen, font, player_data):
        self.screen = screen
        self.font = font
        self.player = player_data

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self):
        # Draw title
        name = f"{self.player['first_name']} {self.player['last_name']}"
        title = self.font.render(name, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 30))
        self.screen.blit(title, title_rect)

        # Draw player stats
        stats = [
            ("Position", self.player['position']),
            ("Age", str(self.player['age'])),
            ("Attack", str(self.player['attacking'])),
            ("Defense", str(self.player['defending'])),
            ("Goalkeeping", str(self.player['goalkeeping'])),
            ("Stamina", str(self.player['stamina'])),
            ("Speed", str(self.player['speed'])),
            ("Morale", str(self.player['morale'])),
            ("Value", f"£{self.player['value']:,}"),
            ("Wages", f"£{self.player['wages']:,}/week"),
            ("Contract", f"{self.player['contract_years']} years")
        ]

        label_x = 400   # Moved from 50
        value_x = 500   # Moved from 250
        y = 100
        
        for label, value in stats:
            # Label (right-aligned)
            text = self.font.render(f"{label}:", True, (200, 200, 200))
            text_rect = text.get_rect(right=label_x, y=y)  # Right-align the label
            self.screen.blit(text, text_rect)
            
            # Value (left-aligned)
            text = self.font.render(value, True, (255, 255, 255))
            self.screen.blit(text, (value_x, y))
            y += 40

        # Draw navigation hint
        hint = self.font.render("ESC - Back", True, (255, 255, 255))
        hint_rect = hint.get_rect(bottomright=(self.screen.get_width() - 20, 
                                             self.screen.get_height() - 20))
        self.screen.blit(hint, hint_rect)
