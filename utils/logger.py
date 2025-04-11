# c:/Users/megha/Downloads/hack/utils/logger.py
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any

class JobScreeningLogger:
    def __init__(self, log_dir: Optional[str] = None, log_level: int = logging.INFO):
        """
        Initialize a comprehensive logger for job screening system
        
        :param log_dir: Directory to store log files
        :param log_level: Logging level
        """
        # Create log directory if not exists
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('job_screening_system')
        self.logger.setLevel(log_level)
        
        # Create file handler
        log_file = os.path.join(self.log_dir, f'job_screening_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_job_description_processing(self, job_id: int, details: Dict[str, Any]):
        """Log job description processing details"""
        self.logger.info(f"Processing Job Description (ID: {job_id})")
        self.logger.debug(f"Job Details: {details}")
    
    def log_candidate_extraction(self, candidate_id: int, skills: list, experience: list):
        """Log candidate resume extraction details"""
        self.logger.info(f"Extracting Candidate Details (ID: {candidate_id})")
        self.logger.debug(f"Skills: {skills}")
        self.logger.debug(f"Experience: {experience}")
    
    def log_matching_result(self, job_id: int, candidate_id: int, match_score: float):
        """Log candidate-job matching result"""
        self.logger.info(
            f"Matching Result - Job {job_id}, Candidate {candidate_id}: {match_score * 100:.2f}%"
        )
    
    def log_error(self, component: str, error: Exception):
        """Log errors with detailed traceback"""
        self.logger.error(f"Error in {component}: {str(error)}", exc_info=True)
    
    def log_interview_scheduling(self, candidate_email: str, status: str):
        """Log interview scheduling details"""
        self.logger.info(f"Interview Scheduling - Candidate {candidate_email}: {status}")
        if status.lower() == 'failed':
            self.logger.warning(f"Interview scheduling failed for {candidate_email}")
        elif status.lower() == 'success':
            self.logger.info(f"Interview successfully scheduled for {candidate_email}")