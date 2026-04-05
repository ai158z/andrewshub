import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, Any, Tuple, Optional
from src.skill_catalog import SkillCatalog
from src.models.skill import Skill
from src.models.curiosity_model import CurricularModel
from src.models.task_predictor import TaskPredictor
import logging

logger = logging.getLogger(__name__)

class RLAgent:
    def __init__(self, observation_space, action_space, config=None):
        """
        Initialize the RL agent with policy network and curiosity model.

        Args:
            observation_space: The observation space of the environment
            action_space: The action space of the environment
            config: Configuration dictionary for the agent
        """
        self.observation_space = observation_space
        self.action_space = action_space
        self.config = config or {}

        # Validate spaces
        validate_observation_space(self.observation_space)
        validate_action_space(self.action_space)

        # Initialize components
        self.skill_catalog = SkillCatalog()
        self.task_predictor = TaskPredictor()

        # Initialize policy network
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_network = self._build_policy_network()
        self.optimizer = optim.Adam(self.policy_network.parameters(), lr=self.config.get('learning_rate', 0.001))

        logger.info("RLAgent initialized with observation space: %s, action space: %s",
                   self.observation_space, self.action_space)

    def _build_policy_network(self):
        """Build the policy network based on observation and action space."""
        obs_dim = np.prod(self.observation_space.shape) if hasattr(self.action_space, 'shape') else self.action_space.n
        # Simple MLP policy network
        network = nn.Sequential(
            nn.Linear(4, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 128)
        )

        return network.to(self.device)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
            action_logits = self.policy_network(obs_tensor)
            action_probs = torch.softmax(action_logits, dim=1)
            action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        curiosity_bonus = self.curiosity_model.compute_curiosity(observation)

        # Use curiosity bonus to modify action selection
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor.unsqueeze(1))

        # Compute loss (REINFORCE with baseline)
        # Using reward as the return (simplified)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        # Update curiosity model
        self.curiosity_model.update_curiosity(observations, next_observations)

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().item(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return metrics

        # Save the agent's model to disk.
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path=mock_observation_space, action_space=mock_action_space)
        logger.info("Model saved to %s", path)

        return "Model loaded from %s" % path

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        curiosity_bonus = self.curiosity_model.compute_curiosity(observation)

        # Use curiosity bonus to modify action selection
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor.unsqueeze(1))

        # Compute loss (REINFORCE with baseline)
        # Using reward as the return (simplified)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        # Update curiosity model
        self.curiosity_model.update_curiosity(observations, next_observations)

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().item(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return metrics

        return True

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad:
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Use curiosity bonus to modify action selection
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor.unsqueeze(1))

        # Compute loss (REINFORCE with baseline)
        # Using reward as the return (simplified)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        # Update curiosity model
        self.curiosity_model.update_curiosity(observations, next_observations)

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().item(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return metrics

        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor.unsqueeze(1))
        action_log_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Use curiosity bonus to modify action selection
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has to be ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        curiosity_bonus = self.curiosity_model.compute_curiosity(observation)

        # Use curiosity bonus to modify action selection
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor.unsqueeze(1))

        # Compute loss (REINFORCE with baseline)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().item(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return True

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration reward

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy results.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor.unsqueeze(1))

        # Compute loss (REINFORCE with baseline)
        # Using reward as the return (simplified)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        # Update curiosity model
        self.curiosity_model.update_curiosity(observations, next_observations)

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().rewards(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return metrics

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        # This is a simplified exploration implementation
        if torch.randn() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

        return True

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor)

        # Compute loss (REINFORCE with baseline)
        # Using reward as the return (simplified)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        # Update curiosity model
        self.curiosity_model.update_curiosity(observations, next_observations)

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().item(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return metrics

        return True

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'observation_space': self.observation_space,
            'action_space': self.action_space
        }

        torch.save(model_state, path)
        logger.info("Model saved to %s", path)
        return True

    def load_model(self, path: str) -> None:
        """
        Load the agent's model from disk.

        Args:
            path: File path to load the model from
        """
        model_state = torch.load(path, map_location=self.device)

        self.policy_network.load_state_dict(model_state['policy_network_state_dict'])
        self.optimizer.load_state_dict(model_state['optimizer_state_dict'])

        logger.info("Model loaded from %s", path)
        return True

    def add_experience(self, observation, action, reward, next_observation, done):
        """
        Add an experience to the agent's memory.

        Args:
            observation: Current environment observation
            action: Current environment action
            reward: Reward for the action
            next_observation: Next environment observation
            done: Whether the episode has ended
        """
        # Add experience
        self.replay_buffer.append(
            (observation, action, reward, next_observation, done)
        )
        return True

    def get_exploration_bonus(self, state):
        """
        Get the exploration bonus for a given state.

        Args:
            state: The state to get the exploration bonus for

        Returns:
            The exploration bonus
        """
        # Calculate curiosity bonus
        return self.curiosity_model.compute_curiosity(state)

    def select_action(self, observation):
        """
        Select an action using the policy network and curiosity-driven exploration.

        Args:
            observation: Current environment observation

        Returns:
            Tuple of (action, info) where info contains action metadata
        """
        obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)

        # Get action preferences from policy network
        with torch.no_grad():
        action_logits = self.policy_network(obs_tensor)
        action_probs = torch.softmax(action_logits, dim=1)
        action = torch.argmax(action_probs, dim=1).item()

        # Calculate curiosity bonus
        # This is a simplified exploration implementation
        if np.random.rand() < curiosity_bonus:
            # Sample action based on policy network probabilities
            action = np.random.choice(
                self.action_space.n if hasattr(self.action_space, 'n') else self.action_space.shape[0],
                p=torch.softmax(action_logits, dim=1).cpu().numpy().flatten()
            )

        info = {
            'action_prob': action_probs.cpu().numpy().tolist(),
            'curiosity_bonus': curiosity_bonus
        }

        return action, info

    def learn(self,
              observations: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_observations: np.ndarray,
              dones: np.ndarray) -> Dict[str, float]:
        """
        Update the policy network based on experiences.

        Returns:
            Dictionary of training metrics
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(observations).to(self.device)
        actions_tensor = torch.LongTensor(actions).to(self.device)
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        next_obs_tensor = torch.FloatTensor(next_observations).to(self.device)
        dones_tensor = torch.BoolTensor(dones).to(self.device)

        # Compute policy loss using policy gradient
        logits = self.policy_network(obs_tensor)
        log_probs = torch.log_softmax(logits, dim=1)
        action_log_probs = log_probs.gather(1, actions_tensor)

        # Compute loss (REINFORCE with baseline)
        # Using reward as the return (simplified)
        policy_loss = (-action_log_probs * advantages.unsqueeze(1)).mean()

        # Update network
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()

        # Update curiosity model
        self.curiosity_model.update_curiosity(observations, next_observations)

        metrics = {
            'loss': policy_loss.item(),
            'mean_curiosity': curiosity_rewards.mean().item(),
            'mean_reward': combined_rewards.mean().item()
        }

        logger.info("Training metrics: %s", metrics)
        return metrics

        return True

    def save_model(self, path: str) -> None:
        """
        Save the agent's model to disk.

        Args:
            path: File path to save the model
        """
        model_state = {
            'policy_network_state_dict': self.policy_network