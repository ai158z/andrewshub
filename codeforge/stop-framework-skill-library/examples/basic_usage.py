import logging
from typing import Dict, Any
from stop_skill_library.models import Skill, PerformanceMetrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_skill() -> Dict[str, Any]:
    """Create a sample skill for demonstration"""
    return {
        "id": "sample-skill-001",
        "name": "Data Processing",
        "description": "Process and analyze large datasets efficiently",
        "version": "1.0.0",
        "code": "def process_data(data): return data",
        "metadata": {
            "category": "data_science",
            "complexity": "intermediate",
            "last_updated": "2024-01-01"
        }
    }

def demonstrate_skill_lifecycle(library) -> None:
    """Demonstrate the complete skill lifecycle"""
    logger.info("Starting skill lifecycle demonstration")
    
    # Create a sample skill
    skill_data = create_sample_skill()
    skill = Skill(**skill_data)
    
    # Add skill to library
    logger.info("Adding skill to library...")
    library.add_skill(skill)
    
    # Retrieve and display skill
    retrieved_skill = library.get_skill(skill.id)
    logger.info(f"Retrieved skill: {retrieved_skill.name}")
    
    # List all skills
    skills = library.list_skills()
    logger.info(f"Total skills in library: {len(skills)}")
    
    # Improve the skill
    logger.info("Improving skill...")
    improved_skill = library.improve_skill(skill.id, {
        "improvement": "Optimized data processing algorithm"
    })
    
    # Reflect on performance
    logger.info("Generating performance reflection...")
    metrics = PerformanceMetrics(accuracy=0.95, latency=0.02, throughput=1000)
    reflection = library.reflect("sample-skill-001", metrics)
    logger.info(f"Performance reflection: {reflection}")

def main() -> None:
    """Main demonstration function"""
    try:
        # Initialize the skill library
        logger.info("Initializing SkillLibrary...")
        from stop_skill_library import SkillLibrary
        library = SkillLibrary()
        
        # Run the demonstration
        demonstrate_skill_lifecycle(library)
        
        logger.info("Basic usage demonstration completed successfully")
        
    except Exception as e:
        logger.error(f"Error in basic usage demonstration: {str(e)}")
        raise

if __name__ == "__main__":
    main()