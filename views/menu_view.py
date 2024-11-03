# views/menu_view.py
import pygame
import sys  # Add this import

class MenuView:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Start Game", "Load Game", "Settings", "Quit Game"]
        self.selected_option = 0
        
    def handle_input(self, key):
        if key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key == pygame.K_RETURN:
            self.select_option()
    
    def select_option(self):
        if self.options[self.selected_option] == "Quit Game":
            pygame.quit()
            sys.exit()
        # Other options will be implemented later
    
    def draw(self):
        # Calculate center position
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        spacing = 50
        
        # Draw title
        title = self.font.render("FOOTBALL MANAGER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, center_y - 150))
        self.screen.blit(title, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(center_x, center_y - 50 + i * spacing))
            self.screen.blit(text, text_rect)