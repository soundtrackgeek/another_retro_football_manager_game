# main.py
import pygame
import sys
import os
from views.menu_view import MenuView
from views.division_select_view import DivisionSelectView
from views.team_select_view import TeamSelectView
from views.game_menu_view import GameMenuView
from views.team_submenu_view import TeamSubmenuView  # Add this import
from views.team_view import TeamView  # Add this import
from views.player_view import PlayerView
from database.database import FootballDB  # Fix this import line

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Football Manager")
        
        # Load C64 font
        font_path = os.path.join('assets', 'fonts', 'C64_Pro-STYLE.ttf')
        self.font_size = 32
        self.font = pygame.font.Font(font_path, self.font_size)
        
        # Initialize menu
        self.menu = MenuView(self.screen, self.font)
        self.current_view = self.menu
        
        self.db = FootballDB()
        self.game_started = False
        print("Game initialized")  # Debug print
        
    def start_new_game(self):
        print("Starting new game - generating players...")
        try:
            self.db.clear_all_players()
            self.db.generate_all_teams_squads()
            self.game_started = True
            print("Player generation complete")
        except Exception as e:
            print(f"Error starting new game: {e}")

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
                            self.start_new_game()  # This will now definitely generate players
                            self.current_view = DivisionSelectView(self.screen, self.font)
                    
                    elif isinstance(self.current_view, DivisionSelectView):
                        if result is not None:  # Division ID was returned
                            self.current_view = TeamSelectView(self.screen, self.font, result)
                    
                    elif isinstance(self.current_view, TeamSelectView):
                        if result == -1:  # Back button pressed
                            self.current_view = DivisionSelectView(self.screen, self.font)
                        elif result is not None:  # Team was selected
                            self.current_view = GameMenuView(self.screen, self.font, result)
                    
                    elif isinstance(self.current_view, GameMenuView):
                        if result == "TEAM":
                            self.current_view = TeamSubmenuView(self.screen, self.font, self.current_view.team_id)
                        elif result == "EXIT_GAME":
                            self.current_view = self.menu
                        elif result is not None:
                            print(f"Selected menu option: {result}")
                    
                    elif isinstance(self.current_view, TeamSubmenuView):
                        if result == "BACK_TO_MAIN_MENU":
                            self.current_view = GameMenuView(self.screen, self.font, self.current_view.team_id)
                        elif result == "SELECT_PLAYERS":
                            # TODO: Create and show player selection view
                            print("Select players for next match")
                        elif result == "VIEW_TEAM":
                            self.current_view = TeamView(self.screen, self.font, self.current_view.team_id)
                    
                    elif isinstance(self.current_view, TeamView):
                        if result == "BACK":
                            self.current_view = TeamSubmenuView(self.screen, self.font, self.current_view.team_id)
                        elif isinstance(result, tuple) and result[0] == "SHOW_PLAYER":
                            self.current_view = PlayerView(self.screen, self.font, result[1])
                    
                    elif isinstance(self.current_view, PlayerView):
                        if result == "BACK":
                            # Go back to team view
                            self.current_view = TeamView(self.screen, self.font, self.current_view.player['team_id'])
            
            # Add check for game state - if not started, ensure players are generated
            if not self.game_started and not isinstance(self.current_view, MenuView):
                self.start_new_game()
            
            self.screen.fill((0, 0, 128))  # Navy blue background
            self.current_view.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__": 
    game = Game()
    game.run()