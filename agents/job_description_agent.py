from utils.ollama_interface import OllamaInterface
from utils.database_manager import DatabaseManager
from config import Config

class JobDescriptionAgent:
    def __init__(self, ollama_interface: OllamaInterface, db_manager: DatabaseManager):
        """
        Initialize Job Description Agent
        
        :param ollama_interface: Ollama interface for text generation
        :param db_manager: Database manager for storing job descriptions
        """
        self.ollama = ollama_interface
        self.db = db_manager

    def process_job_description(self, raw_job_description: str) -> int:
        """
        Process and store job description
        
        :param raw_job_description: Full text of job description
        :return: Job description ID
        """
        # Summarize job description
        summary = self.ollama.summarize_job_description(raw_job_description)
        
        # Prepare job data for storage
        job_data = {
            'title': summary.get('title', ''),
            'company': summary.get('company', ''),
            'summary': summary.get('summary', ''),
            'required_skills': summary.get('required_skills', []),
            'experience_level': summary.get('experience_level', ''),
            'raw_jd': raw_job_description
        }
        
        # Store in database
        return self.db.insert_job_description(job_data)