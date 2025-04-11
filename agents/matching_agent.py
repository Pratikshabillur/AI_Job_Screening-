from models.embedding_model import EmbeddingModel
from utils.database_manager import DatabaseManager
from config import Config

class MatchingAgent:
    def __init__(self, embedding_model: EmbeddingModel, db_manager: DatabaseManager):
        """
        Initialize Matching Agent
        
        :param embedding_model: Embedding model for similarity calculation
        :param db_manager: Database manager for storing match results
        """
        self.embedding_model = embedding_model
        self.db = db_manager
        self.match_threshold = Config.MATCH_THRESHOLD

    def calculate_candidate_match(self, job_id: int, candidate_id: int) -> float:
        """
        Calculate match score between a job and a candidate
        
        :param job_id: ID of the job description
        :param candidate_id: ID of the candidate
        :return: Match score
        """
        # Retrieve job description and candidate details
        job_query = "SELECT * FROM job_descriptions WHERE id = ?"
        candidate_query = "SELECT * FROM candidates WHERE id = ?"
        
        job = self.db.cursor.execute(job_query, (job_id,)).fetchone()
        candidate = self.db.cursor.execute(candidate_query, (candidate_id,)).fetchone()
        
        if not job or not candidate:
            return 0.0
        
        # Compare job requirements with candidate profile
        job_text = f"{job[1]} {job[3]} {job[4]}"  # Title, summary, skills
        candidate_text = f"{candidate[1]} {candidate[4]} {candidate[5]}"  # Name, skills, experience
        
        # Calculate similarity
        match_score = self.embedding_model.calculate_similarity(job_text, candidate_text)
        
        # Store match result
        self.db.insert_job_match(job_id, candidate_id, match_score)
        
        return match_score

    def shortlist_candidates(self, job_id: int) -> list:
        """
        Shortlist candidates for a specific job
        
        :param job_id: ID of the job description
        :return: List of shortlisted candidates
        """
        # Retrieve candidates
        candidate_query = "SELECT id FROM candidates"
        candidates = self.db.cursor.execute(candidate_query).fetchall()
        
        # Calculate matches
        matches = []
        for (candidate_id,) in candidates:
            match_score = self.calculate_candidate_match(job_id, candidate_id)
            if match_score >= self.match_threshold:
                matches.append({
                    'candidate_id': candidate_id,
                    'match_score': match_score
                })
        
        # Sort matches by score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches