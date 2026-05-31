import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfRanker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def rank_resumes(self, job_description: str, resume_texts: list) -> list:
        if not resume_texts:
            return []
            
        # Fit vectorizer on job description and all resumes
        documents = [job_description] + resume_texts
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        
        # Cosine similarity between JD (index 0) and resumes (indices 1 to N)
        jd_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(resume_vectors, jd_vector).flatten()
        return similarities.tolist()
