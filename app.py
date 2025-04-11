import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app_debug.log'),
        logging.StreamHandler()
    ]
)

def load_candidate_matches():
    """Load candidate matches from SQLite database"""
    match_db_path = r'C:\Users\megha\Downloads\hack\database\match.db'
    
    logging.info(f"Attempting to load database from: {match_db_path}")
    
    # Validate database file exists and is accessible
    try:
        if not os.path.exists(match_db_path):
            logging.error(f"Database file not found: {match_db_path}")
            raise FileNotFoundError(f"Database file not found: {match_db_path}")
        
        # Check file permissions and size
        file_stats = os.stat(match_db_path)
        logging.info(f"Database file size: {file_stats.st_size} bytes")
        
        if file_stats.st_size == 0:
            logging.error("Database file is empty")
            raise ValueError("Database file is empty")
        
        # Attempt to connect and validate database
        conn = sqlite3.connect(match_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        # Check table existence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='candidate_matches'")
        if not cursor.fetchone():
            logging.error("No 'candidate_matches' table found in the database")
            raise ValueError("No 'candidate_matches' table found in the database")
        
        # Fetch and validate data
        df = pd.read_sql_query("SELECT * FROM candidate_matches", conn)
        
        if df.empty:
            logging.warning("No candidate matches found in the database")
            raise ValueError("No candidate matches found in the database")
        
        logging.info(f"Successfully loaded {len(df)} candidate matches")
        conn.close()
        return df
    
    except sqlite3.Error as e:
        logging.error(f"SQLite database error: {e}")
        raise sqlite3.Error(f"SQLite error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error loading database: {e}")
        raise RuntimeError(f"Unexpected error loading database: {e}")

def display_candidate_details(candidate_name, cv_path):
    """Display detailed candidate information"""
    st.subheader(f"Candidate: {candidate_name}")
    
    # Display CV path
    st.write(f"**CV Path:** {cv_path}")
    
    # Option to view CV (if PDF)
    if os.path.exists(cv_path) and cv_path.lower().endswith('.pdf'):
        with open(cv_path, 'rb') as file:
            st.download_button(
                label="Download CV",
                data=file.read(),
                file_name=f"{candidate_name}_CV.pdf",
                mime="application/pdf"
            )

def main():
    st.set_page_config(
        page_title="Job Candidate Matching Dashboard",
        page_icon=":briefcase:",
        layout="wide"
    )
    
    st.title("🚀 Job Candidate Matching Dashboard")
    
    # Add debug information
    st.sidebar.header("Debug Information")
    st.sidebar.text(f"Database Path: {os.path.abspath(r'C:\Users\megha\Downloads\hack\database\match.db')}")
    
    try:
        candidates_df = load_candidate_matches()
        
        # Top row with key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Candidates Matched", len(candidates_df))
        
        with col2:
            st.metric("Highest Match Score", f"{candidates_df['match_score'].max():.2%}")
        
        with col3:
            st.metric("Average Match Score", f"{candidates_df['match_score'].mean():.2%}")
        
        # Candidate Match Scores Bar Chart
        st.subheader("Candidate Match Scores")
        fig = px.bar(
            candidates_df, 
            x='candidate_name', 
            y='match_score', 
            title='Match Scores by Candidate',
            labels={'match_score': 'Match Score', 'candidate_name': 'Candidate'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Candidate Table
        st.subheader("Candidate Details")
        candidates_df['match_score_percent'] = candidates_df['match_score'] * 100
        display_df = candidates_df[['candidate_name', 'match_score_percent', 'cv_path']]
        display_df.columns = ['Candidate', 'Match Score (%)', 'CV Path']
        st.dataframe(display_df, hide_index=True)
        
        # Candidate Selection
        selected_candidate = st.selectbox(
            "Select a Candidate for Detailed View", 
            candidates_df['candidate_name']
        )
        
        if selected_candidate:
            candidate_row = candidates_df[candidates_df['candidate_name'] == selected_candidate].iloc[0]
            display_candidate_details(candidate_row['candidate_name'], candidate_row['cv_path'])
    
    except Exception as e:
        st.error(f"Error: {e}")
        st.sidebar.error("Check app_debug.log for detailed error information")
        logging.exception("Dashboard initialization failed")

if __name__ == "__main__":
    main()