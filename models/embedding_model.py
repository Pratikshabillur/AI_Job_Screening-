from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingModel:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize embedding model
        
        :param model_name: Name of the embedding model
        """
        self.model = SentenceTransformer(model_name)

    def encode_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for input text
        
        :param text: Input text
        :return: Embedding vector
        """
        return self.model.encode(text)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        
        :param text1: First text
        :param text2: Second text
        :return: Similarity score
        """
        embedding1 = self.encode_text(text1)
        embedding2 = self.encode_text(text2)
        
        return float(cosine_similarity([embedding1], [embedding2])[0][0])