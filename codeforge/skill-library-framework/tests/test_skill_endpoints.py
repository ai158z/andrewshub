import pytest
from fastapi.testclient import TestClient
from src.skill_library.api.skill_endpoints import router

client = TestClient(router)

class TestSkillEndpoints:
    def test_get_skills_endpoint(self):
        response = client.get("/skills")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_skill_success(self):
        skill_data = {"id": "test-skill-1", "name": "Test Skill"}
        response = client.post("/skills", json=skill_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Skill created"

    def test_create_skill_missing_id(self):
        skill_data = {"name": "Test Skill"}
        response = client.post("/skills", json=skill_data)
        assert response.status_code == 400
        assert "Skill ID is required" in response.json()["detail"]

    def test_create_skill_exception_handling(self, mocker):
        mocker.patch('src.skill_library.api.skill_endpoints.SkillRepository.save', side_effect=Exception("DB Error"))
        response = client.post("/skills", json={"id": "test-skill-2", "name": "Test Skill"})
        assert response.status_code == 500
        assert "DB Error" in response.json()["detail"]

    def test_delete_skill_success(self):
        response = client.delete("/skills/skill-123")
        assert response.status_code == 200
        assert response.json()["message"] == "Skill deleted"

    def test_delete_skill_exception_handling(self, mocker):
        mocker.patch('src.skill_library.api.skill_endpoints.SkillRepository.delete', side_effect=Exception("DB Error"))
        response = client.delete("/skills/skill-123")
        assert response.status_code == 500
        assert "DB Error" in response.json()["detail"]

    def test_get_skills_exception_handling(self, mocker):
        mocker.patch('src.skill_library.api.skill_endpoints.SkillRepository.__init__', side_effect=Exception("DB Error"))
        response = client.get("/skills")
        assert response.status_code == 500
        assert "DB Error" in response.json()["detail"]