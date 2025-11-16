"""
Performance Analyzer
Analyzes system performance and generates insights
Adapted from meat export analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging
import json

class PerformanceAnalyzer:
    """
    Analyzes performance of healthcare supply chain system
    Enhanced from meat export performance analytics
    """
    
    def __init__(self):
        self.setup_logging()
        self.performance_benchmarks = {
            'temperature_compliance': {'excellent': 99.0, 'good': 95.0, 'poor': 90.0},
            'delivery_efficiency': {'excellent': 95.0, 'good': 90.0, 'poor': 80.0},
            'system_uptime': {'excellent': 99.5, 'good': 99.0, 'poor': 98.0},
            'cost_savings': {'excellent': 80.0, 'good': 70.0, 'poor': 50.0}
        }
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('PerformanceAnalyzer')
    
    def analyze_system_performance(self, metrics_data: Dict) -> Dict:
        """
        Analyze overall system performance
        """
        analysis_results = {
            'analysis_date': datetime.now().isoformat(),
            'overall_score': 0,
            'category_scores': {},
            'recommendations': [],
            'trend_analysis': {}
        }
        
        # Calculate category scores
        for category, metrics in metrics_data.items():
            category_score = self._calculate_category_score(category, metrics)
            analysis_results['category_scores'][category] = category_score
        
        # Calculate overall score
        analysis_results['overall_score'] = self._calculate_overall_score(
            analysis_results['category_scores']
        )
        
        # Generate recommendations
        analysis_results['recommendations'] = self._generate_recommendations(
            analysis_results['category_scores']
        )
        
        # Trend analysis
        analysis_results['trend_analysis'] = self._analyze_trends(metrics_data)
        
        self.logger.info(f"Performance analysis completed. Overall score: {analysis_results['overall_score']}")
        return analysis_results
    
    def _calculate_category_score(self, category: str, metrics: Dict) -> Dict:
        """Calculate score for a specific category"""
        if category == 'temperature_compliance':
            return self._analyze_temperature_compliance(metrics)
        elif category == 'delivery_efficiency':
            return self._analyze_delivery_efficiency(metrics)
        elif category == 'system_uptime':
            return self._analyze_system_uptime(metrics)
        elif category == 'cost_savings':
            return self._analyze_cost_savings(metrics)
        else:
            return {'score': 0, 'status': 'unknown', 'details': {}}
    
    def _analyze_temperature_compliance(self, metrics: Dict) -> Dict:
        """Analyze temperature compliance performance"""
        compliance_rate = metrics.get('compliance_rate', 0)
        benchmarks = self.performance_benchmarks['temperature_compliance']
        
        score = self._calculate_performance_score(compliance_rate, benchmarks)
        
        return {
            'score': score,
            'status': self._get_performance_status(compliance_rate, benchmarks),
            'details': {
                'compliance_rate': compliance_rate,
                'violations_count': metrics.get('violations_count', 0),
                'average_response_time': metrics.get('average_response_time', 0),
                'improvement_suggestions': self._get_temperature_improvements(metrics)
            }
        }
    
    def _analyze_delivery_efficiency(self, metrics: Dict) -> Dict:
        """Analyze delivery efficiency performance"""
        efficiency_rate = metrics.get('on_time_rate', 0)
        benchmarks = self.performance_benchmarks['delivery_efficiency']
        
        score = self._calculate_performance_score(efficiency_rate, benchmarks)
        
        return {
            'score': score,
            'status': self._get_performance_status(efficiency_rate, benchmarks),
            'details': {
                'on_time_rate': efficiency_rate,
                'average_delivery_time': metrics.get('average_delivery_time', 0),
                'route_optimization_rate': metrics.get('route_optimization_rate', 0),
                'improvement_suggestions': self._get_delivery_improvements(metrics)
            }
        }
    
    def _analyze_system_uptime(self, metrics: Dict) -> Dict:
        """Analyze system uptime performance"""
        uptime_rate = metrics.get('uptime_percentage', 0)
        benchmarks = self.performance_benchmarks['system_uptime']
        
        score = self._calculate_performance_score(uptime_rate, benchmarks)
        
        return {
            'score': score,
            'status': self._get_performance_status(uptime_rate, benchmarks),
            'details': {
                'uptime_percentage': uptime_rate,
                'downtime_incidents': metrics.get('downtime_incidents', 0),
                'average_recovery_time': metrics.get('average_recovery_time', 0),
                'improvement_suggestions': self._get_uptime_improvements(metrics)
            }
        }
    
    def _analyze_cost_savings(self, metrics: Dict) -> Dict:
        """Analyze cost savings performance"""
        savings_rate = metrics.get('savings_percentage', 0)
        benchmarks = self.performance_benchmarks['cost_savings']
        
        score = self._calculate_performance_score(savings_rate, benchmarks)
        
        return {
            'score': score,
            'status': self._get_performance_status(savings_rate, benchmarks),
            'details': {
                'savings_percentage': savings_rate,
                'monthly_savings_amount': metrics.get('monthly_savings_amount', 0),
                'roi_percentage': metrics.get('roi_percentage', 0),
                'improvement_suggestions': self._get_cost_improvements(metrics)
            }
        }
    
    def _calculate_performance_score(self, value: float, benchmarks: Dict) -> float:
        """Calculate performance score (0-100)"""
        if value >= benchmarks['excellent']:
            return 100.0
        elif value >= benchmarks['good']:
            return 80.0 + ((value - benchmarks['good']) / (benchmarks['excellent'] - benchmarks['good'])) * 20.0
        elif value >= benchmarks['poor']:
            return 60.0 + ((value - benchmarks['poor']) / (benchmarks['good'] - benchmarks['poor'])) * 20.0
        else:
            return (value / benchmarks['poor']) * 60.0
    
    def _get_performance_status(self, value: float, benchmarks: Dict) -> str:
        """Get performance status based on benchmarks"""
        if value >= benchmarks['excellent']:
            return 'excellent'
        elif value >= benchmarks['good']:
            return 'good'
        elif value >= benchmarks['poor']:
            return 'fair'
        else:
            return 'poor'
    
    def _get_temperature_improvements(self, metrics: Dict) -> List[str]:
        """Get improvement suggestions for temperature compliance"""
        suggestions = []
        
        if metrics.get('compliance_rate', 0) < 95.0:
            suggestions.append("Increase sensor calibration frequency")
            suggestions.append("Implement redundant monitoring systems")
        
        if metrics.get('average_response_time', 0) > 10:
            suggestions.append("Optimize alert escalation protocols")
            suggestions.append("Train staff on faster response procedures")
        
        return suggestions
    
    def _get_delivery_improvements(self, metrics: Dict) -> List[str]:
        """Get improvement suggestions for delivery efficiency"""
        suggestions = []
        
        if metrics.get('on_time_rate', 0) < 90.0:
            suggestions.append("Improve route optimization algorithms")
            suggestions.append("Add real-time traffic monitoring")
        
        if metrics.get('route_optimization_rate', 0) < 85.0:
            suggestions.append("Enhance weather prediction integration")
            suggestions.append("Optimize vehicle capacity utilization")
        
        return suggestions
    
    def _get_uptime_improvements(self, metrics: Dict) -> List[str]:
        """Get improvement suggestions for system uptime"""
        suggestions = []
        
        if metrics.get('uptime_percentage', 0) < 99.0:
            suggestions.append("Implement redundant server infrastructure")
            suggestions.append("Improve monitoring and alerting systems")
        
        if metrics.get('average_recovery_time', 0) > 30:
            suggestions.append("Develop faster recovery procedures")
            suggestions.append("Create comprehensive disaster recovery plan")
        
        return suggestions
    
    def _get_cost_improvements(self, metrics: Dict) -> List[str]:
        """Get improvement suggestions for cost savings"""
        suggestions = []
        
        if metrics.get('savings_percentage', 0) < 70.0:
            suggestions.append("Optimize inventory management further")
            suggestions.append("Reduce medication spoilage through better monitoring")
        
        return suggestions
    
    def _calculate_overall_score(self, category_scores: Dict) -> float:
        """Calculate overall performance score"""
        if not category_scores:
            return 0.0
        
        total_score = sum(score['score'] for score in category_scores.values())
        return total_score / len(category_scores)
    
    def _generate_recommendations(self, category_scores: Dict) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        for category, score_data in category_scores.items():
            if score_data['status'] in ['fair', 'poor']:
                recommendations.extend(score_data['details']['improvement_suggestions'])
        
        # Add general recommendations if overall score is low
        overall_score = self._calculate_overall_score(category_scores)
        if overall_score < 70.0:
            recommendations.append("Conduct comprehensive system performance review")
            recommendations.append("Implement continuous improvement program")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _analyze_trends(self, metrics_data: Dict) -> Dict:
        """Analyze performance trends"""
        # This would typically compare current metrics with historical data
        # For demo purposes, we'll generate some sample trend analysis
        
        return {
            'temperature_trend': 'improving',
            'delivery_trend': 'stable',
            'uptime_trend': 'improving',
            'cost_trend': 'improving',
            'overall_trend': 'positive'
        }
    
    def generate_performance_report(self, analysis_results: Dict) -> str:
        """
        Generate human-readable performance report
        """
        report_lines = []
        
        report_lines.append("HEALTHCARE SUPPLY CHAIN PERFORMANCE REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Report Date: {analysis_results['analysis_date']}")
        report_lines.append(f"Overall Performance Score: {analysis_results['overall_score']:.1f}/100")
        report_lines.append("")
        
        # Category scores
        report_lines.append("CATEGORY PERFORMANCE:")
        report_lines.append("-" * 30)
        for category, score_data in analysis_results['category_scores'].items():
            report_lines.append(
                f"{category.replace('_', ' ').title()}: "
                f"{score_data['score']:.1f}/100 ({score_data['status']})"
            )
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS FOR IMPROVEMENT:")
        report_lines.append("-" * 35)
        for i, recommendation in enumerate(analysis_results['recommendations'], 1):
            report_lines.append(f"{i}. {recommendation}")
        
        return "\n".join(report_lines)


# Example usage
def main():
    analyzer = PerformanceAnalyzer()
    
    # Sample performance metrics
    sample_metrics = {
        'temperature_compliance': {
            'compliance_rate': 96.8,
            'violations_count': 12,
            'average_response_time': 8.5
        },
        'delivery_efficiency': {
            'on_time_rate': 94.2,
            'average_delivery_time': 3.2,
            'route_optimization_rate': 88.7
        },
        'system_uptime': {
            'uptime_percentage': 99.7,
            'downtime_incidents': 2,
            'average_recovery_time': 15.0
        },
        'cost_savings': {
            'savings_percentage': 73.0,
            'monthly_savings_amount': 237000,
            'roi_percentage': 925.0
        }
    }
    
    # Analyze performance
    analysis = analyzer.analyze_system_performance(sample_metrics)
    
    print("Performance Analysis Results:")
    print(f"Overall Score: {analysis['overall_score']:.1f}/100")
    
    for category, score_data in analysis['category_scores'].items():
        print(f"{category}: {score_data['score']:.1f}/100 ({score_data['status']})")
    
    # Generate report
    report = analyzer.generate_performance_report(analysis)
    print("\n" + report)

if __name__ == "__main__":
    main()
