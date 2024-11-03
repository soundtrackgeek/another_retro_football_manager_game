from typing import List, Dict

class LeagueTable:
    def __init__(self, db):
        self.db = db

    def get_league_table(self, division_id: int) -> List[Dict]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    t.name as club,
                    lt.played,
                    lt.won,
                    lt.drawn,
                    lt.lost,
                    lt.goals_for as gf,
                    lt.goals_against as ga,
                    (lt.goals_for - lt.goals_against) as gd,
                    lt.points as pts
                FROM league_tables lt
                JOIN teams t ON lt.team_id = t.id
                WHERE lt.division_id = ?
                ORDER BY lt.points DESC, 
                         (lt.goals_for - lt.goals_against) DESC, 
                         lt.goals_for DESC,
                         t.name ASC
            """, (division_id,))
            
            return [dict(row) for row in cursor.fetchall()]

    def initialize_league_table(self, division_id: int):
        """Initialize or reset league table for a division"""
        with self.db.connect() as conn:
            cursor = conn.cursor()
            # First, clear existing entries
            cursor.execute("DELETE FROM league_tables WHERE division_id = ?", (division_id,))
            
            # Get all teams in the division
            cursor.execute("SELECT id FROM teams WHERE division_id = ?", (division_id,))
            teams = cursor.fetchall()
            
            # Initialize each team's record
            for team in teams:
                cursor.execute("""
                    INSERT INTO league_tables 
                    (team_id, division_id, played, won, drawn, lost, 
                     goals_for, goals_against, points, season)
                    VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 1)
                """, (team[0], division_id))
