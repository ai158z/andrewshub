from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

router = APIRouter()

class SkillCreateRequest(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

class SkillResponse(BaseModel):
    message: str

@router.get("/skills")
async def get_skills():
    try:
        repo = SkillRepository()
        skills = repo.get_all()
        return skills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skills", response_model=SkillResponse)
async def create_skill(skill: SkillCreateRequest):
    try:
        if not skill.id:
            raise HTTPException(status_code=400, detail="Skill ID is required")
        
        repo = SkillRepository()
        repo.save(skill.dict())
        return SkillResponse(message="Skill created")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/skills/{skill_id}", response_model=SkillResponse)
async def delete_skill(skill_id: str):
    try:
        repo = SkillRepository()
        repo.delete(skill_id)
        return SkillResponse(message="Skill deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SkillRepository:
    def __init__(self):
        self.file_path = "skills.json"
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)
    
    def get_all(self):
        with open(self.file_path, "r") as f:
            return json.load(f)
    
    def save(self, skill_data):
        skills = self.get_all()
        skills.append(skill_data)
        with open(self.file_path, "w") as f:
            json.dump(skills, f)
    
    def delete(self, skill_id):
        skills = self.get_all()
        filtered_skills = [s for s in skills if s.get("id") != skill_id]
        with open(self.file_path, "w") as f:
            json.dump(filtered_skills, f)