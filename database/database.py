# database/database.py
import sqlite3
import os
import logging
from typing import List, Dict, Any

class FootballDB:
    def __init__(self):
        self.db_path = os.path.join('database', 'football.db')
        self.conn = None
        self.setup_logging()
        self.initialize_database()

    def setup_logging(self):
        logging.basicConfig(
            filename=os.path.join('logs', 'database.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return self.conn
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            raise

    def initialize_database(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Create divisions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS divisions (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    level INTEGER NOT NULL
                )
            ''')

            # Create teams table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    division_id INTEGER,
                    reputation INTEGER,
                    finances INTEGER,
                    FOREIGN KEY (division_id) REFERENCES divisions(id)
                )
            ''')

            # Create players table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    team_id INTEGER,
                    age INTEGER,
                    position TEXT,
                    attacking INTEGER,
                    defending INTEGER,
                    goalkeeping INTEGER,
                    stamina INTEGER,
                    speed INTEGER,
                    value INTEGER,
                    wages INTEGER,
                    contract_years INTEGER,
                    FOREIGN KEY (team_id) REFERENCES teams(id)
                )
            ''')

            # Create league_tables table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS league_tables (
                    id INTEGER PRIMARY KEY,
                    team_id INTEGER,
                    division_id INTEGER,
                    played INTEGER DEFAULT 0,
                    won INTEGER DEFAULT 0,
                    drawn INTEGER DEFAULT 0,
                    lost INTEGER DEFAULT 0,
                    goals_for INTEGER DEFAULT 0,
                    goals_against INTEGER DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    season INTEGER,
                    FOREIGN KEY (team_id) REFERENCES teams(id),
                    FOREIGN KEY (division_id) REFERENCES divisions(id)
                )
            ''')

            # Initialize divisions
            divisions = [
                (1, "Premier League", 1),
                (2, "Championship", 2),
                (3, "League One", 3),
                (4, "League Two", 4)
            ]
            cursor.executemany("INSERT OR IGNORE INTO divisions VALUES (?,?,?)", divisions)

            # Sample method to add a team
            def add_team(name: str, division_id: int, reputation: int, finances: int):
                cursor.execute("""
                    INSERT OR IGNORE INTO teams (name, division_id, reputation, finances)
                    VALUES (?, ?, ?, ?)
                """, (name, division_id, reputation, finances))

            # Add sample Premier League teams
            premier_league_teams = [
                ("Arsenal", 1, 90, 500000000),
                ("Chelsea", 1, 88, 450000000),
                ("Liverpool", 1, 89, 475000000),
                ("Manchester City", 1, 92, 600000000),
                ("Manchester United", 1, 88, 525000000),
                # Add more teams as needed
            ]

            for team in premier_league_teams:
                add_team(*team)

    def get_teams_in_division(self, division_id: int) -> List[Dict[str, Any]]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM teams 
                WHERE division_id = ?
                ORDER BY name
            """, (division_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_player_details(self, player_id: int) -> Dict[str, Any]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
            result = cursor.fetchone()
            return dict(result) if result else None

    def get_team_players(self, team_id: int) -> List[Dict[str, Any]]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM players 
                WHERE team_id = ?
                ORDER BY position, last_name
            """, (team_id,))
            return [dict(row) for row in cursor.fetchall()]

    def update_league_table(self, team_id: int, division_id: int, 
                          played: int, won: int, drawn: int, lost: int,
                          goals_for: int, goals_against: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            points = won * 3 + drawn
            cursor.execute("""
                UPDATE league_tables 
                SET played=?, won=?, drawn=?, lost=?, 
                    goals_for=?, goals_against=?, points=?
                WHERE team_id=? AND division_id=?
            """, (played, won, drawn, lost, goals_for, goals_against, 
                 points, team_id, division_id))