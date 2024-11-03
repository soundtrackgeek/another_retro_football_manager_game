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
from views.player_selection_view import PlayerSelectionView
from views.league_table_view import LeagueTableView
from controllers.league_table import LeagueTable  # Add this import

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Football Manager")
        
        # Load C64 font
        font_path = os.path.join('assets', 'fonts', 'C64_Pro-STYLE.ttf')
        self.font_size = 24
        self.font = pygame.font.Font(font_path, self.font_size)
        
        # Initialize menu
        self.menu = MenuView(self.screen, self.font)
        self.current_view = self.menu
        
        self.db = FootballDB()
        self.game_started = False
        print("Game initialized")  # Debug print
        
    def start_new_game(self):
        if self.game_started:  # Add this check to prevent recursion
            return
            
        print("Starting new game - generating players...")
        try:
            self.db.clear_all_players()
            self.db.generate_all_teams_squads()
            # Initialize league tables for all divisions
            for division_id in range(1, 5):
                league_table = LeagueTable(self.db)
                league_table.initialize_league_table(division_id)
            self.game_started = True
            print("Game initialization complete")
        except Exception as e:
            print(f"Error starting new game: {e}")
            self.game_started = False  # Reset if there was an error

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
                        elif result == "VIEW_TABLE":
                            team = self.db.get_team_details(self.current_view.team_id)
                            self.current_view = LeagueTableView(self.screen, self.font, team['division_id'], self.db)
                        elif result == "EXIT_GAME":
                            self.current_view = self.menu
                        elif result == "SHOW_PLAYER_SELECTION":
                            self.current_view = PlayerSelectionView(self.screen, self.font, self.current_view.team_id)
                        elif result == "VIEW_TEAM":
                            self.current_view = TeamView(self.screen, self.font, self.current_view.team_id)
                        elif result is not None:
                            print(f"Selected menu option: {result}")
                    
                    elif isinstance(self.current_view, LeagueTableView):
                        if result == "BACK":
                            team_id = self.current_view.team_id  # Store team_id before switching view
                            self.current_view = GameMenuView(self.screen, self.font, team_id)

                    elif isinstance(self.current_view, TeamSubmenuView):
                        if result == "BACK":
                            self.current_view = GameMenuView(self.screen, self.font, self.current_view.team_id)
                        elif result == "SHOW_PLAYER_SELECTION":
                            self.current_view = PlayerSelectionView(self.screen, self.font, self.current_view.team_id)
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
                    
                    elif isinstance(self.current_view, PlayerSelectionView):
                        if result == "BACK":
                            self.current_view = TeamSubmenuView(self.screen, self.font, self.current_view.team_id)
                        elif result == "SELECTION_COMPLETE":
                            # TODO: Save the selected team
                            self.current_view = TeamView(self.screen, self.font, self.current_view.team_id)
            
            self.screen.fill((0, 0, 128))  # Navy blue background
            self.current_view.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
            

if __name__ == "__main__": 
    game = Game()
    game.run()