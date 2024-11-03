import pygame
from controllers.league_table import LeagueTable

class LeagueTableView:
    def __init__(self, screen, font, division_id, db):
        self.screen = screen
        self.font = font
        self.division_id = division_id
        self.league_table = LeagueTable(db)
        # Get any team from this division to store team_id
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM teams WHERE division_id = ? LIMIT 1", (division_id,))
            result = cursor.fetchone()
            self.team_id = result[0] if result else None
        # Header for the table columns
        self.headers = ["Pos", "Club", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]
        self.column_widths = [50, 300, 40, 40, 40, 40, 50, 50, 50, 50]  # Widths for each column

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self):
        # Get table data
        table_data = self.league_table.get_league_table(self.division_id)
        
        # Draw title
        title = self.font.render("LEAGUE TABLE", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        # Draw headers
        y = 100
        x = 50
        for header, width in zip(self.headers, self.column_widths):
            text = self.font.render(header, True, (255, 255, 0))
            self.screen.blit(text, (x, y))
            x += width

        # Draw table data
        y = 140
        for pos, row in enumerate(table_data, 1):
            x = 50
            # Position number
            pos_text = self.font.render(str(pos), True, (255, 255, 255))
            self.screen.blit(pos_text, (x, y))
            x += self.column_widths[0]
            
            # Club name
            club_text = self.font.render(row['club'], True, (255, 255, 255))
            self.screen.blit(club_text, (x, y))
            x += self.column_widths[1]
            
            # Stats
            for stat, width in zip(['played', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts'], 
                                 self.column_widths[2:]):
                stat_text = self.font.render(str(row[stat]), True, (255, 255, 255))
                self.screen.blit(stat_text, (x, y))
                x += width
            
            y += 30

        # Draw footer with instructions
        footer = self.font.render("Press ESC to return", True, (255, 255, 255))
        footer_rect = footer.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(footer, footer_rect)
