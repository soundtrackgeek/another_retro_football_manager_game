# main.py
import pygame
import sys
import os
from views.menu_view import MenuView

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Football Manager")
        
        # Load C64 font
        font_path = os.path.join('assets', 'fonts', 'C64_Pro-STYLE.ttf')
        self.font_size = 32
        self.font = pygame.font.Font(font_path, self.font_size)
        
        # Initialize menu
        self.menu = MenuView(self.screen, self.font)
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.menu.handle_input(event.key)
            
            # Draw
            self.screen.fill((0, 0, 128))  # Navy blue background
            self.menu.draw()
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__": 
    game = Game()
    game.run()