import sqlite3
import logging
import os
from typing import Optional
import json

class SkillRepository:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.environ.get("DATABASE_URL", "sqlite:///skills.db")
        
        self.db_path = db_path
        self.vector_db = None  # Will be initialized lazily to avoid circular imports
        self._init_db()
    
    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS skills (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        domain TEXT,
                        complexity TEXT,
                        utility TEXT,
                        metadata TEXT
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            raise

    def _get_vector_db(self):
        """Lazily initialize VectorDB to avoid circular import issues"""
        if self.vector_db is None:
            from src.skill_library.storage.vector_db import VectorDB
            self.vector_db = VectorDB()
        return self.vector_db

    def save(self, skill) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO skills (id, name, description, domain, complexity, utility, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    skill.id,
                    skill.name,
                    skill.description,
                    getattr(skill, 'domain', None) and skill.domain.get_category() if hasattr(skill, 'domain') and skill.domain else None,
                    getattr(skill, 'complexity', None) and skill.complexity.assess() if hasattr(skill, 'complexity') and skill.complexity else None,
                    getattr(skill, 'utility', None) and skill.utility.calculate() if hasattr(skill, 'utility') and skill.utility else None,
                    json.dumps(getattr(skill, 'metadata', None)) if hasattr(skill, 'metadata') and skill.metadata else None
                ))
                conn.commit()
                if hasattr(skill, 'id') and skill.id:  # Only add to vector DB if it's a valid skill with ID
                    self._get_vector_db().add_skill(skill)
                return True
        except Exception as e:
            logging.error(f"Error saving skill {getattr(skill, 'id', 'unknown')}: {e}")
            return False

    def get(self, skill_id: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM skills WHERE id = ?', (skill_id,))
                row = cursor.fetchone()
                if row:
                    return row
                return None
        except Exception as e:
            logging.error(f"Error retrieving skill {skill_id}: {e}")
            return None

    def delete(self, skill_id: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM skills WHERE id = ?', (skill_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deleting skill {skill_id}: {e}")
            return False