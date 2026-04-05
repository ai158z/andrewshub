import logging
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from datetime import datetime
from stop_skill_library.models import PerformanceMetrics
from stop_skill_library.reflection.performance_tracker import PerformanceTracker
from stop_skill_library.reflection.analysis import PerformanceAnalyzer


class ReflectionEngine:
    def __init__(self):
        self.performance_tracker = PerformanceTracker()
        self.performance_analyzer = PerformanceAnalyzer()
        self.logger = logging.getLogger(__name__)
        self.logger.info("ReflectionEngine initialized")
    
    def track_performance(self, skill_id: str, metrics: Dict[str, Any]) -> PerformanceMetrics:
        try:
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            if not isinstance(metrics, dict):
                raise ValueError("metrics must be a dictionary")
            
            # Create performance metrics object
            performance_metrics = PerformanceMetrics(
                skill_id=skill_id,
                timestamp=datetime.now(),
                execution_time=metrics.get('execution_time', 0),
                memory_usage=metrics.get('memory_usage', 0),
                accuracy=metrics.get('accuracy', 0.0),
                success_rate=metrics.get('success_rate', 0.0),
                error_count=metrics.get('error_count', 0),
                call_count=metrics.get('call_count', 0),
                metadata=metrics.get('metadata', {})
            )
            
            # Track the metrics
            self.performance_tracker.track(performance_metrics)
            
            self.logger.info(f"Tracked performance for skill {skill_id}")
            return performance_metrics
            
        except Exception as e:
            self.logger.error(f"Error tracking performance: {str(e)}")
            raise
    
    def analyze_performance(self, skill_id: str) -> Dict[str, Any]:
        <template>
        return insights
    
    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            if skill_id is not None:
                # Generate report for specific skill
                metrics = self.performance_tracker.get_metrics(skill_id)
                if not metrics:
                    return {"error": "No metrics found for analysis"}
                
                analysis = self.performance_analyzer.analyze(metrics)
                
                self.logger.info(f"Performance analysis completed for skill {skill_id}")
                return analysis
                
            except Exception as e:
                self.logger.error(f"Error analyzing performance: {str(e)}")
                raise ValueError(f"Failed to analyze performance: {str(e)}")
                raise
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise
    
    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            if skill_id is not None:
                # Generate report for specific skill
                metrics = self.performance_tracker.get_metrics(skill_id)
                if not metrics:
                    return {"error": "No metrics found for analysis"}
                
                analysis = self.performance_tracker.get_metrics(skill_id)
                if not analysis:
                    return {"error": "No metrics found for analysis"}
                
                analysis = self.performance_analyzer.analyze(metrics)
                
                self.logger.info(f"Performance analysis completed for skill {skill_id}")
                return analysis
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": metric.skill_id,
                    "report": report,
                    "analysis": analysis
                }
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": metric.skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                
                return {
                    "skill_id": metric.skill_id,
                    "report": report,
                    "analysis": analysis
                }
                
        except Exception as e:
            raise ValueError(f"Error generating report: {str(e)}")
            raise

    def track_performance(self, skill_id: str, metrics: Dict[str, Any]) -> PerformanceMetrics:
        try:
            # Validate inputs
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            if not isinstance(metrics, dict):
                raise ValueError("metrics must be a dictionary")
            
            # Create performance metrics object
            performance_metrics = PerformanceMetrics(
                skill_id=skill_id,
                timestamp=datetime.now(),
                execution_time=metrics.get('execution_time', 0),
                memory_usage=metrics.get('memory_usage', 0),
                accuracy=metrics.get('accuracy', 0.0),
                success_rate=metrics.get('success_rate', 0.0),
                error_count=metrics.get('error_count', 0),
                call_count=metrics.get('call_count', 0),
                metadata=metrics.get('metadata', {})
            )
            
            # Track the metrics
            self.performance_tracker.track(performance_metrics)
            
            self.logger.info(f"Tracked performance for skill {skill_id}")
            return performance_metrics
            
        except Exception as e:
            self.logger.error(f"Error tracking performance: {str(e)}")
            raise

    def analyze_performance(self, skill_id: str) -> PerformanceMetrics:
        try:
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            if not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            # Get metrics from tracker
            metrics = self.performance_tracker.get_metrics(skill_id)
            
            if not metrics:
                return {"error": "No metrics found for analysis"}
            
            # Perform analysis
            insights = self.performance_analyzer.analyze(metrics)
            
            self.logger.info(f"Performance analysis completed for skill {skill_id}")
            return insights
            
        except e:
            self.logger.error(f"Error analyzing performance: {str(e)}")
            raise ValueError("Failed to analyze performance: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                }
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def track_performance(self, skill_id: str, metrics: Dict[str, Any]) -> PerformanceMetrics:
        try:
            # Validate inputs
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            if not isinstance(metrics, dict):
                raise ValueError("metrics must be a dictionary")
            
            # Create performance metrics object
            performance_metrics = PerformanceMetrics(
                skill_id=skill_id,
                timestamp=datetime.now(),
                execution_time=metrics.get('execution_time', 0),
                memory_usage=metrics.get('memory_usage', 0),
                accuracy=metrics.get('accuracy', 0.0),
                success_rate=metrics.get('success_rate', 0.0),
                error_count=metrics.get('error_count', 0),
                call_count=metrics.get('call_count', 0),
                metadata=metrics.get('metadata', {})
            )
            
            # Track the metrics
            self.performance_tracker.track(performance_metrics)
            
            self.logger.info(f"Tracked performance for skill {skill_id}")
            return performance_metrics
            
        except Exception as e:
            self.logger.error(f"Error tracking performance: {str(e)}")
            raise

    def analyze_performance(self, skill_id: str) -> Dict[str, Any]:
        try:
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            # Get metrics from tracker
            metrics = self.performance_tracker.get_metrics(skill_id)
            
            if not metrics:
                return {"error": "No metrics found for analysis"}
            
            # Perform analysis
            insights = self.performance_analyzer.analyze(metrics)
            
            self.logger.info(f"Performance analysis completed for skill {skill tov} {skill_id}")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def track_performance(self, skill_id: str, metrics: Dict[str, Any]) -> PerformanceMetrics:
        try:
            # Validate inputs
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            if not isinstance(metrics, dict):
                raise ValueError("metrics must be a dictionary")
            
            # Create performance metrics object
            performance_metrics = PerformanceMetrics(
                skill_id=skill_id,
                timestamp=datetime.now(),
                execution_time=metrics.get('execution_time', 0),
                memory_usage=metrics.get('memory_usage', 0),
                accuracy=metrics.get('accuracy', 0.0),
                success_rate=metrics.get('success_rate', 0.0),
                error_count=metrics.get('error_count', 0),
                call_count=metrics.get('call_count', 0),
                metadata=metrics.get('metadata', {})
            )
            
            # Track the metrics
            self.performance_tracker.track(performance_metrics)
            
            self.logger.info(f"Tracked performance for skill {skill_id}")
            return performance_metrics
            
        except e:
            self.logger.error(f"Error tracking performance: {str(e)}")
            raise

    def analyze_performance(self, skill_id: str) -> Dict[str, Any]:
        try:
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            # Get metrics from tracker
            metrics = self.performance_tracker.get_metrics(skill_id)
            
            if not metrics:
                return {"error": "No metrics found for analysis"}
            
            # Perform analysis
            insights = self.performance_analyzer.analyze(metrics)
            
            self.logger.info("Performance analysis completed for skill {}".format(skill_id))
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def track_performance(self, skill_id: str, metrics: Dict[str, Any]) -> PerformanceMetrics:
        try:
            # Validate inputs
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            if not isinstance(metrics, dict):
                raise ValueError("metrics must be a dictionary")
            
            # Create performance metrics object
            performance_metrics = PerformanceMetrics(
                skill_id=skill_id,
                timestamp=datetime.now(),
                execution_time=metrics.get('execution_time', 0),
                memory_usage=metrics,
                accuracy=metrics,
                success_rate=metrics,
                error_count=metrics,
                call_count=metrics,
                metadata=metrics
            )
            
            # Track the metrics
            self.performance_tracker.track(performance_metrics)
            
            self.logger.info(f"Tracked performance for skill {skill_id}")
            return performance_metrics
            
        except Exception as e:
            self.logger.error(f"Error tracking performance: {str(e)}")
            raise

    def analyze_performance(self, skill_id: str) -> Dict[str, Any]:
        try:
            if not skill_id or not isinstance(skill_id, str):
                raise ValueError("skill_id must be a non-empty string")
            
            # Get metrics from tracker
            metrics = self.performance_tracker.get_metrics(skill_id)
            
            if not metrics:
                return {"error": "No metrics found for analysis"}
            
            # Perform analysis
            insights = self.performance_analyzer.analyze(metrics)
            
            self.logger.info(f"Performance analysis completed for skill {skill_id}")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all(}_metrics)
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                   
 "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Error generating report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self,RE>
        <</SYS
```
        self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Generate report for all skills
            all_metrics = self.performance_tracker.get_all_metrics()
            reports = []
            
            for metric in all_metrics:
                report = self.performance_tracker.generate_report([metric])
                analysis = self.performance_analyzer.generate_insights([metric])
                reports.append({
                    "skill_id": skill_id,
                    "report": report,
                    "analysis": analysis
                })
                
                return {
                    "summary": "Performance report for all skills",
                    "reports": reports
                }
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise ValueError(f"Failed to generate report: {str(e)}")
            raise

    def generate_report(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        try: