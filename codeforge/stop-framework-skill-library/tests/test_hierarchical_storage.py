import pytest
from pathlib import Path
from stop_skill_library.storage.hierarchical_storage import HierarchicalStorage


class TestHierarchicalStorage:
    def test_add_valid_path_stores_data(self):
        storage = HierarchicalStorage()
        result = storage.add("skills/machine_learning", {"name": "ML Skill"})
        assert result is True
        assert storage.get("skills/machine_learning") == {"name": "ML Skill"}

    def test_add_invalid_path_raises_valueerror(self):
        storage = HierarchicalStorage()
        with pytest.raises(ValueError):
            storage.add("", {"data": "test"})
        with pytest.raises(ValueError):
            storage.add("/invalid/path", {"data": "test"})

    def test_add_non_string_path_raises_valueerror(self):
        storage = HierarchicalStorage()
        with pytest.raises(ValueError):
            storage.add(123, {"data": "test"})

    def test_get_existing_path_returns_data(self):
        storage = HierarchicalStorage()
        storage.add("skills/machine_learning", {"name": "ML Skill"})
        result = storage.get("skills/machine_learning")
        assert result == {"name": "ML Skill"}

    def test_get_nonexistent_path_returns_none(self):
        storage = HierarchicalStorage()
        result = storage.get("nonexistent/path")
        assert result is None

    def test_get_empty_path_returns_none(self):
        storage = HierarchicalStorage()
        result = storage.get("")
        assert result is None

    def test_remove_existing_path_returns_true(self):
        storage = HierarchicalStorage()
        storage.add("skills/machine_learning", {"name": "ML Skill"})
        result = storage.remove("skills/machine_learning")
        assert result is True
        assert storage.get("skills/machine_learning") is None

    def test_remove_nonexistent_path_returns_false(self):
        storage = HierarchicalStorage()
        result = storage.remove("nonexistent/path")
        assert result is False

    def test_list_children_root_returns_all_paths(self):
        storage = HierarchicalStorage()
        storage.add("skills/machine_learning", {"name": "ML Skill"})
        storage.add("skills/nlp", {"name": "NLP Skill"})
        children = storage.list_children()
        assert "skills/machine_learning" in children
        assert "skills/nlp" in children

    def test_list_children_specific_path(self):
        storage = HierarchicalStorage()
        storage.add("skills/machine_learning/supervised", {"name": "Supervised"})
        storage.add("skills/machine_learning/unsupervised", {"name": "Unsupervised"})
        children = storage.list_children("skills/machine_learning")
        assert "skills/machine_learning/supervised" in children
        assert "skills/machine_learning/unsupervised" in children

    def test_list_children_nonexistent_path_returns_empty_list(self):
        storage = HierarchicalStorage()
        children = storage.list_children("nonexistent")
        assert children == []

    def test_get_parent_returns_correct_parent(self):
        storage = HierarchicalStorage()
        storage.add("skills/machine_learning/supervised", {"name": "Supervised"})
        parent = storage.get_parent("skills/machine_learning/supervised")
        assert parent == "skills/machine_learning"

    def test_get_parent_root_node_returns_none(self):
        storage = HierarchicalStorage()
        storage.add("skills", {"name": "Root Skill"})
        parent = storage.get_parent("skills")
        assert parent is None

    def test_get_parent_nonexistent_path_returns_none(self):
        storage = HierarchicalStorage()
        parent = storage.get_parent("nonexistent/path")
        assert parent is None

    def test_add_path_with_trailing_slash_raises_valueerror(self):
        storage = HierarchicalStorage()
        with pytest.raises(ValueError):
            storage.add("invalid/path/", {"data": "test"})

    def test_add_path_with_leading_slash_raises_valueerror(self):
        storage = HierarchicalStorage()
        with pytest.raises(ValueError):
            storage.add("/invalid/path", {"data": "test"})

    def test_add_multiple_nested_paths(self):
        storage = HierarchicalStorage()
        storage.add("a/b/c", {"data": "nested"})
        assert storage.get("a/b/c") == {"data": "nested"}
        assert storage.get("a/b") is not None
        assert storage.get("a") is not None

    def test_remove_path_removes_from_parent_children(self):
        storage = HierarchicalStorage()
        storage.add("parent/child", {"data": "test"})
        storage.remove("parent/child")
        assert "parent/child" not in storage._children["parent"]

    def test_list_children_empty_path_returns_root_nodes(self):
        storage = HierarchicalStorage()
        storage.add("root1", {"data": "root"})
        storage.add("root2", {"data": "root"})
        children = storage.list_children()
        assert "root1" in children
        assert "root2" in children

    def test_add_normalizes_path_separators(self):
        storage = HierarchicalStorage()
        # Using backslashes to test normalization
        storage.add("a\\b\\c", {"data": "test"})
        # Should be stored with forward slashes
        assert storage.get("a/b/c") == {"data": "test"}