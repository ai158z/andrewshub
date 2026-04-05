import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

from stop_skill_library.models import PerformanceMetrics, Skill


@dataclass
class AnalysisResult:
    """Data class to hold performance analysis results"""
    skill_id: str
    metrics: List[PerformanceMetrics] = field(default_factory=list)
    insights: Dict[str, Any] = field(default_factory=dict)
    visualizations: Dict[str, Any] = field(default_factory=dict)


class PerformanceAnalyzer:
    """Performance analysis and reporting engine for skill library"""
    
    def __init__(self, performance_tracker):
        """
        Initialize the PerformanceAnalyzer with required dependencies.
        
        Args:
            performance_tracker: Instance of PerformanceTracker for accessing performance data
        """
        self.performance_tracker = performance_tracker
        self.logger = logging.getLogger(__name__)
        
    def analyze(self, skill_id: str, time_window: Optional[int] = None) -> AnalysisResult:
        """
        Analyze performance metrics for a specific skill over a given time window.
        
        Args:
            skill_id: The ID of the skill to analyze
            time_window: Time window in days to analyze (default: all time)
            
        Returns:
            AnalysisResult containing metrics and statistical analysis
        """
        try:
            # Get performance metrics
            metrics = self.performance_tracker.get_metrics(skill_id)
            
            # Filter by time window if specified
            if time_window:
                cutoff_date = datetime.now() - timedelta(days=time_window)
                metrics = [m for m in metrics if m.timestamp >= cutoff_date]
            
            # Create analysis result
            result = AnalysisResult(skill_id=skill_id, metrics=metrics)
            
            # Generate basic statistics
            if metrics:
                result.insights = self._calculate_insights(metrics)
            
            self.logger.info(f"Performance analysis completed for skill {skill_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance for skill {skill_id}: {str(e)}")
            raise
            
    def _calculate_insights(self, metrics: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Calculate statistical insights from performance metrics"""
        if not metrics:
            return {}
            
        insights = {}
        
        # Extract metric values for analysis
        values = [m.value for m in metrics if hasattr(m, 'value') and m.value is not None]
        execution_times = [m.execution_time for m in metrics if hasattr(m, 'execution_time') and m.execution_time is not None]
        success_rates = [m.success_rate for m in metrics if hasattr(m, 'success_rate') and m.success_rate is not None]
        
        if values:
            insights['avg_performance'] = float(np.mean(values))
            insights['performance_std'] = float(np.std(values))
            insights['min_performance'] = float(np.min(values))
            insights['max_performance'] = float(np.max(values))
            
        if execution_times:
            insights['avg_execution_time'] = float(np.mean(execution_times))
            insights['execution_time_std'] = float(np.std(execution_times))
            
        if success_rates:
            insights['avg_success_rate'] = float(np.mean(success_rates))
            
        insights['total_executions'] = len(metrics)
        
        return insights
        
    def generate_insights(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """
        Generate detailed insights from analysis results.
        
        Args:
            analysis_result: AnalysisResult object containing metrics data
            
        Returns:
            Dictionary of detailed insights
        """
        insights = {}
        
        try:
            # Get performance trend
            metrics = analysis_result.metrics
            if metrics:
                values = [m.value for m in metrics if hasattr(m, 'value') and m.value is not None]
                if values:
                    insights['trend'] = self._determine_trend(values)
                    insights['volatility'] = float(np.std(values)) if len(values) > 1 else 0.0
                    
            insights['performance_stability'] = self._assess_stability(metrics)
            insights['recommendations'] = self._generate_recommendations(analysis_result)
            
            self.logger.info(f"Generated insights for skill {analysis_result.skill_id}")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {str(e)}")
            raise
            
    def _determine_trend(self, values: List[float]) -> str:
        """Determine performance trend from values"""
        if len(values) < 2:
            return "insufficient_data"
            
        # Calculate trend using linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"
            
    def _assess_stability(self, metrics: List[PerformanceMetrics]) -> str:
        """Assess the stability of skill performance"""
        if not metrics:
            return "unknown"
            
        values = [m.value for m in metrics if hasattr(m, 'value') and m.value is not None]
        if len(values) < 2:
            return "insufficient_data"
            
        std_dev = np.std(values)
        if std_dev < 0.1:
            return "stable"
        elif std_dev < 0.5:
            return "moderately_unstable"
        else:
            return "highly_unstable"
            
    def _generate_recommendations(self, analysis_result: AnalysisResult) -> List[str]:
        """Generate improvement recommendations based on analysis"""
        recommendations = []
        insights = analysis_result.insights
        
        if analysis_result.insights.get('trend') == 'declining':
            recommendations.append("Performance is declining - consider skill retraining")
            
        if analysis_result.insights.get('volatility', 0) > 0.5:
            recommendations.append("High performance variance detected - consider stabilization")
            
        if analysis_result.insights.get('performance_stability') == "highly_unstable":
            recommendations.append("Unstable performance - review skill implementation")
            
        return recommendations
        
    def visualize(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """
        Generate visualizations for the analysis results.
        
        Args:
            analysis_result: AnalysisResult object containing metrics data
            
        Returns:
            Dictionary containing matplotlib figure objects
        """
        visualizations = {}
        
        try:
            metrics = analysis_result.metrics
            if not metrics:
                return visualizations
                
            # Extract data for plotting
            timestamps = [m.timestamp for m in metrics]
            values = [m.value for m in metrics if hasattr(m, 'value') and m.value is not None]
            
            if not values:
                return visualizations
                
            # Create performance over time plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(timestamps, values, marker='o')
            ax.set_xlabel('Time')
            ax.set_ylabel('Performance Value')
            ax.set_title(f'Performance Trend for Skill {analysis_result.skill_id}')
            ax.grid(True)
            visualizations['performance_trend'] = fig
            plt.close(fig)
            
            # Create histogram of performance values
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(values, bins=20, alpha=0.7)
            ax.set_xlabel('Performance Value')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Performance Distribution for Skill {analysis_result.skill_id}')
            visualizations['performance_distribution'] = fig
            plt.close(fig)
            
            self.logger.info(f"Generated visualizations for skill {analysis_result.skill_id}")
            return visualizations
            
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")
            return {}