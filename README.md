# Project Overview
This project is designed to provide advanced candidate matching using a hierarchical skills taxonomy and semantic matching with embeddings. It includes features such as bias detection mechanisms, advanced candidate ranking, explainable matching results, and a feedback integration system.

## Key Features
1. **Hierarchical Skills Taxonomy**: Organizes skills into a hierarchical structure for better classification and matching.
2. **Semantic Matching using Embeddings**: Utilizes vector embeddings to perform semantic skill matching.
3. **Bias Detection Mechanisms**: Implements methods to detect and mitigate biases in the matching process.
4. **Advanced Candidate Ranking**: Provides sophisticated ranking algorithms to prioritize candidates.
5. **Explainable Matching Results**: Offers visualization and explanation modules for better understanding of matching results.
6. **Feedback Integration System**: Builds a feedback loop for continuous improvement of the system.

## Technical Approach
- **Vector Embeddings**: Used for semantic skill matching to improve accuracy.
- **Hierarchical Skill Classification**: Implements a structured approach to skill categorization.
- **Visualization and Explanation Modules**: Provides tools for understanding and interpreting the matching process.
- **Feedback Loop**: Integrates user feedback to enhance system performance over time.

## Setup Instructions
1. **Ensure virtual environment is activated**
   - Activate your virtual environment using the command: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).

2. **Install requirements**
   - Install the necessary packages using: `pip install -r requirements.txt`

3. **Run Streamlit app**
   - Start the app with the command: `streamlit run app.py`

4. **Access app via localhost**
   - Open your browser and go to `http://localhost:8501` to access the application.

## Requirements
Refer to `requirements.txt` for the list of dependencies needed for this project.

## Environment Variables
Ensure that all necessary environment variables are set as per the `.env` file.


