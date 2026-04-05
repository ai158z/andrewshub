import os
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

# Mock required dependencies for the test
import sys
import subprocess
import pytest
import os
from unittest.mock import patch, MagicMock

# Add the src directory to path for import
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

def get_db():
    """Get database connection"""
    pass

def get_current_user():
    """Get current user"""
    return "testuser"

class RepositoryManager:
    def __init__(self):
        self.db = get_db()
        self.user = get_current_user()

# Repository model
class Repository:
    def __init__(self, db: Session):
        self.db = db
        self.user = None

    def get_user(self):
        return self.user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/repositories", response_model=List[RepositorySchema])
async def list_repositories(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    List all repositories for the current user
    """
    try:
        repositories = db.query(Repository).filter(
            and_(
                Repository.owner_id == current_user.id,
                Repository.is_active == True
            )
        ).all()
           except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        return repositories
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTP
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {
        {
            "url": "https://github.com/testuser/test-repo"
        }
    }
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except  Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTP (
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=1)
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTP
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e:
        logger.error(f"Error listing repositories: {str(e)}")
        raise HTTPException(
            status_code=status.HTT
        )
        return []
    except Exception as e