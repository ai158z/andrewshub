import logging
from typing import Dict, Any
import requests
from src.network_data import get_network_apy, get_network_commission
from src.currency_converter import convert_to_fiat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Risk thresholds
SLASHING_RISK_HIGH = 0.7
SLASHING_RISK_MEDIUM = 0.4
SLASHING_RISK_LOW = 0.1

# Network-specific risk factors (these would typically come from a database or API)
NETWORK_RISK_DATA = {
    "cosmos": {
        "slashing_risk": 0.05,
        "governance_risk": 0.03,
        "market_risk": 0.02,
        "security_risk": 0.01
    },
    "ethereum": {
        "slashing_risk": 0.02,
        "governance_risk": 0.05,
        "market_risk": 0.04,
        "security_risk": 0.02
    },
    "polkadot": {
        "slashing_risk": 0.03,
        "governance_risk": 0.04,
        "market_risk": 0.03,
        "security_risk": 0.01
    }
}

def get_network_risk_data(network: str) -> Dict[str, Any]:
    """Fetch risk data for a specific network"""
    return NETWORK_RISK_DATA.get(network.lower(), {
        "slashing_risk": 0.05,
        "governance_risk": 0.05,
        "market_risk": 0.05,
        "security_risk": 0.03
    })

def analyze_network_risks(network: str) -> dict:
    """
    Analyze risk factors that could affect staking rewards for a given network
    
    Args:
        network: The blockchain network to analyze
        
    Returns:
        Dictionary containing risk analysis results
    """
    try:
        # Get network risk data
        risk_data = get_network_risk_data(network)
        
        # Get base APY and commission for context
        try:
            base_apy = get_network_apy(network)
            commission_rate = get_network_commission(network)
        except Exception as e:
            logger.error(f"Error fetching network data for {network}: {str(e)}")
            base_apy = 0.0
            commission_rate = 0.0
            
        # Calculate risk-adjusted APY
        slashing_risk = risk_data["slashing_risk"]
        governance_risk = risk_data["governance_risk"]
        market_risk = risk_data["market_risk"]
        security_risk = risk_data["security_risk"]
        
        # Total risk score calculation
        total_risk_score = (
            slashing_risk * 0.4 +  # Slashing is weighted most heavily
            governance_risk * 0.3 +  # Governance risk
            market_risk * 0.2 +  # Market risk
            security_risk * 0.1   # Security risk
        )
        
        # Risk category classification
        if total_risk_score >= SLASHING_RISK_HIGH:
            risk_level = "HIGH"
        elif total_risk_score >= SLASHING_RISK_MEDIUM:
            risk_level = "MEDIUM"
        elif total_risk_score >= SLASHING_RISK_LOW:
            risk_level = "LOW"
        else:
            risk_level = "VERY_LOW"
            
        # Calculate potential loss scenarios
        potential_losses = {
            "annual_slashing": base_apy * slashing_risk,
            "annual_governance_loss": base_apy * governance_risk,
            "annual_market_loss": base_apy * market_risk,
            "annual_security_loss": base_apy * security_risk
        }
        
        # Risk-adjusted return calculation
        risk_adjusted_apy = base_apy * (1 - total_risk_score)
        
        # Generate risk report
        risk_report = {
            "network": network,
            "risk_level": risk_level,
            "total_risk_score": total_risk_score,
            "base_apy": base_apy,
            "risk_adjusted_apy": risk_adjusted_apy,
            "commission_rate": commission_rate,
            "risk_breakdown": {
                "slashing_risk": slashing_risk,
                "governance_risk": governance_risk,
                "market_risk": market_risk,
                "security_risk": security_risk
            },
            "potential_losses": potential_losses,
            "recommendations": _generate_risk_recommendations(network, risk_level, total_risk_score)
        }
        
        return risk_report
        
    except Exception as e:
        logger.error(f"Error analyzing network risks for {network}: {str(e)}")
        return {
            "network": network,
            "error": f"Failed to analyze risks: {str(e)}",
            "risk_level": "UNKNOWN",
            "total_risk_score": 0,
            "base_apy": 0,
            "risk_adjusted_apy": 0,
            "commission_rate": 0,
            "risk_breakdown": {},
            "potential_losses": {},
            "recommendations": []
        }

def _generate_risk_recommendations(network: str, risk_level: str, risk_score: float) -> list:
    """Generate risk-appropriate recommendations based on risk level"""
    recommendations = []
    
    if risk_level == "HIGH":
        recommendations.append("Consider diversifying stake across multiple validators")
        recommendations.append("Monitor network governance proposals closely")
        recommendations.append("Review validator performance regularly")
    elif risk_level == "MEDIUM":
        recommendations.append("Regular monitoring of validator performance recommended")
        recommendations.append("Stay informed about network governance")
    else:
        recommendations.append("Risk profile appears acceptable for current staking")
        recommendations.append("Continue standard monitoring practices")
    
    # Add network-specific recommendations
    if network.lower() in ["cosmos", "ethereum", "polkadot"]:
        recommendations.append(f"{network.title()} specific: Review network upgrade schedule")
    
    return recommendations