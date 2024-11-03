import pygame

class TeamSubmenuView:
    def __init__(self, screen, font, team_id):
        self.screen = screen
        self.font = font
        self.team_id = team_id
        self.selected_index = 0
        self.menu_items = [
            "View Team",
            "Select Players",
            "Back to Main Menu"
        ]

    def handle_input(self, key):
        if key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif key == pygame.K_RETURN:
            selected = self.menu_items[self.selected_index].upper().replace(" ", "_")
            if selected == "SELECT_PLAYERS":
                return "SHOW_PLAYER_SELECTION"
            return selected
        return None

    def draw(self):
        # Draw title
        center_x = self.screen.get_width() // 2
        title = self.font.render("TEAM MENU", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 50))
        self.screen.blit(title, title_rect)

        # Draw menu items
        start_y = 150
        spacing = 40
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(center_x, start_y + i * spacing))
            self.screen.blit(text, text_rect)
