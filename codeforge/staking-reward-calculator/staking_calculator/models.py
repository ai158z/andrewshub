from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Dict, Any
import json

@dataclass
class StakingParameters:
    """Data class to hold staking parameters"""
    apy: Decimal
    lockup_period: int
    compound_frequency: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'apy': str(self.apy),
            'lockup_period': self.lockup_period,
            'compound_frequency': self.compound_frequency
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StakingParameters':
        """Create instance from dictionary"""
        return cls(
            apy=Decimal(data['apy']),
            lockup_period=int(data['lockup_period']),
            compound_frequency=int(data['compound_frequency'])
        )

@dataclass
class RewardBreakdown:
    """Data class to hold reward breakdown information"""
    total_reward: Decimal
    compound_rewards: Decimal
    penalty_deductions: Decimal
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'total_reward': str(self.total_reward),
            'compound_rewards': str(self.compound_rewards),
            'penalty_deductions': str(self.penalty_deductions)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RewardBreakdown':
        """Create instance from dictionary"""
        return cls(
            total_reward=Decimal(data['total_reward']),
            compound_rewards=Decimal(data['compound_rewards']),
            penalty_deductions=Decimal(data['penalty_deductions'])
        )

@dataclass
class StakingResult:
    """Complete staking result including parameters and breakdown"""
    parameters: StakingParameters
    breakdown: RewardBreakdown
    stake_amount: Decimal
    duration: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'parameters': self.parameters.to_dict(),
            'breakdown': self.breakdown.to_dict(),
            'stake_amount': str(self.stake_amount),
            'duration': self.duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StakingResult':
        """Create instance from dictionary"""
        parameters = StakingParameters.from_dict(data['parameters'])
        breakdown = RewardBreakdown.from_dict(data['breakdown'])
        return cls(
            parameters=parameters,
            breakdown=breakdown,
            stake_amount=Decimal(data['stake_amount']),
            duration=int(data['duration'])
        )

@dataclass
class CompoundFrequency:
    """Compound frequency options"""
    DAILY = 365
    WEEKLY = 52
    MONTHLY = 12
    QUARTERLY = 4
    ANNUALLY = 1

@dataclass
class StakingReward:
    """Represents a single staking reward calculation result"""
    principal: Decimal
    apy: Decimal
    duration: int
    compound_frequency: int
    penalty_rate: Decimal
    total_reward: Decimal
    compound_rewards: Decimal
    penalty_deductions: Decimal
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'principal': str(self.principal),
            'apy': str(self.apy),
            'duration': self.duration,
            'compound_frequency': self.compound_frequency,
            'penalty_rate': str(self.penalty_rate),
            'total_reward': str(self.total_reward),
            'compound_rewards': str(self.compound_rewards),
            'penalty_deductions': str(self.penalty_deductions)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StakingReward':
        """Create instance from dictionary"""
        return cls(
            principal=Decimal(data['principal']),
            apy=Decimal(data['apy']),
            duration=int(data['duration']),
            compound_frequency=int(data['compound_frequency']),
            penalty_rate=Decimal(data['penalty_rate']),
            total_reward=Decimal(data['total_reward']),
            compound_rewards=Decimal(data['compound_rewards']),
            penalty_deductions=Decimal(data['penalty_deductions'])
        )