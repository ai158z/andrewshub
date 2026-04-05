import pytest
from typing import Dict, Any
from stop_skill_library.core import SkillLibrary
from stop_skill_library.models import Skill
from stop_skill_library.skill_storage import SkillStorage


@pytest.fixture
def skill_storage():
    return SkillStorage()


@pytest.fixture
def sample_skills():
    parent_skill = Skill(
        id="parent_001",
        name="Parent Skill",
        description="A test parent skill",
        metadata={"category": "testing"}
    )
    
    child_skill = Skill(
        id="child_001",
        name="Child Skill",
        description="A test child skill",
        metadata={"category": "testing", "parent_id": "parent_001"}
    )
    
    return parent_skill, child_skill


def test_add_skill_basic(skill_storage):
    skill = Skill(
        id="test_001",
        name="Test Skill",
        description="A test skill",
        metadata={"type": "test"}
    )
    
    skill_storage.add_skill(skill)
    retrieved = skill_storage.get_skill("test_001")
    
    assert retrieved is not None
    assert retrieved.id == "test_001"
    assert retrieved.name == "Test Skill"


def test_get_nonexistent_skill(skill_storage):
    result = skill_storage.get_skill("nonexistent")
    assert result is None


def test_add_and_retrieve_skill(skill_storage):
    skill = Skill(
        id="storage_test_001",
        name="Storage Test Skill",
        description="Skill for storage test",
        metadata={"test": "data"}
    )
    
    skill_storage.add_skill(skill)
    retrieved = skill_storage.get_skill("storage_test_001")
    
    assert retrieved is not None
    assert retrieved.id == "storage_test_001"
    assert retrieved.name == "Storage Test Skill"
    assert retrieved.metadata["test"] == "data"


def test_list_skills(skill_storage):
    skill1 = Skill(
        id="list_test_1",
        name="List Test 1",
        description="First test skill",
        metadata={"category": "test"}
    )
    
    skill2 = Skill(
        id="list_test_2",
        name="List Test 2",
        description="Second test skill",
        metadata={"category": "test", "priority": "high"}
    )
    
    skill_storage.add_skill(skill1)
    skill_storage.add_skill(skill2)
    
    skills = skill_storage.list_skills()
    assert len(skills) >= 2
    assert skill1 in skills
    assert skill2 in skills


def test_hierarchical_parent_child_relationship(skill_storage, sample_skills):
    parent_skill, child_skill = sample_skills
    skill_storage.add_skill(parent_skill)
    skill_storage.add_skill(child_skill)
    
    children = skill_storage.get_children("parent_001")
    parent = skill_storage.get_parent("child_001")
    
    assert len(children) == 1
    assert children[0].id == "child_001"
    assert parent.id == "parent_001"


def test_get_children_nonexistent_parent(skill_storage):
    children = skill_storage.get_children("nonexistent_parent")
    assert children == []


def test_get_parent_nonexistent_child(skill_storage):
    parent = skill_storage.get_parent("nonexistent_child")
    assert parent is None


def test_add_skill_with_empty_metadata(skill_storage):
    skill = Skill(
        id="empty_meta_001",
        name="Empty Metadata Skill",
        description="Skill with no metadata",
        metadata={}
    )
    
    skill_storage.add_skill(skill)
    retrieved = skill_storage.get_skill("empty_meta_001")
    
    assert retrieved is not None
    assert retrieved.id == "empty_meta_001"
    assert retrieved.metadata == {}


def test_skill_equality_after_storage(skill_storage):
    original_skill = Skill(
        id="equality_test_001",
        name="Equality Test",
        description="Test skill equality",
        metadata={"test": "equality"}
    )
    
    skill_storage.add_skill(original_skill)
    retrieved_skill = skill_storage.get_skill("equality_test_001")
    
    # Test that retrieved skill equals original skill
    assert retrieved_skill == original_skill
    # Test specific attributes to ensure data integrity
    assert retrieved_skill.id == original_skill.id
    assert retrieved_skill.name == original_skill.name
    assert retrieved_skill.description == original_skill.description
    assert retrieved_skill.metadata == original_skill.metadata


def test_multiple_child_skills_same_parent(skill_storage):
    parent = Skill(
        id="multi_child_parent",
        name="Parent Skill",
        description="Parent for multiple children",
        metadata={}
    )
    
    child1 = Skill(
        id="multi_child_1",
        name="Child 1",
        description="First child",
        metadata={"parent_id": "multi_child_parent"}
    )
    
    child2 = Skill(
        id="multi_child_2",
        name="Child 2",
        description="Second child",
        metadata={"parent_id": "multi_child_parent"}
    )
    
    skill_storage.add_skill(parent)
    skill_storage.add_skill(child1)
    skill_storage.add_skill(child2)
    
    children = skill_storage.get_children("multi_child_parent")
    
    assert len(children) == 2
    child_ids = [child.id for child in children]
    assert "multi_child_1" in child_ids
    assert "multi_child_2" in child_ids


def test_skill_storage_with_none_metadata(skill_storage):
    skill = Skill(
        id="none_metadata_001",
        name="None Metadata Skill",
        description="Skill with None metadata",
        metadata=None
    )
    
    # Should handle None metadata gracefully
    skill_storage.add_skill(skill)
    retrieved = skill_storage.get_skill("none_metadata_001")
    
    assert retrieved is not None
    assert retrieved.id == "none_metadata_001"
    # If metadata is None, it should be converted to empty dict or handled gracefully
    assert isinstance(retrieved.metadata, dict)


def test_overwrite_existing_skill(skill_storage):
    skill1 = Skill(
        id="overwrite_test",
        name="Original Name",
        description="Original skill",
        metadata={"version": "1.0"}
    )
    
    skill2 = Skill(
        id="overwrite_test",
        name="Updated Name",
        description="Updated skill",
        metadata={"version": "2.0"}
    )
    
    skill_storage.add_skill(skill1)
    skill_storage.add_skill(skill2)
    
    retrieved = skill_storage.get_skill("overwrite_test")
    assert retrieved.name == "Updated Name"
    assert retrieved.metadata["version"] == "2.0"


def test_get_skill_preserves_data_types(skill_storage):
    skill = Skill(
        id="type_test_001",
        name="Type Test Skill",
        description="Testing data types",
        metadata={
            "string_val": "test",
            "int_val": 42,
            "float_val": 3.14,
            "bool_val": True,
            "list_val": ["a", "b", "c"],
            "dict_val": {"nested": "value"}
        }
    )
    
    skill_storage.add_skill(skill)
    retrieved = skill_storage.get_skill("type_test_001")
    
    assert isinstance(retrieved, Skill)
    assert retrieved.metadata["string_val"] == "test"
    assert retrieved.metadata["int_val"] == 42
    assert retrieved.metadata["float_val"] == 3.14
    assert retrieved.metadata["bool_val"] is True
    assert retrieved.metadata["list_val"] == ["a", "b", "c"]
    assert retrieved.metadata["dict_val"] == {"nested": "value"}