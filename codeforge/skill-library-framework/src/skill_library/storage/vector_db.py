import os
import logging
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class VectorDB:
    """
    Vector database for skill similarity matching using FAISS for efficient similarity search
    and TF-IDF for text vectorization.
    """
    
    def __init__(self, skill_repo: Any, embedding_dim: int = 300):
        """
        Initialize the VectorDB with FAISS index and TF-IDF vectorizer.
        
        Args:
            skill_repo: Repository for skill data access
            embedding_dim: Dimension of the skill embeddings
        """
        self.skill_repo = skill_repo
        self.embedding_dim = embedding_dim
        self.vectorizer = TfidfVectorizer(max_features=embedding_dim, stop_words='english')
        self.index = faiss.IndexFlatIP(embedding_dim)  # Inner product index for cosine similarity
        self.skill_ids: List[str] = []  # Track skill IDs corresponding to index positions
        self.skill_texts: List[str] = []  # Store skill text representations
        
        # Initialize with existing skills if any
        self._initialize_index()
        
    def _initialize_index(self) -> None:
        """Initialize the FAISS index with existing skills from repository."""
        try:
            skills = self.skill_repo.get_all_skills()
            if skills:
                self._build_index(skills)
            logger.info("VectorDB index initialized with %d skills", len(skills))
        except Exception as e:
            logger.error("Failed to initialize VectorDB index: %s", str(e))
            raise
    
    def _build_index(self, skills: List[Any]) -> None:
        """
        Build the FAISS index from skills.
        
        Args:
            skills: List of skill objects to index
        """
        if not skills:
            return
            
        # Prepare skill text representations for vectorization
        self.skill_texts = []
        self.skill_ids = []
        
        for skill in skills:
            # Combine skill name and description for text representation
            text = f"{skill.name} {skill.description}" if skill.description else skill.name
            self.skill_texts.append(text)
            self.skill_ids.append(str(skill.id))
            
        # Fit and transform the skill texts to vectors
        if self.skill_texts:
            try:
                vectors = self.vectorizer.fit_transform(self.skill_texts).toarray().astype('float32')
                # Normalize for cosine similarity
                faiss.normalize_L2(vectors)
                # Replace index with new data
                self.index = faiss.IndexFlatIP(self.embedding_dim)
                self.index.add(vectors)
                logger.info("FAISS index built with %d skills", len(skills))
            except Exception as e:
                logger.error("Error building FAISS index: %s", str(e))
                raise
    
    def add_skill(self, skill: Any) -> None:
        """
        Add a new skill to the vector database.
        
        Args:
            skill: Skill object to add to the database
        """
        try:
            # Create text representation of the skill
            text = f"{skill.name} {skill.description}" if skill.description else skill.name
            
            # Transform text to vector
            vector = self.vectorizer.transform([text]).toarray().astype('float32')
            faiss.normalize_L2(vector)
            
            # Add to index and tracking lists
            self.index.add(vector)
            self.skill_ids.append(str(skill.id))
            self.skill_texts.append(text)
            
            logger.info("Added skill %s to vector database", skill.id)
        except Exception as e:
            logger.error("Failed to add skill to vector database: %s", str(e))
            raise
    
    def find_similar_skills(self, skill_id: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Find k most similar skills to the given skill.
        
        Args:
            skill_id: ID of the skill to find similarities for
            k: Number of similar skills to return
            
        Returns:
            List of tuples (skill_id, similarity_score) sorted by similarity
        """
        try:
            # Get the query skill's text representation
            if skill_id not in self.skill_ids:
                logger.warning("Skill ID %s not found in vector database", skill_id)
                return []
                
            # Find index of query skill
            try:
                idx = self.skill_ids.index(skill_id)
            except ValueError:
                logger.warning("Index not found for skill ID %s", skill_id)
                return []
                
            # Get the query vector
            query_vector = self._get_vector_at_index(idx)
            if query_vector is None:
                return []
                
            # Perform similarity search
            similarities, indices = self.index.search(query_vector, min(k + 1, self.index.ntotal))  # +1 to exclude self
            
            # Process results
            results = []
            for i in range(len(indices[0])):
                # Skip the query skill itself (highest similarity will be to itself)
                if indices[0][i] == idx:
                    continue
                if indices[0][i] < len(self.skill_ids):
                    if indices[0][i] >= 0:  # Check for valid index
                        similar_skill_id = self.skill_ids[indices[0][i]]
                        similarity_score = float(similarities[0][i])
                        results.append((similar_skill_id, similarity_score))
                    
            # Return top k results (excluding self)
            return results[:k] if results else []
            
        except Exception as e:
            logger.error("Error finding similar skills: %s", str(e))
            return []
    
    def _get_vector_at_index(self, idx: int) -> Optional[np.ndarray]:
        """
        Get the vector at a specific index in the skill_texts list.
        
        Args:
            idx: Index of the vector to retrieve
            
        Returns:
            Vector at the specified index or None if error
        """
        try:
            if idx < len(self.skill_texts):
                text = self.skill_texts[idx]
                vector = self.vectorizer.transform([text]).toarray().astype('float32')
                faiss.normalize_L2(vector)
                return vector
            return None
        except Exception as e:
            logger.error("Error getting vector at index %d: %s", idx, str(e))
            return None
    
    def update_skill(self, skill: Any) -> None:
        """
        Update an existing skill in the vector database.
        
        Args:
            skill: Updated Skill object
        """
        try:
            # Remove old skill if it exists
            if str(skill.id) in self.skill_ids:
                # Note: FAISS doesn't support direct removal, so we rebuild
                # In practice, this would require reindexing all skills
                skills = self.skill_repo.get_all_skills()
                self._build_index(skills)
                logger.info("Updated skill %s in vector database", skill.id)
            else:
                self.add_skill(skill)
        except Exception as e:
            logger.error("Failed to update skill in vector database: %s", str(e))
            raise

    def remove_skill(self, skill_id: str) -> None:
        """
        Remove a skill from the vector database.
        
        Args:
            skill_id: ID of the skill to remove
        """
        try:
            if skill_id in self.skill_ids:
                # Rebuild index without the removed skill
                skills = self.skill_repo.get_all_skills()
                # Filter out the removed skill
                filtered_skills = [s for s in skills if str(s.id) != skill_id]
                self._build_index(filtered_skills)
                logger.info("Removed skill %s from vector database", skill_id)
        except Exception as e:
            logger.error("Failed to remove skill from vector database: %s", str(e))
            raise