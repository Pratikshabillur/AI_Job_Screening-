import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.database_manager import DatabaseManager
from config import Config

class InterviewSchedulerAgent:
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize Interview Scheduler Agent
        
        :param db_manager: Database manager for retrieving candidate details
        """
        self.db = db_manager

    def send_interview_invite(self, job_id: int, email_config: dict):
        """
        Send interview invites to shortlisted candidates
        
        :param job_id: ID of the job description
        :param email_config: Email configuration dictionary
        """
        # Get shortlisted candidates
        shortlisted = self.db.get_shortlisted_candidates(job_id)
        
        for candidate in shortlisted:
            # Prepare email
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = candidate['email']
            msg['Subject'] = f"Interview Invitation - {candidate['match_scores']}"
            
            # Email body
            body = f"""
            Dear {candidate['name']},

            Congratulations! Based on your impressive profile, we would like to invite you for an interview.

            Match Score: {candidate['match_scores']}
            
            Please confirm your availability for the interview.

            Best regards,
            Recruitment Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            try:
                with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                    server.starttls()
                    server.login(email_config['sender_email'], email_config['sender_password'])
                    server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email to {candidate['email']}: {e}")