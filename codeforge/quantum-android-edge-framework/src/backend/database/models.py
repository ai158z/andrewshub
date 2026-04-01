import os
from typing import Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/quantumdb")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class NodeModel(Base):
    __tablename__ = "nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    config = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    location = Column(String, nullable=True)
    metadata_col = Column('metadata', JSONB, nullable=True)
    capabilities = Column(JSONB, nullable=True)
    last_heartbeat = Column(DateTime, nullable=True)
    encryption_key = Column(String, nullable=True)
    firmware_version = Column(String, nullable=True)
    hardware_revision = Column(String, nullable=True)
    operational_status = Column(String, default="online")
    assigned_tasks = Column(JSONB, nullable=True)
    performance_metrics = Column(JSONB, nullable=True)

class SimulationModel(Base):
    __tablename__ = "simulations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    simulation_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    scenario = Column(String, nullable=False)
    status = Column(String, default="pending")
    config = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    results = Column(JSONB, nullable=True)
    parameters = Column(JSONB, nullable=True)
    logs = Column(JSONB, nullable=True)
    tags = Column(JSONB, nullable=True)
    metadata_col = Column('metadata', JSONB, nullable=True)
    owner = Column(String, nullable=True)
    progress = Column(Float, default=0.0)
    __table_args__ = ({'schema': 'public'})

class QuantumState(Base):
    __tablename__ = "quantum_states"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_id = Column(String, unique=True, index=True, nullable=False)
    node_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    state_vector = Column(JSONB, nullable=False)
    entanglement_info = Column(JSONB, nullable=True)
    coherence_metrics = Column(JSONB, nullable=True)
    measurement_results = Column(JSONB, nullable=True)
    superposition_data = Column(JSONB, nullable=True)
    collapse_history = Column(JSONB, nullable=True)
    entropy_levels = Column(JSONB, nullable=True)
    phase_info = Column(JSONB, nullable=True)
    amplitude_damping = Column(JSONB, nullable=True)
    calibration_data = Column(JSONB, nullable=True)
    signal_strength = Column(Float, nullable=True)
    battery_level = Column(Float, nullable=True)
    error_flags = Column(JSONB, nullable=True)

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(String, unique=True, index=True, nullable=False)
    node_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSONB, nullable=False)
    processed_values = Column(JSONB, nullable=True)
    calibrated = Column(Boolean, default=False)
    sensor_type = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    location_x = Column(Float, default=0.0)
    location_y = Column(Float, default=0.0)
    location_z = Column(Float, default=0.0)
    temperature = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    acceleration = Column(Float, nullable=True)
    orientation = Column(JSONB, nullable=True)
    error_flags = Column(JSONB, nullable=True)

def create_tables():
    """Create database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Database session dependency for FastAPI"""
    pass

def init_db():
    """Initialize database connection and create tables"""
    try:
        create_tables()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

def get_db():
    """Database session dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()