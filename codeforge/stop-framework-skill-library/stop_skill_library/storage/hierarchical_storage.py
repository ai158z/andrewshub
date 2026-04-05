import logging
from typing import Dict, List, Optional, Any
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)


class HierarchicalStorage:
    """A hierarchical storage system that organizes skills in a tree-like structure."""

    def __init__(self):
        """Initialize the hierarchical storage system."""
        self._storage: Dict[str, Any] = {}
        self._children: Dict[str, List[str]] = defaultdict(list)
        self._parent: Dict[str, str] = {}
        self._root_nodes: List[str] = []
        logger.info("HierarchicalStorage initialized")

    def add(self, path: str, data: Any) -> bool:
        """
        Add data to the hierarchical storage at the specified path.
        
        Args:
            path: The hierarchical path (e.g., "skills/machine_learning/supervised")
            data: The data to store
            
        Returns:
            bool: True if successfully added, False otherwise
            
        Raises:
            ValueError: If path is invalid
        """
        if not path or not isinstance(path, str):
            raise ValueError("Path must be a non-empty string")
            
        if path.startswith('/') or path.endswith('/'):
            raise ValueError("Path should not start or end with '/'")
            
        # Normalize path
        normalized_path = Path(path).as_posix()
        if normalized_path != path:
            logger.debug(f"Path normalized from {path} to {normalized_path}")
            
        # Create the path in our storage structure
        path_parts = normalized_path.split('/')
        current_path = ""
        
        # Build the hierarchy
        for i, part in enumerate(path_parts):
            if current_path:
                parent_path = current_path
                current_path = f"{current_path}/{part}"
            else:
                parent_path = None
                current_path = part
                
            # If this is not the leaf node, ensure it exists as a container
            if i < len(path_parts) - 1:
                if current_path not in self._storage:
                    self._storage[current_path] = {}
                if parent_path and current_path not in self._children[parent_path]:
                    self._children[parent_path].append(current_path)
                if parent_path:
                    self._parent[current_path] = parent_path
            else:
                # This is the leaf node, store the actual data
                self._storage[current_path] = data
                if parent_path:
                    self._parent[current_path] = parent_path
                if parent_path and current_path not in self._children[parent_path]:
                    self._children[parent_path].append(current_path)
                    
        # Handle root nodes
        if len(path_parts) == 1 and normalized_path not in self._root_nodes:
            self._root_nodes.append(normalized_path)
                    
        logger.info(f"Data added at path: {normalized_path}")
        return True

    def get(self, path: str) -> Optional[Any]:
        """
        Retrieve data from the storage at the specified path.
        
        Args:
            path: The hierarchical path to retrieve data from
            
        Returns:
            The data at the path, or None if not found
        """
        if not path:
            return None
            
        normalized_path = Path(path).as_posix()
        return self._storage.get(normalized_path)

    def remove(self, path: str) -> bool:
        """
        Remove data from the storage at the specified path.
        
        Args:
            path: The hierarchical path to remove
            
        Returns:
            bool: True if successfully removed, False if not found
        """
        normalized_path = Path(path).as_posix()
        
        if normalized_path not in self._storage:
            logger.warning(f"Path {normalized_path} not found for removal")
            return False
            
        # Remove from parent's children list
        parent = self._parent.get(normalized_path)
        if parent and normalized_path in self._children[parent]:
            self._children[parent].remove(normalized_path)
            
        # Remove from storage
        if normalized_path in self._storage:
            del self._storage[normalized_path]
            
        # Remove from parent mapping
        if normalized_path in self._parent:
            del self._parent[normalized_path]
            
        # Remove from children mappings
        if normalized_path in self._children:
            del self._children[normalized_path]
            
        # Remove from root nodes if it's a root
        if normalized_path in self._root_nodes:
            self._root_nodes.remove(normalized_path)
            
        logger.info(f"Data removed from path: {normalized_path}")
        return True

    def list_children(self, path: str = "") -> List[str]:
        """
        List children of the specified path.
        
        Args:
            path: The parent path to list children for (empty for root)
            
        Returns:
            List of child paths
        """
        normalized_path = Path(path).as_posix() if path else ""
        if not path:
            # Return root nodes
            return self._root_nodes[:]
        return self._children.get(normalized_path, [])[:]

    def get_parent(self, path: str) -> Optional[str]:
        """
        Get the parent path of the specified path.
        
        Args:
            path: The path to get parent for
            
        Returns:
            The parent path or None if root
        """
        normalized_path = Path(path).as_posix()
        return self._parent.get(normalized_path)