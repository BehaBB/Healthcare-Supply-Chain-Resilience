## 4-Prototyping/temperature-monitor/

### 4-Prototyping/temperature-monitor/sensor_processor.py
```python
"""
Temperature Sensor Data Processor
Adapted from meat export monitoring system for pharmaceutical use
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class PharmaceuticalTemperatureMonitor:
    """
    Monitors temperature for pharmaceutical products
    Adapted from meat export temperature control system
    """
    
    # Temperature requirements for different medication types
    MEDICATION_TEMPERATURE_RANGES = {
        'vaccines': {'min': 2.0, 'max': 8.0, 'critical_min': 0.0, 'critical_max': 10.0},
        'insulins': {'min': 2.0, 'max': 8.0, 'critical_min': 0.0, 'critical_max': 12.0},
        'biologics': {'min': -20.0, 'max': -15.0, 'critical_min': -25.0, 'critical_max': -10.0},
        'antibiotics': {'min': 15.0, 'max': 25.0, 'critical_min': 8.0, 'critical_max': 30.0}
    }
    
    def __init__(self):
        self.alert_history = []
        self.sensor_readings = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('TemperatureMonitor')
    
    async def process_sensor_reading(self, sensor_data: Dict) -> Dict:
        """
        Process temperature reading from IoT sensor
        Adapted from meat export monitoring with pharmaceutical parameters
        """
        try:
            medication_type = sensor_data.get('medication_type', 'vaccines')
            current_temp = sensor_data['temperature']
            sensor_id = sensor_data['sensor_id']
            
            # Get temperature requirements for this medication type
            temp_range = self.MEDICATION_TEMPERATURE_RANGES.get(
                medication_type, 
                self.MEDICATION_TEMPERATURE_RANGES['vaccines']
            )
            
            # Check temperature compliance
            compliance_status = self._check_temperature_compliance(
                current_temp, temp_range
            )
            
            # Store reading
            self.sensor_readings[sensor_id] = {
                'temperature': current_temp,
                'timestamp': datetime.now(),
                'status': compliance_status,
                'medication_type': medication_type
            }
            
            # Generate alert if needed
            if compliance_status in ['warning', 'critical']:
                await self._generate_alert(sensor_data, compliance_status, temp_range)
            
            return {
                'sensor_id': sensor_id,
                'temperature': current_temp,
                'status': compliance_status,
                'timestamp': datetime.now().isoformat(),
                'medication_type': medication_type
            }
            
        except Exception as e:
            self.logger.error(f"Error processing sensor reading: {e}")
            raise
    
    def _check_temperature_compliance(self, temperature: float, temp_range: Dict) -> str:
        """
        Check if temperature is within acceptable range
        Returns: 'normal', 'warning', or 'critical'
        """
        if temp_range['min'] <= temperature <= temp_range['max']:
            return 'normal'
        elif (temp_range['critical_min'] <= temperature < temp_range['min'] or 
              temp_range['max'] < temperature <= temp_range['critical_max']):
            return 'warning'
        else:
            return 'critical'
    
    async def _generate_alert(self, sensor_data: Dict, status: str, temp_range: Dict):
        """
        Generate temperature alert
        Enhanced from meat export system with pharmaceutical-specific messaging
        """
        alert = {
            'alert_id': f"temp_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'sensor_id': sensor_data['sensor_id'],
            'medication_type': sensor_data.get('medication_type', 'unknown'),
            'current_temperature': sensor_data['temperature'],
            'required_range': f"{temp_range['min']}°C - {temp_range['max']}°C",
            'status': status,
            'timestamp': datetime.now(),
            'location': sensor_data.get('location', 'unknown'),
            'batch_number': sensor_data.get('batch_number'),
            'priority': 'high' if status == 'critical' else 'medium'
        }
        
        self.alert_history.append(alert)
        
        # Log alert
        self.logger.warning(
            f"Temperature alert: {status.upper()} - "
            f"Sensor {sensor_data['sensor_id']} - "
            f"Temp: {sensor_data['temperature']}°C - "
            f"Medication: {sensor_data.get('medication_type', 'unknown')}"
        )
        
        # In production, this would send SMS/email/push notifications
        await self._notify_stakeholders(alert)
    
    async def _notify_stakeholders(self, alert: Dict):
        """
        Notify relevant stakeholders about temperature issues
        """
        # Mock implementation - in production would integrate with notification services
        stakeholders = ['pharmacy_manager', 'quality_control', 'logistics_coordinator']
        
        for stakeholder in stakeholders:
            self.logger.info(
                f"Notifying {stakeholder}: {alert['alert_id']} - "
                f"{alert['status'].upper()} temperature violation"
            )
    
    def get_temperature_stats(self, hours: int = 24) -> Dict:
        """
        Get temperature statistics for the specified period
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_readings = [
            reading for reading in self.sensor_readings.values()
            if reading['timestamp'] >= cutoff_time
        ]
        
        if not recent_readings:
            return {}
        
        temperatures = [r['temperature'] for r in recent_readings]
        statuses = [r['status'] for r in recent_readings]
        
        return {
            'total_readings': len(recent_readings),
            'average_temperature': sum(temperatures) / len(temperatures),
            'min_temperature': min(temperatures),
            'max_temperature': max(temperatures),
            'compliance_rate': (statuses.count('normal') / len(statuses)) * 100,
            'critical_alerts': statuses.count('critical'),
            'warning_alerts': statuses.count('warning')
        }

# Example usage and testing
async def main():
    """Example usage of the temperature monitor"""
    monitor = PharmaceuticalTemperatureMonitor()
    
    # Simulate sensor readings
    test_readings = [
        {
            'sensor_id': 'sensor_vaccine_001',
            'temperature': 5.2,
            'medication_type': 'vaccines',
            'location': 'Pharmacy Storage Unit A',
            'batch_number': 'BATCH-2024-VAC-001'
        },
        {
            'sensor_id': 'sensor_insulin_001', 
            'temperature': 12.5,  # This should trigger a warning
            'medication_type': 'insulins',
            'location': 'Delivery Vehicle 1',
            'batch_number': 'BATCH-2024-INS-001'
        },
        {
            'sensor_id': 'sensor_biologics_001',
            'temperature': -12.0,  # This should trigger critical
            'medication_type': 'biologics', 
            'location': 'Freezer Unit B',
            'batch_number': 'BATCH-2024-BIO-001'
        }
    ]
    
    # Process test readings
    for reading in test_readings:
        result = await monitor.process_sensor_reading(reading)
        print(f"Processed: {result}")
    
    # Get statistics
    stats = monitor.get_temperature_stats()
    print(f"\nTemperature Statistics: {stats}")

if __name__ == "__main__":
    asyncio.run(main())
  ```
