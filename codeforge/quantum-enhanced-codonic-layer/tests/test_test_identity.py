import pytest
import tempfile
import os
from codonic_layer.identity_manager import IdentityManager
from codonic_layer.persistence import StatePersistence

def test_identity_creation():
    """Test identity creation functionality"""
    manager = IdentityManager()
    
    identity_id = "test_user_001"
    identity_data = {
        "name": "Test User",
        "role": "test_role",
        "permissions": ["read", "write"]
    }
    
    created_identity = manager.create_identity(identity_id, identity_data)
    
    assert created_identity is not None
    assert created_identity["id"] == identity_id
    assert created_identity["data"]["name"] == identity_data["name"]

def test_identity_retrieval():
    """Test retrieving an identity"""
    manager = IdentityManager()
    
    identity_id = "test_user_002"
    identity_data = {
        "name": "Test User",
        "role": "test_role",
        "permissions": ["read", "write"]
    }
    
    manager.create_identity(identity_id, identity_data)
    retrieved_identity = manager.get_identity_state(identity_id)
    
    assert retrieved_identity is not None
    assert retrieved_identity["data"]["name"] == identity_data["name"]

def test_identity_update():
    """Test identity update functionality"""
    manager = IdentityManager()
    
    identity_id = "test_user_003"
    identity_data = {"name": "Test User", "initial": True}
    
    manager.create_identity(identity_id, identity_data)
    manager.update_identity(identity_id, {"updated": True})
    
    updated_identity = manager.get_identity_state(identity_id)
    assert updated_identity["data"]["name"] == "Test User"
    assert updated_identity["data"]["initial"] is True
    assert updated_identity["data"]["updated"] is True

def test_identity_deletion():
    """Test identity deletion"""
    manager = IdentityManager()
    
    identity_id = "test_user_004"
    identity_data = {"name": "Delete Test"}
    
    manager.create_identity(identity_id, identity_data)
    manager.delete_identity(identity_id)
    
    assert manager.get_identity_state(identity_id) is None

def test_empty_identity_id():
    """Test creating identity with empty ID"""
    manager = IdentityManager()
    
    with pytest.raises(ValueError):
        manager.create_identity("", {"test": "data"})

def test_none_identity_data():
    """Test handling None identity data"""
    manager = IdentityManager()
    
    with pytest.raises(ValueError):
        manager.create_identity("test_id", None)

def test_invalid_identity_data():
    """Test creating identity with invalid data"""
    manager = IdentityManager()
    
    with pytest.raises(ValueError):
        manager.create_identity("test_id", "invalid_data")

def test_persistence_save_load():
    """Test persistence save and load functionality"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_filename = tmp_file.name
    
    identity_data = {"name": "Persistence Test", "value": 42}
    persistence = StatePersistence()
    
    persistence.save_state("persistence_test", identity_data, tmp_filename)
    loaded_data = persistence.load_state(tmp_filename)
    
    assert loaded_data is not None
    assert loaded_data["name"] == "Persistence Test"
    assert loaded_data["value"] == 42

def test_persistence_file_operations():
    """Test file operations in persistence"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_filename = tmp_file.name
    
    # Test that file operations work correctly
    data = {"test": "data"}
    persistence = StatePersistence()
    
    persistence.save_state("file_test", data, tmp_filename)
    loaded = persistence.load_state(tmp_filename)
    
    assert loaded is not None
    assert loaded["test"] == "data"

def test_identity_manager_get_state():
    """Test IdentityManager get_state method"""
    manager = IdentityManager()
    identity_data = {"name": "Test", "value": 100}
    
    manager.create_identity("get_state_test", identity_data)
    state = manager.get_identity_state("get_state_test")
    
    assert state is not None
    assert state["data"]["name"] == "Test"
    assert state["data"]["value"] == 100

def test_identity_manager_update_state():
    """Test updating identity state"""
    manager = IdentityManager()
    identity_data = {"name": "Update Test", "status": "active"}
    
    manager.create_identity("update_test", identity_data)
    manager.update_identity("update_test", {"status": "updated"})
    
    state = manager.get_identity_state("update_test")
    assert state is not None
    assert state["data"]["name"] == "Update Test"
    assert state["data"]["status"] == "updated"

