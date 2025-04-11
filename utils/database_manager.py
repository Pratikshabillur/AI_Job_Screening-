import os
import sqlite3
import json
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str):
        """
        Initialize database connection
        
        :param db_path: Path to SQLite database
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to the database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Job Descriptions Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                summary TEXT,
                required_skills TEXT,
                experience_level TEXT,
                raw_jd TEXT
            )
        ''')

        # Candidates Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                resume_path TEXT,
                skills TEXT,
                experience TEXT,
                education TEXT,
                match_scores TEXT
            )
        ''')

        # Matching Results Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                candidate_id INTEGER,
                match_score REAL,
                status TEXT,
                FOREIGN KEY(job_id) REFERENCES job_descriptions(id),
                FOREIGN KEY(candidate_id) REFERENCES candidates(id)
            )
        ''')

        self.conn.commit()

    def insert_job_description(self, job_data: Dict[str, Any]) -> int:
        """
        Insert a new job description
        
        :param job_data: Dictionary containing job description details
        :return: ID of inserted job description
        """
        query = '''
            INSERT INTO job_descriptions 
            (title, company, summary, required_skills, experience_level, raw_jd) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        values = (
            job_data.get('title', ''),
            job_data.get('company', ''),
            job_data.get('summary', ''),
            json.dumps(job_data.get('required_skills', [])),
            job_data.get('experience_level', ''),
            job_data.get('raw_jd', '')
        )
        
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def store_candidate(self, candidate_data: Dict[str, Any]) -> int:
        """
        Store candidate information in the database
        
        :param candidate_data: Dictionary containing candidate information
        :return: Candidate ID
        """
        try:
            # Convert experiences and education to JSON strings
            experiences_json = json.dumps(candidate_data.get('experiences', []))
            education_json = json.dumps(candidate_data.get('education', []))
            
            # Extract skills from experiences if not provided
            skills = candidate_data.get('skills', [])
            if not skills:
                skills = [exp.get('role', '') for exp in candidate_data.get('experiences', [])]
            skills_json = json.dumps(skills)
            
            # Insert or update candidate
            self.cursor.execute('''
                INSERT INTO candidates 
                (name, email, resume_text, experiences, education, skills) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                candidate_data.get('name', ''), 
                candidate_data.get('email', ''), 
                candidate_data.get('resume_text', ''),
                experiences_json,
                education_json,
                skills_json
            ))
            
            # Commit and get the last inserted ID
            self.conn.commit()
            return self.cursor.lastrowid
        
        except Exception as e:
            # Rollback in case of error
            self.conn.rollback()
            raise

    def insert_candidate(self, candidate_data: Dict[str, Any]) -> int:
        """
        Insert a new candidate
        
        :param candidate_data: Dictionary containing candidate details
        :return: ID of inserted candidate
        """
        query = '''
            INSERT INTO candidates 
            (name, email, resume_path, skills, experience, education, match_scores) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        values = (
            candidate_data.get('name', ''),
            candidate_data.get('email', ''),
            candidate_data.get('resume_path', ''),
            json.dumps(candidate_data.get('skills', [])),
            json.dumps(candidate_data.get('experience', [])),
            json.dumps(candidate_data.get('education', [])),
            json.dumps(candidate_data.get('match_scores', {}))
        )
        
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_job_match(self, job_id: int, candidate_id: int, match_score: float, status: str = 'pending'):
        """
        Record job match for a candidate
        
        :param job_id: ID of the job description
        :param candidate_id: ID of the candidate
        :param match_score: Matching score
        :param status: Current status of the match
        """
        query = '''
            INSERT INTO job_matches 
            (job_id, candidate_id, match_score, status) 
            VALUES (?, ?, ?, ?)
        '''
        
        self.cursor.execute(query, (job_id, candidate_id, match_score, status))
        self.conn.commit()

    def get_shortlisted_candidates(self, job_id: int, threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Retrieve shortlisted candidates for a job
        
        :param job_id: ID of the job description
        :param threshold: Minimum match score
        :return: List of shortlisted candidates
        """
        query = '''
            SELECT c.*, jm.match_score 
            FROM candidates c
            JOIN job_matches jm ON c.id = jm.candidate_id
            WHERE jm.job_id = ? AND jm.match_score >= ?
            ORDER BY jm.match_score DESC
        '''
        
        self.cursor.execute(query, (job_id, threshold))
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

def get_all_candidates(self) -> List[Dict[str, Any]]:
    """
    Fetch all records from the candidates table.
    :return: List of all candidates
    """
    query = "SELECT * FROM candidates"
    self.cursor.execute(query)
    columns = [column[0] for column in self.cursor.description]
    return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def close(self):
        """Close database connection"""
        self.conn.close()