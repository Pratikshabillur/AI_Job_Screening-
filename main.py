import os
import sys
import logging
import pandas as pd
import sqlite3
from config import Config
from utils.database_manager import DatabaseManager
from utils.ollama_interface import OllamaInterface
from models.embedding_model import EmbeddingModel
from agents.job_description_agent import JobDescriptionAgent
from agents.recruiting_agent import RecruitingAgent
from agents.matching_agent import MatchingAgent
from agents.interview_scheduler import InterviewSchedulerAgent
from utils.logger import JobScreeningLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('job_screening.log')
    ]
)
logger = logging.getLogger(__name__)

def calculate_match_score(cv_text, job_description_text, embedding_model):
    """
    Calculate match score between CV and job description using embedding similarity
    
    :param cv_text: Text from the CV
    :param job_description_text: Text from the job description
    :param embedding_model: Embedding model for text comparison
    :return: Match score (0-1)
    """
    # Use the built-in calculate_similarity method
    similarity = embedding_model.calculate_similarity(cv_text, job_description_text)
    
    return similarity

def main():
    try:
        logger.info("Starting Job Screening Process")
        
        # Directories and paths
        cvs_directory = r'C:\Users\megha\Downloads\hack\database\CVs1'
        job_description_path = r'C:\Users\megha\Downloads\hack\database\job_description.csv'
        match_db_path = r'C:\Users\megha\Downloads\hack\database\match.db'
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(match_db_path), exist_ok=True)
        
        # Initialize embedding model
        logger.info("Initializing embedding model")
        embedding_model = EmbeddingModel()
        
        # Read job description with multiple encoding attempts
        encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
        job_description_df = None
        
        for encoding in encodings:
            try:
                job_description_df = pd.read_csv(job_description_path, encoding=encoding)
                logger.info(f"Successfully read job description with {encoding} encoding")
                break
            except UnicodeDecodeError:
                logger.warning(f"Failed to read job description with {encoding} encoding")
        
        if job_description_df is None or job_description_df.empty:
            logger.error("Could not read job description CSV with any encoding")
            return
        
        # Use the first row's job description (now using the correct column name)
        job_description_text = job_description_df.iloc[0]['Job Description']
        
        # Prepare results storage
        cv_match_scores = []
        
        # Process all CVs
        for resume_file in os.listdir(cvs_directory):
            try:
                # Skip non-text files
                if not resume_file.lower().endswith(('.txt', '.pdf', '.docx')):
                    continue
                
                resume_path = os.path.join(cvs_directory, resume_file)
                candidate_name = os.path.splitext(resume_file)[0]
                
                # Read CV content
                with open(resume_path, 'r', encoding='utf-8', errors='ignore') as f:
                    cv_text = f.read()
                
                # Calculate match score
                match_score = calculate_match_score(cv_text, job_description_text, embedding_model)
                
                cv_match_scores.append({
                    'candidate_name': candidate_name,
                    'match_score': match_score,
                    'cv_path': resume_path
                })
                
                logger.info(f"Processed {candidate_name} with match score: {match_score}")
            
            except Exception as e:
                logger.error(f"Error processing {resume_file}: {e}", exc_info=True)
        
        # Sort candidates by match score
        cv_match_scores.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Select top 3 candidates
        top_3_candidates = cv_match_scores[:3]
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(match_db_path), exist_ok=True)
        
        # Remove existing database if it exists to prevent corruption
        if os.path.exists(match_db_path):
            try:
                os.remove(match_db_path)
                logger.info(f"Removed existing database: {match_db_path}")
            except PermissionError:
                logger.error(f"Cannot remove database. It might be in use: {match_db_path}")
                raise
        
        # Create a new database connection with error handling
        try:
            conn = sqlite3.connect(match_db_path)
            cursor = conn.cursor()
            
            # Create table with strict schema
            cursor.execute('''
                CREATE TABLE candidate_matches (
                    candidate_name TEXT PRIMARY KEY,
                    match_score REAL NOT NULL CHECK(match_score >= 0 AND match_score <= 1),
                    cv_path TEXT NOT NULL
                )
            ''')
            
            # Insert candidates with type conversion and error handling
            for candidate in top_3_candidates:
                try:
                    cursor.execute('''
                        INSERT INTO candidate_matches 
                        (candidate_name, match_score, cv_path) 
                        VALUES (?, ?, ?)
                    ''', (
                        str(candidate['candidate_name']), 
                        float(candidate['match_score']), 
                        str(candidate['cv_path'])
                    ))
                except sqlite3.IntegrityError as e:
                    logger.error(f"Integrity error inserting candidate {candidate['candidate_name']}: {e}")
                except Exception as e:
                    logger.error(f"Error inserting candidate {candidate['candidate_name']}: {e}")
            
            # Commit and verify
            conn.commit()
            
            # Verify data insertion
            cursor.execute('SELECT COUNT(*) FROM candidate_matches')
            count = cursor.fetchone()[0]
            logger.info(f"Successfully inserted {count} candidates into the database")
        
        except sqlite3.Error as e:
            logger.error(f"SQLite database creation error: {e}")
            raise
        finally:
            if conn:
                conn.close()
        
        # Log results
        logger.info("Top 3 Matching Candidates:")
        for candidate in top_3_candidates:
            logger.info(f"Candidate: {candidate['candidate_name']}, Match Score: {candidate['match_score']}")
        
        logger.info(f"Results saved to {match_db_path}")
    
    except Exception as e:
        logger.error(f"An error occurred during job screening: {e}", exc_info=True)

if __name__ == "__main__":
    main()