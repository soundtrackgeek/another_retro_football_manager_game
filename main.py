# main.py
import pygame
import sys
import os
from views.menu_view import MenuView
from views.division_select_view import DivisionSelectView
from views.team_select_view import TeamSelectView

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
        self.current_view = self.menu
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    result = self.current_view.handle_input(event.key)
                    
                    if isinstance(self.current_view, MenuView):
                        if result == "START_GAME":
                            self.current_view = DivisionSelectView(self.screen, self.font)
                    
                    elif isinstance(self.current_view, DivisionSelectView):
                        if result is not None:  # Division ID was returned
                            self.current_view = TeamSelectView(self.screen, self.font, result)
                    
                    elif isinstance(self.current_view, TeamSelectView):
                        if result == -1:  # Back button pressed
                            self.current_view = DivisionSelectView(self.screen, self.font)
                        elif result is not None:  # Team was selected
                            # TODO: Start game with selected team
                            print(f"Selected team ID: {result}")
                            self.current_view = self.menu  # Temporarily go back to menu
            
            self.screen.fill((0, 0, 128))  # Navy blue background
            self.current_view.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__": 
    game = Game()
    game.run()