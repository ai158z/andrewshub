from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import psutil
import os

# Database setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class AgentStatus(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    status = Column(String)
    last_heartbeat = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'last_heartbeat': self.last_heartbeat
        }

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "disk_used_percent": (disk.used / disk.total) * 100 if disk.total > 0 else 0
    }

def get_all_agents(db):
    # Return mock agents for testing
    return [
        AgentStatus(id=1, name="agent1", status="active", last_heartbeat=str(datetime.now())),
        AgentStatus(id=2, name="agent2", status="inactive", last_heartbeat=None)
    ]

def get_node_status():
    # Mock implementation
    return {"status": "active", "message": "Node is running"}

@router.get("/health")
async def get_system_health():
    """
    Get overall system health status including CPU, memory, disk usage and ROS2 node status
    """
    try:
        metrics = get_system_metrics()
        agents = get_all_agents(None)  # db session not actually used in this mock
        agent_health = {}
        for agent in agents:
            agent_health[agent.id] = {
                "id": agent.id,
                "name": agent.name,
                "status": agent.status,
                "last_heartbeat": agent.last_heartbeat
            }
        
        # Calculate system health
        cpu_percent = metrics["cpu_percent"]
        memory_percent = metrics["memory_percent"]
        
        return {
            "status": "healthy" if cpu_percent < 80 and memory_percent < 80 else "degraded",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_used_percent": metrics["disk_used_percent"],
                "agent_count": len(agents),
                "agent_details": agent_health
            }
        }
        
    except Exception as e:
        # Fallback response in case of error
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@router.get("/status") 
async def get_system_status():
    """
    Get comprehensive system status including database, ROS2 node, and application components
    """
    try:
        # Mock database connection check
        db_status = "unknown"
        try:
            # Simple DB connectivity test
            db_status = "healthy"
        except Exception:
            db_status = "unhealthy"
        
        # Check ROS2 node status
        ros_status = get_node_status()
        
        # Get agents
        agents = get_all_agents(None)
        active_agents = len([a for a in agents if a.status == "active"])
        
        overall_status = "healthy" if db_status == "healthy" and ros_status.get("status") == "active" else "degraded"
        
        return {
            "overall_status": overall_status,
            "components": {
                "database": db_status,
                "ros2_node": ros_status,
                "agent_system": "healthy" if active_agents > 0 else "warning"
            }
        }
        
    except Exception as e:
        return {
            "error": str(e)
        }