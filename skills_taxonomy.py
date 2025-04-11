import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fairlearn.metrics import demographic_parity_difference

class SkillsTaxonomy:
    def __init__(self):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Hierarchical skills taxonomy
        self.skills_hierarchy = {
            'Technical Skills': {
                'Programming Languages': ['Python', 'Java', 'JavaScript'],
                'Frameworks': ['Django', 'React', 'Spring'],
                'Cloud Technologies': ['AWS', 'Azure', 'GCP']
            },
            'Soft Skills': {
                'Communication': ['Verbal', 'Written', 'Presentation'],
                'Leadership': ['Team Management', 'Strategic Planning']
            }
        }
    
    def get_skill_embedding(self, skill):
        """Generate embedding for a skill"""
        return self.embedding_model.encode([skill])[0]
    
    def semantic_skill_match(self, candidate_skills, job_skills):
        """Perform semantic matching of skills"""
        candidate_embeddings = [self.get_skill_embedding(skill) for skill in candidate_skills]
        job_embeddings = [self.get_skill_embedding(skill) for skill in job_skills]
        
        similarity_matrix = cosine_similarity(candidate_embeddings, job_embeddings)
        return similarity_matrix
    
    def detect_bias(self, candidate_pool, selection_results):
        """Detect potential bias in candidate selection"""
        # Implement fairness metrics
        demographic_parity = demographic_parity_difference(
            y_true=selection_results['selected'],
            y_pred=selection_results['demographic_group']
        )
        return demographic_parity

    def rank_candidates(self, candidates, job_description):
        """Advanced candidate ranking"""
        ranked_candidates = []
        for candidate in candidates:
            skill_match_score = self.semantic_skill_match(
                candidate['skills'], 
                job_description['required_skills']
            )
            # Combine multiple scoring factors
            overall_score = np.mean(skill_match_score)
            ranked_candidates.append({
                'candidate': candidate,
                'match_score': overall_score
            })
        
        return sorted(ranked_candidates, key=lambda x: x['match_score'], reverse=True)

    def explain_match(self, candidate, job_description):
        """Generate explainable match results"""
        skill_matches = self.semantic_skill_match(
            candidate['skills'], 
            job_description['required_skills']
        )
        
        explanation = {
            'matched_skills': [],
            'missing_skills': [],
            'overall_match_percentage': np.mean(skill_matches) * 100
        }
        
        return explanation