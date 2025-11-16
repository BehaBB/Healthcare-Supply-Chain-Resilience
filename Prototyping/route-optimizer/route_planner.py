"""
AI-Powered Route Optimizer for Pharmaceutical Deliveries
Adapted from meat export logistics with healthcare-specific constraints
"""

import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging
from dataclasses import dataclass
from math import radians, sin, cos, sqrt, atan2

@dataclass
class Pharmacy:
    id: str
    name: str
    latitude: float
    longitude: float
    priority: int  # 1-10, higher is more critical
    delivery_window: Tuple[datetime, datetime]

@dataclass
class RouteSegment:
    start_pharmacy: Pharmacy
    end_pharmacy: Pharmacy
    distance_km: float
    estimated_duration_min: int
    road_conditions: str
    weather_risk: float  # 0-1 scale

class PharmaceuticalRouteOptimizer:
    """
    Optimizes delivery routes for pharmaceutical shipments
    Enhanced from meat export logistics with medical emergency considerations
    """
    
    def __init__(self):
        self.setup_logging()
        self.road_conditions_weights = {
            'highway': 1.0,
            'paved_road': 1.2,
            'gravel_road': 1.5,
            'mountain_pass': 2.0,
            'winter_road': 1.8
        }
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('RouteOptimizer')
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        """
        R = 6371  # Earth radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def optimize_delivery_route(self, pharmacies: List[Pharmacy], 
                               vehicle_capacity: int,
                               current_weather: Dict) -> List[Pharmacy]:
        """
        Optimize delivery route using modified TSP with healthcare priorities
        """
        if not pharmacies:
            return []
        
        # Start from central depot (simplified - in production would be actual depot)
        depot = Pharmacy(
            id="depot",
            name="Central Distribution Center",
            latitude=52.0375,  # Ulan-Ude coordinates
            longitude=106.6522,
            priority=1,
            delivery_window=(datetime.now(), datetime.now() + timedelta(hours=8))
        )
        
        # Add emergency priority boost based on medication types
        prioritized_pharmacies = self._apply_emergency_priority(pharmacies)
        
        # Use nearest neighbor algorithm with priority weighting
        route = [depot]
        unvisited = prioritized_pharmacies.copy()
        
        while unvisited:
            current_location = route[-1]
            
            # Find next pharmacy considering distance and priority
            next_pharmacy = self._select_next_pharmacy(
                current_location, unvisited, current_weather
            )
            
            if next_pharmacy:
                route.append(next_pharmacy)
                unvisited.remove(next_pharmacy)
            else:
                break
        
        # Return to depot
        route.append(depot)
        
        self.logger.info(f"Optimized route with {len(route)} stops")
        return route
    
    def _apply_emergency_priority(self, pharmacies: List[Pharmacy]) -> List[Pharmacy]:
        """
        Apply emergency priority adjustments based on real-time data
        """
        # In production, this would integrate with PublicHealthOS
        # for epidemic data and emergency medication needs
        
        emergency_boosted = []
        for pharmacy in pharmacies:
            # Simulate emergency detection (e.g., disease outbreak in area)
            emergency_multiplier = self._detect_emergency_situation(pharmacy)
            
            # Create new pharmacy with adjusted priority
            boosted_pharmacy = Pharmacy(
                id=pharmacy.id,
                name=pharmacy.name,
                latitude=pharmacy.latitude,
                longitude=pharmacy.longitude,
                priority=min(10, pharmacy.priority * emergency_multiplier),
                delivery_window=pharmacy.delivery_window
            )
            emergency_boosted.append(boosted_pharmacy)
        
        # Sort by priority (highest first)
        return sorted(emergency_boosted, key=lambda x: x.priority, reverse=True)
    
    def _detect_emergency_situation(self, pharmacy: Pharmacy) -> float:
        """
        Detect if pharmacy is in emergency situation
        Returns multiplier for priority (1.0 = normal, up to 3.0 for emergencies)
        """
        # Mock implementation - in production would use real epidemic data
        emergency_zones = {
            'pharmacy_001': 2.5,  # High priority due to outbreak
            'pharmacy_005': 1.8,  # Medium priority
        }
        
        return emergency_zones.get(pharmacy.id, 1.0)
    
    def _select_next_pharmacy(self, current: Pharmacy, 
                            candidates: List[Pharmacy],
                            weather: Dict) -> Pharmacy:
        """
        Select next pharmacy based on multiple factors
        """
        best_score = float('-inf')
        best_pharmacy = None
        
        for pharmacy in candidates:
            score = self._calculate_pharmacy_score(current, pharmacy, weather)
            
            if score > best_score:
                best_score = score
                best_pharmacy = pharmacy
        
        return best_pharmacy
    
    def _calculate_pharmacy_score(self, current: Pharmacy, 
                                target: Pharmacy,
                                weather: Dict) -> float:
        """
        Calculate composite score for pharmacy selection
        """
        # Distance score (shorter is better)
        distance = self.calculate_distance(
            current.latitude, current.longitude,
            target.latitude, target.longitude
        )
        distance_score = 100 / (distance + 1)  # Avoid division by zero
        
        # Priority score (higher priority is better)
        priority_score = target.priority * 10
        
        # Weather impact score
        weather_impact = self._calculate_weather_impact(weather, target)
        weather_score = 50 * (1 - weather_impact)
        
        # Time window urgency
        time_urgency = self._calculate_time_urgency(target)
        
        total_score = distance_score + priority_score + weather_score + time_urgency
        
        return total_score
    
    def _calculate_weather_impact(self, weather: Dict, pharmacy: Pharmacy) -> float:
        """
        Calculate weather impact on route to pharmacy (0-1 scale)
        """
        # Mock implementation - in production would use real weather API
        base_risk = 0.1
        
        # Increase risk for mountain areas
        if pharmacy.latitude > 52.5:  # Northern/mountainous region
            base_risk += 0.3
        
        # Weather conditions
        if weather.get('condition') == 'snow':
            base_risk += 0.4
        elif weather.get('condition') == 'rain':
            base_risk += 0.2
        
        return min(base_risk, 1.0)
    
    def _calculate_time_urgency(self, pharmacy: Pharmacy) -> float:
        """
        Calculate urgency based on delivery window
        """
        now = datetime.now()
        window_start, window_end = pharmacy.delivery_window
        
        time_until_start = (window_start - now).total_seconds() / 3600  # hours
        
        if time_until_start <= 2:  # Urgent - within 2 hours
            return 30
        elif time_until_start <= 4:  # Soon - within 4 hours
            return 15
        else:
            return 5
    
    def generate_route_report(self, route: List[Pharmacy]) -> Dict:
        """
        Generate detailed route report with timing and risk assessment
        """
        total_distance = 0
        total_duration = 0
        segments = []
        
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            
            distance = self.calculate_distance(
                start.latitude, start.longitude,
                end.latitude, end.longitude
            )
            
            # Estimate duration considering road conditions
            base_speed = 60  # km/h
            road_condition_factor = self.road_conditions_weights.get('paved_road', 1.0)
            duration = (distance / base_speed) * road_condition_factor * 60  # minutes
            
            segment = RouteSegment(
                start_pharmacy=start,
                end_pharmacy=end,
                distance_km=round(distance, 2),
                estimated_duration_min=int(duration),
                road_conditions='paved_road',  # Simplified
                weather_risk=0.1
            )
            
            segments.append(segment)
            total_distance += distance
            total_duration += duration
        
        return {
            'route_id': f"route_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'total_distance_km': round(total_distance, 2),
            'total_duration_min': int(total_duration),
            'pharmacy_count': len(route) - 2,  # Exclude depot start and end
            'segments': segments,
            'estimated_fuel_consumption': round(total_distance * 0.12, 2),  # 12L/100km
            'generated_at': datetime.now().isoformat()
        }


# Example usage
def main():
    optimizer = PharmaceuticalRouteOptimizer()
    
    # Sample pharmacies in Buryatia region
    pharmacies = [
        Pharmacy(
            id="pharmacy_001",
            name="Лара Аптека Центральная",
            latitude=52.0375,
            longitude=106.6522,
            priority=8,
            delivery_window=(
                datetime.now() + timedelta(hours=1),
                datetime.now() + timedelta(hours=6)
            )
        ),
        Pharmacy(
            id="pharmacy_002", 
            name="Лара Аптека Курумкан",
            latitude=54.3000,
            longitude=110.3000,
            priority=6,
            delivery_window=(
                datetime.now() + timedelta(hours=2),
                datetime.now() + timedelta(hours=8)
            )
        ),
        Pharmacy(
            id="pharmacy_003",
            name="Лара Аптека Ока",
            latitude=52.5000, 
            longitude=110.1000,
            priority=9,  # High priority for emergency
            delivery_window=(
                datetime.now() + timedelta(hours=1),
                datetime.now() + timedelta(hours=4)
            )
        )
    ]
    
    current_weather = {
        'condition': 'snow',
        'temperature': -15,
        'wind_speed': 25
    }
    
    # Optimize route
    optimized_route = optimizer.optimize_delivery_route(
        pharmacies, vehicle_capacity=1000, current_weather=current_weather
    )
    
    # Generate report
    route_report = optimizer.generate_route_report(optimized_route)
    
    print("Optimized Route:")
    for i, pharmacy in enumerate(optimized_route):
        print(f"{i+1}. {pharmacy.name} (Priority: {pharmacy.priority})")
    
    print(f"\nRoute Report:")
    print(f"Total Distance: {route_report['total_distance_km']} km")
    print(f"Total Duration: {route_report['total_duration_min']} min")
    print(f"Pharmacies: {route_report['pharmacy_count']}")

if __name__ == "__main__":
    main()
