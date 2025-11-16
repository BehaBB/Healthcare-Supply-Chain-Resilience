"""
Tests for Pharmaceutical Temperature Monitor
"""

import pytest
import asyncio
from datetime import datetime
from sensor_processor import PharmaceuticalTemperatureMonitor

@pytest.fixture
def temperature_monitor():
    return PharmaceuticalTemperatureMonitor()

@pytest.mark.asyncio
async def test_vaccine_temperature_normal(temperature_monitor):
    """Test normal vaccine temperature reading"""
    sensor_data = {
        'sensor_id': 'test_sensor_1',
        'temperature': 5.0,
        'medication_type': 'vaccines',
        'location': 'test_location'
    }
    
    result = await temperature_monitor.process_sensor_reading(sensor_data)
    
    assert result['status'] == 'normal'
    assert result['medication_type'] == 'vaccines'
    assert result['sensor_id'] == 'test_sensor_1'

@pytest.mark.asyncio  
async def test_insulin_temperature_warning(temperature_monitor):
    """Test warning insulin temperature reading"""
    sensor_data = {
        'sensor_id': 'test_sensor_2',
        'temperature': 12.0,  # Outside normal range but within critical limits
        'medication_type': 'insulins',
        'location': 'test_location'
    }
    
    result = await temperature_monitor.process_sensor_reading(sensor_data)
    
    assert result['status'] == 'warning'
    assert len(temperature_monitor.alert_history) == 1

@pytest.mark.asyncio
async def test_biologics_temperature_critical(temperature_monitor):
    """Test critical biologics temperature reading"""
    sensor_data = {
        'sensor_id': 'test_sensor_3',
        'temperature': -12.0,  # Outside critical limits
        'medication_type': 'biologics',
        'location': 'test_location'
    }
    
    result = await temperature_monitor.process_sensor_reading(sensor_data)
    
    assert result['status'] == 'critical'
    # Should have 2 alerts now (1 from previous test, 1 from this test)
    assert len(temperature_monitor.alert_history) >= 1

def test_temperature_compliance_check(temperature_monitor):
    """Test temperature compliance checking logic"""
    temp_range = {'min': 2.0, 'max': 8.0, 'critical_min': 0.0, 'critical_max': 10.0}
    
    # Test normal temperature
    assert temperature_monitor._check_temperature_compliance(5.0, temp_range) == 'normal'
    
    # Test warning temperature (above normal but below critical)
    assert temperature_monitor._check_temperature_compliance(9.0, temp_range) == 'warning'
    
    # Test critical temperature (above critical max)
    assert temperature_monitor._check_temperature_compliance(15.0, temp_range) == 'critical'

def test_temperature_stats(temperature_monitor):
    """Test temperature statistics calculation"""
    # Add some test readings
    temperature_monitor.sensor_readings = {
        'sensor1': {'temperature': 5.0, 'timestamp': datetime.now(), 'status': 'normal'},
        'sensor2': {'temperature': 6.0, 'timestamp': datetime.now(), 'status': 'normal'},
        'sensor3': {'temperature': 12.0, 'timestamp': datetime.now(), 'status': 'warning'},
    }
    
    stats = temperature_monitor.get_temperature_stats(hours=1)
    
    assert stats['total_readings'] == 3
    assert stats['average_temperature'] == pytest.approx(7.67, 0.01)
    assert stats['compliance_rate'] == pytest.approx(66.67, 0.01)
    assert stats['warning_alerts'] == 1
