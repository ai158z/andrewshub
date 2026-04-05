import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import numpy as np
from stop_skill_library.models import PerformanceMetrics

logger = logging.getLogger(__name__)

@dataclass
class PerformanceRecord:
    execution_time: float
    success: bool = True
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PerformanceTracker:
    def __init__(self):
        self.metrics: Dict[str, List[PerformanceRecord]] = {}
        self.total_executions: int = 0
        self.successful_executions: int = 0
        self.failed_executions: int = 0
        self.total_execution_time: float = 0.0
        self.start_time: float = time.time()
        
    def track(self, skill_id: str, execution_time: float, success: bool, error_message: Optional[str] = None):
        """Track performance metrics for a specific skill"""
        if skill_id not in self.metrics:
            self.metrics[skill_id] = []
            
        record = PerformanceRecord(
            execution_time=execution_time,
            success=success,
            error_message=error_message
        )
        self.metrics[skill_id].append(record)
        
        # Update aggregate metrics
        self.total_executions += 1
        self.total_execution_time += execution_time
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
            
        logger.debug(f"Tracked performance for skill {skill_id}: {execution_time}s, success={success}")

    def get_metrics(self, skill_id: Optional[str] = None) -> PerformanceMetrics:
        """Get performance metrics for a specific skill or overall metrics"""
        if not self.metrics:
            return PerformanceMetrics()
            
        if skill_id:
            if skill_id not in self.metrics:
                return PerformanceMetrics()
            records = self.metrics[skill_id]
        else:
            # Flatten all records for overall metrics
            records = []
            for skill_records in self.metrics.values():
                records.extend(skill_records)
                
        if not records:
            return PerformanceMetrics()
            
        total_executions = len(records)
        successful_executions = sum(1 for r in records if r.success)
        failed_executions = total_executions - successful_executions
        
        total_time = sum(r.execution_time for r in records) if records else 0
        avg_execution_time = total_time / len(records) if records else 0
        success_rate = successful_executions / total_executions if total_executions > 0 else 0
        
        return PerformanceMetrics(
            total_executions=total_executions,
            successful_executions=successful_executions,
            failed_executions=failed_executions,
            average_execution_time=avg_execution_time,
            success_rate=success_rate,
            total_execution_time=total_time
        )
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "tracking_duration": time.time() - self.start_time,
            "overall_metrics": self.get_metrics(),
            "skill_metrics": {},
            "execution_summary": {
                "total_executions": self.total_executions,
                "successful_executions": self.successful_executions,
                "failed_executions": self.failed_executions,
                "total_execution_time": self.total_execution_time
            }
        }
        
        # Add skill-specific metrics
        for skill_id in self.metrics:
            report["skill_metrics"][skill_id] = asdict(self.get_metrics(skill_id))
        
        logger.info("Generated performance report")
        return report