def test_persistence_error_handling():
    """Test persistence error handling"""
    persistence = StatePersistence()
    
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        persistence.load_state("non_existent_file.json")
    
    # Test with invalid data
    with pytest.raises(ValueError):
        persistence.save_state("test", None, "temp.json")

def test_identity_lifecycle():
    """Test complete identity lifecycle"""
    manager = IdentityManager()
    
    # Test creation
    identity_data = {"name": "Lifecycle Test", "created": True}
    manager.create_identity("lifecycle_test", identity_data)
    
    # Test retrieval
    state = manager.get_identity_state("lifecycle_test")
    assert state is not None
    assert state["data"]["name"] == "Lifecycle Test"
    
    # Test update
    manager.update_identity("lifecycle_test", {"updated": True})
    updated_state = manager.get_identity_state("lifecycle_test")
    assert updated_state["data"]["updated"] is True
    
    # Test deletion
    manager.delete_identity("lifecycle_test")
    final_state = manager.get_identity_state("lifecycle_test")
    assert final_state is None

def test_multiple_identities():
    """Test handling multiple identities"""
    manager = IdentityManager()
    
    # Create multiple identities
    id1_data = {"name": "User1", "type": "test"}
    id2_data = {"name": "User2", "type": "test"}
    
    manager.create_identity("user1", id1_data)
    manager.create_identity("user2", id2_data)
    
    # Verify both identities exist
    state1 = manager.get_identity_state("user1")
    state2 = manager.get_identity_state("user2")
    
    assert state1 is not None
    assert state2 is not None
    assert state1["data"]["name"] == "User1"
    assert state2["data"]["name"] == "User2"

def test_identity_state_validation():
    """Test identity state validation"""
    manager = IdentityManager()
    
    # Test with invalid state
    with pytest.raises(ValueError):
        manager.create_identity(None, {"test": "data"})
    
    # Test with valid state
    manager.create_identity("valid_test", {"name": "Valid"})
    state = manager.get_identity_state("valid_test")
    assert state is not None

def test_identity_permissions():
    """Test identity permissions handling"""
    manager = IdentityManager()
    identity_data = {
        "name": "Permission Test", 
        "permissions": ["read", "write", "execute"]
    }
    
    manager.create_identity("perm_test", identity_data)
    
    # Verify permissions are stored
    state = manager.get_identity_state("perm_test")
    assert state is not None
    assert "read" in state["data"]["permissions"]

def test_edge_cases():
    """Test edge cases in identity management"""
    manager = IdentityManager()
    
    # Test empty string
    with pytest.raises(ValueError):
        manager.create_identity("", {"test": "data"})
    
    # Test None data
    with pytest.raises(ValueError):
        manager.create_identity("test", None)
    
    # Test large identity ID
    large_id = "x" * 1000
    with pytest.raises(ValueError):
        manager.create_identity(large_id, {"test": "data"})

def test_file_permissions():
    """Test file permission handling"""
    # Test with file that doesn't exist
    with pytest.raises(IOError):
        with open("nonexistent.txt", "r") as f:
            f.read()
    
    # Test with valid file permissions
    with tempfile.NamedTemporaryFile(mode='w') as tmp:
        try:
            os.chmod(tmp.name, 0o600)
            # Should have permission
            with open(tmp.name, "r"):
                pass
        except PermissionError:
            pytest.fail("Should have had permission to access file")

def test_identity_persistence_compatibility():
    """Test state persistence compatibility"""
    manager = IdentityManager()
    persistence = StatePersistence()
    
    # Test compatibility between manager and persistence
    test_data = {"version": "1.0", "data": "test"}
    manager.create_identity("compat_test", test_data)
    
    state = manager.get_identity_state("compat_test")
    assert state is not None
    assert state["data"]["version"] == "1.0"

def test_identity_manager_error_cases():
    """Test error cases in identity manager"""
    manager = IdentityManager()
    
    # Test None manager
    with pytest.raises(TypeError):
        manager.create_identity(None, {"test": "data"})
    
    # Test invalid data
    with pytest.raises(ValueError):
        manager.create_identity("error_test", "invalid")
    
    # Test valid case
    manager.create_identity("valid_error_test", {"name": "Valid"})
    state = manager.get_identity_state("valid_error_test")
    assert state is not None