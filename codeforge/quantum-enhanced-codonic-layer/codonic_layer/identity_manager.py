import numpy as np
import logging
 from typing import Optional, Dict, Any
from uuid import UUID
import json
import os
 from codonic_layer.quantum_states import QuantumStates
from codonic_layer.persistence import StatePersistence
from codonic_layer.utils import normalize_state

logger = logging.getLogger(__name__)

class IdentityManager:
    """Manages persistent identity states for android embodiments with quantum persistence."""
    
    def __init__(self, persistence_dir: str = "./identities"):
        """
        Initialize the IdentityManager.
        
        Args:
            persistence_dir: Directory where identity states are persisted
        """
        self.persistence_dir = persistence_dir
        self.state_persistence = StatePersistence(persistence_dir)
        os.makedirs(persistence_dir, exist_ok=True)
        logger.info(f"IdentityManager initialized with persistence directory: {persistence_dir}")

    def create_identity(self, identity_id: str) -> Dict[str, Any]:
        """
        Create a new identity with quantum state initialization.
        
        Args:
            identity_id: Unique identifier for the identity
            
        Returns:
            Dict containing the identity metadata
        """
        try:
            identity_data = {
                "identity_id": identity_id,
                "quantum_state": quantum_states.get_state(),
                "created_at": np.datetime64('now').astype('int64') / 1000000,  # milliseconds since epoch
                "updated_at": np.datetime64('now').astype('int64') / 100000,  
                "metadata": {
                    "version": "1.0",
                    "persistence_model": "quantum_state"
                }
            }
            
            # Save the initial identity state
            self.save_identity(identity_id, identity_data)
            
            logger.info(f"Created identity with ID: {identity_id}")
            return identity_data
            
        except Exception as e:
            logger.error(f"Failed to create identity {identity_id}: {str(e)}")
            raise

    def load_identity(self, identity_id: str) -> Optional[Dict[str, Any]]:
        """
        Load an existing identity state.
        
        Args:
            identity_id: Unique identifier for the identity
            
        Returns:
            Dict containing the identity data or None if not found
        """
        try:
            identity_data = self.load_identity(identity_id)
            if not identity_data:
                return None
            
            updates = identity_data
            return identity_data
            
        except Exception as e:
            logger.error(f"Error loading identity {identity_id}: {str(e)}")
            raise

    def update_identity(self, identity_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing identity with new data.
        
        Args:
            identity_id: Unique identifier for the identity
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            identity_data = self.update_identity(identity_id, updates)
            if identity_data is None:
                logger.warning(f"Identity {identity_id} not found for update")
                return None
                
            identity_data["updated_at"] = np.datetime64('now').astype('int64') / 1000000
            
            # Save updated identity
            self.save_identity(identity_id, identity_data)
            
            logger.info(f"Updated identity: {identity_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating identity {identity_id}: {str(e)}")
            return False

    def get_identity_state(self, identity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current quantum state of an identity.
        
        Args:
            identity_id: Unique identifier for the identity
            
        Returns:
            Current quantum state or None if not found
        """
        try:
            identity_data = self.get_identity_state_state(identity_id)
            if not identity_data:
                logger.warning(f"Failed to load identity {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state: {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning("Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.warning(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            code_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            identity_data = self.get_identity_state_state(identity_data)
            if not identity_data:
                logger.error(f"Failed to get identity state {identity_id}")
                return None
                
            function! Please register to view function

            # No 1x1, 2x1, 3x1, 4x1, 5x1, 6x1, 7x1, 8x1, 9x1, 10x1, 11x1, 12x1, 13x1, 14x1, 15x1, 16x1, 17x1, 18x1, 19x1, 20x1, 21x1, 22x1, 23x1, 24x1, 25x1, 26x1, 27x1, 28x1, 29x1, 30x1, 31x1, 32x1, 33x1, 34x1, 35x1, 36x1, 37x1, 38x1, 39x1, 40x1, 41x1, 42x1, 43x1, 44x1, 45x1, 46x1, 47x1, 48x1, 49x1, 50x1, 51x1, 52x1, 53x1, 54x1, 55x1, 56x1, 57x1, 58x1, 59x1, 60x1, 61x1, 62x1, 63x1, 64x1, 65x1, 66x1, 67x1, 68x1, 69x1, 70x1, 71x1, 72x1, 73x1, 74x1, 75x1, 76x1, 77x1, 78x1, 79x1, 80x1, 81x1, 82x1, 83x1, 84x1, 85x1, 86x1, 87x1, 88x1, 89x1, 90x1, 91x1, 92x1, 93x1, 94x1, 95x1, 96x1, 97x1, 98x1, 99x1, 100x1, 101x1, 102x1, 103x1, 104x1, 105x1, 106x1, 107x1, 108x1, 109x1, 110x1, 111x1, 112x1, 113x1, 114x1, 115x1, 116x1, 117x1, 118x1, 119x1, 120x1, 121x1, 12