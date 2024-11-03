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

            # Add sample teams for all divisions
            teams_data = [
                # Premier League (division_id: 1)
                ("Arsenal", 1, 90, 500000000),
                ("Aston Villa", 1, 85, 300000000),
                ("Brentford", 1, 79, 180000000),
                ("Bournemouth", 1, 78, 200000000),
                ("Brighton & Hove Albion", 1, 82, 250000000),
                ("Chelsea", 1, 88, 450000000),
                ("Crystal Palace", 1, 78, 200000000),
                ("Everton", 1, 80, 250000000),
                ("Fulham", 1, 77, 180000000),
                ("Ipswich Town", 1, 75, 150000000),
                ("Leicester City", 1, 82, 280000000),
                ("Liverpool", 1, 89, 475000000),
                ("Luton Town", 1, 74, 120000000),
                ("Manchester City", 1, 92, 600000000),
                ("Manchester United", 1, 88, 525000000),
                ("Newcastle United", 1, 86, 400000000),
                ("Nottingham Forest", 1, 77, 200000000),
                ("Sheffield United", 1, 75, 150000000),
                ("Tottenham Hotspur", 1, 85, 400000000),
                ("West Ham United", 1, 82, 300000000),
                ("Wolverhampton Wanderers", 1, 79, 250000000),

                # Championship (division_id: 2)
                ("Birmingham City", 2, 70, 50000000),
                ("Blackburn Rovers", 2, 71, 45000000),
                ("Blackpool", 2, 68, 35000000),
                ("Bristol City", 2, 69, 40000000),
                ("Cardiff City", 2, 70, 45000000),
                ("Coventry City", 2, 71, 48000000),
                ("Derby County", 2, 72, 50000000),
                ("Huddersfield Town", 2, 69, 40000000),
                ("Hull City", 2, 70, 45000000),
                ("Leeds United", 2, 75, 100000000),
                ("Middlesbrough", 2, 73, 60000000),
                ("Millwall", 2, 69, 40000000),
                ("Norwich City", 2, 74, 80000000),
                ("Plymouth Argyle", 2, 67, 30000000),
                ("Preston North End", 2, 69, 40000000),
                ("Queens Park Rangers", 2, 70, 45000000),
                ("Reading", 2, 70, 45000000),
                ("Rotherham United", 2, 67, 30000000),
                ("Stoke City", 2, 72, 55000000),
                ("Sunderland", 2, 73, 60000000),
                ("Swansea City", 2, 71, 50000000),
                ("Watford", 2, 73, 60000000),
                ("West Bromwich Albion", 2, 74, 70000000),
                ("Wigan Athletic", 2, 69, 40000000),

                # League One (division_id: 3)
                ("Accrington Stanley", 3, 60, 10000000),
                ("Barnsley", 3, 63, 15000000),
                ("Bolton Wanderers", 3, 64, 18000000),
                ("Bradford City", 3, 62, 12000000),
                ("Burton Albion", 3, 60, 8000000),
                ("Cambridge United", 3, 59, 7000000),
                ("Carlisle United", 3, 59, 7000000),
                ("Charlton Athletic", 3, 63, 15000000),
                ("Cheltenham Town", 3, 58, 6000000),
                ("Colchester United", 3, 59, 7000000),
                ("Crawley Town", 3, 58, 6000000),
                ("Crewe Alexandra", 3, 59, 7000000),
                ("Doncaster Rovers", 3, 61, 10000000),
                ("Exeter City", 3, 60, 8000000),
                ("Fleetwood Town", 3, 61, 10000000),
                ("Gillingham", 3, 60, 8000000),
                ("Leyton Orient", 3, 59, 7000000),
                ("Lincoln City", 3, 60, 8000000),
                ("Milton Keynes Dons", 3, 61, 10000000),
                ("Morecambe", 3, 58, 6000000),
                ("Oxford United", 3, 62, 12000000),
                ("Peterborough United", 3, 63, 15000000),
                ("Portsmouth", 3, 64, 18000000),
                ("Shrewsbury Town", 3, 60, 8000000),

                # League Two (division_id: 4)
                ("AFC Wimbledon", 4, 55, 4000000),
                ("Barrow", 4, 52, 2000000),
                ("Bromley", 4, 51, 1500000),
                ("Chesterfield", 4, 54, 3000000),
                ("Crawley Town", 4, 53, 2500000),
                ("Dagenham & Redbridge", 4, 51, 1500000),
                ("Grimsby Town", 4, 54, 3000000),
                ("Harrogate Town", 4, 51, 1500000),
                ("Hartlepool United", 4, 53, 2500000),
                ("Mansfield Town", 4, 54, 3000000),
                ("Newport County", 4, 53, 2500000),
                ("Northampton Town", 4, 54, 3000000),
                ("Notts County", 4, 55, 4000000),
                ("Oldham Athletic", 4, 54, 3000000),
                ("Port Vale", 4, 54, 3000000),
                ("Rochdale", 4, 53, 2500000),
                ("Salford City", 4, 54, 3000000),
                ("Scunthorpe United", 4, 52, 2000000),
                ("Southend United", 4, 53, 2500000),
                ("Stevenage", 4, 52, 2000000),
                ("Stockport County", 4, 54, 3000000),
                ("Sutton United", 4, 51, 1500000),
                ("Swindon Town", 4, 54, 3000000),
                ("Tranmere Rovers", 4, 54, 3000000)
            ]

            cursor.execute("DELETE FROM teams")  # Clear existing teams
            for team in teams_data:
                cursor.execute("""
                    INSERT INTO teams (name, division_id, reputation, finances)
                    VALUES (?, ?, ?, ?)
                """, team)

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