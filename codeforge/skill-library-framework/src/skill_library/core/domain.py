import logging
from typing import Dict, List, Optional, Tuple
from src.skill_library.core.skill import Skill
from src.skill_library.core.complexity import Complexity
from src.skill_library.core.utility import Utility
from src.skill_library.models.predictive_scoring import PredictiveScoringModel
from src.skill_library.models.task_scoring_model import TaskScoringModel
from src.skill_library.storage.vector_db import VectorDB
from src.skill_library.storage.skill_repository import SkillRepository

logger = logging.getLogger(__name__)

class Domain:
    """Domain categorization system for organizing and classifying skills."""
    
    def __init__(
        self,
        domain_name: str,
        categories: Optional[Dict[str, List[str]]] = None,
        skill_repository: Optional[SkillRepository] = None,
        vector_db: Optional[VectorDB] = None,
        predictive_model: Optional[PredictiveScoringModel] = None,
        task_model: Optional[TaskScoringModel] = None
    ):
        """
        Initialize a Domain instance.
        
        Args:
            domain_name: Name of the domain
            categories: Optional dictionary mapping category names to skill lists
            skill_repository: Repository for skill persistence
            vector_db: Vector database for similarity searches
            predictive_model: Model for predictive scoring
            task_model: Model for task scoring
        """
        self.domain_name = domain_name
        self.categories = categories or {}
        self.skill_repository = skill_repository
        self.vector_db = vector_db
        self.predictive_model = predictive_model
        self.task_model = task_model
        self._validate_inputs()
    
    def _validate_inputs(self) -> None:
        """Validate initialization inputs."""
        if not isinstance(self.domain_name, str) or not self.domain_name.strip():
            raise ValueError("Domain name must be a non-empty string")
        
        if not isinstance(self.categories, dict):
            raise TypeError("Categories must be a dictionary")
    
    def get_category(self, skill: Skill) -> Optional[str]:
        """
        Determine the category for a given skill.
        
        Args:
            skill: Skill instance to categorize
            
        Returns:
            Category name if found, None otherwise
        """
        if not isinstance(skill, Skill):
            raise TypeError("Input must be a Skill instance")
        
        # Try to find exact category match first
        category = self._find_exact_category_match(skill)
        if category:
            return category
            
        # If no exact match, use predictive model if available
        if self.predictive_model and self.vector_db:
            category = self._predict_category(skill)
            if category:
                return category
        
        # Fallback to default categorization
        return self._fallback_categorization(skill)
    
    def _find_exact_category_match(self, skill: Skill) -> Optional[str]:
        """
        Find exact category match based on skill attributes.
        
        Args:
            skill: Skill to categorize
            
        Returns:
            Category name if match found, None otherwise
        """
        # Check skill name against category keywords
        skill_text = f"{skill.name} {skill.description}".lower()
        
        for category, keywords in self.categories.items():
            if any(keyword.lower() in skill_text for keyword in keywords):
                return category
        
        return None
    
    def _predict_category(self, skill: Skill) -> Optional[str]:
        """
        Use predictive model to determine skill category.
        
        Args:
            skill: Skill to categorize
            
        Returns:
            Predicted category or None
        """
        try:
            # Get similar skills from vector database
            if self.vector_db:
                similar_skills = self.vector_db.find_similar_skills(
                    skill.name, 
                    skill.description, 
                    top_k=5
                )
                
                if similar_skills:
                    # Use most common category among similar skills
                    category_counts = {}
                    for similar_skill, _ in similar_skills:
                        category = self._find_exact_category_match(similar_skill)
                        if category:
                            category_counts[category] = category_counts.get(category, 0) + 1
                    
                    if category_counts:
                        return max(category_counts, key=category_counts.get)
        except Exception as e:
            logger.warning(f"Category prediction failed: {e}")
        
        return None
    
    def _fallback_categorization(self, skill: Skill) -> str:
        """
        Fallback categorization when no other method works.
        
        Args:
            skill: Skill to categorize
            
        Returns:
            Default category name
        """
        return "uncategorized"
    
    def add_category(self, category_name: str, keywords: List[str]) -> None:
        """
        Add a new category with associated keywords.
        
        Args:
            category_name: Name of the category
            keywords: List of keywords associated with the category
        """
        if not isinstance(category_name, str) or not category_name.strip():
            raise ValueError("Category name must be a non-empty string")
        
        if not isinstance(keywords, list):
            raise TypeError("Keywords must be a list of strings")
        
        for keyword in keywords:
            if not isinstance(keyword, str):
                raise TypeError("All keywords must be strings")
        
        self.categories[category_name] = keywords
        logger.info(f"Added category '{category_name}' with {len(keywords)} keywords")
    
    def remove_category(self, category_name: str) -> bool:
        """
        Remove a category from the domain.
        
        Args:
            category_name: Name of category to remove
            
        Returns:
            True if removed, False if not found
        """
        if not isinstance(category_name, str) or not category_name.strip():
            raise ValueError("Category name must be a non-empty string")
        
        if category_name in self.categories:
            del self.categories[category_name]
            logger.info(f"Removed category '{category_name}'")
            return True
        
        return False
    
    def list_categories(self) -> List[str]:
        """
        List all categories in this domain.
        
        Returns:
            List of category names
        """
        return list(self.categories.keys())
    
    def get_category_keywords(self, category_name: str) -> List[str]:
        """
        Get keywords associated with a category.
        
        Args:
            category_name: Name of the category
            
        Returns:
            List of keywords for the category
        """
        if not isinstance(category_name, str) or not category_name.strip():
            raise ValueError("Category name must be a non-empty string")
        
        return self.categories.get(category_name, [])
    
    def update_category_keywords(self, category_name: str, keywords: List[str]) -> None:
        """
        Update keywords for an existing category.
        
        Args:
            category_name: Name of the category to update
            keywords: New list of keywords
        """
        if not isinstance(category_name, str) or not category_name.strip():
            raise ValueError("Category name must be a non-empty string")
        
        if category_name not in self.categories:
            raise KeyError(f"Category '{category_name}' not found")
        
        if not isinstance(keywords, list):
            raise TypeError("Keywords must be a list")
        
        self.categories[category_name] = keywords
        logger.info(f"Updated keywords for category '{category_name}'")