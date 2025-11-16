# API Documentation
## Healthcare Supply Chain Bridge

### Base Information
**Base URL**: `https://api.healthcare-supply.buryatia.ru/v1`  
**Authentication**: Bearer Token (JWT)  
**Rate Limit**: 1000 requests per hour per API key

### Authentication

#### Get Access Token
```http
POST /auth/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```
#### Response:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "def50200e9a7a7a7a7..."
}
```
### Temperature Monitoring API
#### Get Current Temperatures
```http
GET /temperature/current
Authorization: Bearer {token}
```
#### Response:

```json
{
  "sensors": [
    {
      "sensor_id": "sensor_vaccine_001",
      "temperature": 4.2,
      "humidity": 45.2,
      "status": "normal",
      "medication_type": "vaccines",
      "location": "Pharmacy Storage A",
      "last_reading": "2024-01-15T10:30:00Z"
    }
  ],
  "summary": {
    "total_sensors": 142,
    "normal_count": 138,
    "warning_count": 3,
    "critical_count": 1
  }
}
```
### Submit Temperature Reading
```http
POST /temperature/readings
Authorization: Bearer {token}
Content-Type: application/json

{
  "sensor_id": "sensor_insulin_001",
  "temperature": 5.2,
  "humidity": 48.7,
  "battery_level": 85,
  "location": {
    "latitude": 52.0375,
    "longitude": 106.6522
  },
  "timestamp": "2024-01-15T10:35:00Z"
}
```
### Logistics API
#### Optimize Delivery Route
```http
POST /routes/optimize
Authorization: Bearer {token}
Content-Type: application/json
{
  "pharmacies": [
    {
      "pharmacy_id": "pharmacy_001",
      "priority": 8,
      "delivery_window": {
        "start": "2024-01-15T14:00:00Z",
        "end": "2024-01-15T18:00:00Z"
      }
    }
  ],
  "vehicle_capacity": 1000,
  "current_weather": {
    "condition": "snow",
    "temperature": -15,
    "wind_speed": 25
  }
}
```
#### Response:

```json
{
  "route_id": "route_202401151030",
  "optimized_route": [
    {
      "sequence": 1,
      "pharmacy_id": "pharmacy_001",
      "estimated_arrival": "2024-01-15T14:30:00Z",
      "estimated_departure": "2024-01-15T14:45:00Z"
    }
  ],
  "total_distance_km": 245.8,
  "total_duration_min": 285,
  "fuel_estimate_liters": 29.5
}
```
#### Track Delivery
```http
GET /deliveries/{delivery_id}/tracking
Authorization: Bearer {token}
```
#### Response:

```json
{
  "delivery_id": "delivery_20240115001",
  "status": "in_transit",
  "current_location": {
    "latitude": 52.1234,
    "longitude": 106.7890,
    "timestamp": "2024-01-15T11:30:00Z"
  },
  "next_stop": {
    "pharmacy_id": "pharmacy_002",
    "estimated_arrival": "2024-01-15T12:15:00Z",
    "distance_remaining_km": 25.3
  },
  "temperature_readings": [
    {
      "timestamp": "2024-01-15T11:25:00Z",
      "temperature": 4.8,
      "status": "normal"
    }
  ]
}
```
### Compliance API
#### Validate Shipment Compliance
```http
POST /compliance/validate
Authorization: Bearer {token}
Content-Type: application/json

{
  "medications": [
    {
      "medication_id": "med_001",
      "name": "COVID-19 Vaccine",
      "manufacturer": "PharmStandard",
      "batch_number": "BATCH-VAC-2024-001",
      "expiry_date": "2024-12-31",
      "temperature_requirements": {
        "min": 2,
        "max": 8
      }
    }
  ],
  "destination_country": "russia"
}
```
#### Response:

```json
{
  "is_compliant": true,
  "validation_errors": [],
  "required_documents": [
    "certificate_of_analysis",
    "customs_declaration",
    "health_certificate"
  ],
  "temperature_compliance": true,
  "regulatory_checks": {
    "gmp": {"passed": true, "errors": []},
    "import_export": {"passed": true, "errors": []}
  }
}
```
#### Generate Compliance Document
```http
POST /compliance/documents/generate
Authorization: Bearer {token}
Content-Type: application/json

{
  "document_type": "certificate_of_analysis",
  "shipment_data": {
    "medications": [
      {
        "name": "COVID-19 Vaccine",
        "batch_number": "BATCH-VAC-2024-001",
        "manufacturer": "PharmStandard"
      }
    ],
    "destination_pharmacy": "Lara Pharmacy Kurumkan"
  }
}
```
#### Response:

```json
{
  "document_id": "COA-20240115-103000",
  "document_type": "certificate_of_analysis",
  "content": {
    "issuing_laboratory": "Quality Control Lab Buryatia",
    "test_results": {
      "purity": "99.8%",
      "potency": "Within specification"
    },
    "approval_signature": "Dr. Ivan Petrov"
  },
  "status": "generated",
  "generated_at": "2024-01-15T10:30:00Z"
}
```
### Inventory API
#### Get Pharmacy Inventory
```http
GET /inventory/pharmacies/{pharmacy_id}
Authorization: Bearer {token}
```
#### Response:

```json
{
  "pharmacy_id": "pharmacy_001",
  "inventory": [
    {
      "medication_id": "med_001",
      "name": "COVID-19 Vaccine",
      "batch_number": "BATCH-VAC-2024-001",
      "quantity": 450,
      "expiry_date": "2024-12-31",
      "storage_zone": "vaccines",
      "current_temperature": 4.2,
      "temperature_status": "normal"
    }
  ],
  "summary": {
    "total_items": 45,
    "low_stock_items": 3,
    "expiring_soon": 2
  }
}
```
#### Update Inventory
```http
POST /inventory/update
Authorization: Bearer {token}
Content-Type: application/json

{
  "pharmacy_id": "pharmacy_001",
  "updates": [
    {
      "medication_id": "med_001",
      "batch_number": "BATCH-VAC-2024-001",
      "quantity_change": -50,
      "reason": "delivery_shipment"
    }
  ]
}
```
### Analytics API
#### Get Performance Metrics
```http
GET /analytics/performance?start_date=2024-01-01&end_date=2024-01-15
Authorization: Bearer {token}
```
#### Response:

```json
{
  "temperature_compliance": 96.8,
  "delivery_efficiency": 94.2,
  "system_utilization": 88.7,
  "cost_savings": 237000,
  "trends": {
    "temperature_compliance_trend": "+0.7%",
    "delivery_efficiency_trend": "+0.7%"
  }
}
```
#### Get KPI Dashboard
```http
GET /analytics/kpi-dashboard
Authorization: Bearer {token}
```
### Error Handling
#### Common HTTP Status Codes
| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input parameters |
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |
#### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "temperature",
      "issue": "Must be between -50 and 50"
    },
    "request_id": "req_123456789"
  }
}
```
### Rate Limiting
#### Headers
X-RateLimit-Limit: Request limit (1000)

X-RateLimit-Remaining: Remaining requests

X-RateLimit-Reset: Reset time (Unix timestamp)

#### Limits by Endpoint
| Endpoint | Limit | Window |
|----------|-------|--------|
| Temperature readings | 100 | 1 minute |
| Route optimization | 50 | 1 hour |
| Document generation | 200 | 1 hour |
| General endpoints | 1000 | 1 hour |
#### Webhooks
#### Available Webhooks
#### Temperature Alerts:

```http
POST /webhooks/temperature-alerts
Content-Type: application/json

{
  "alert_id": "alert_202401151030",
  "sensor_id": "sensor_vaccine_001",
  "temperature": 9.2,
  "threshold": 8.0,
  "status": "warning",
  "timestamp": "2024-01-15T10:30:00Z"
}
```
#### Delivery Updates:

```http
POST /webhooks/delivery-updates
Content-Type: application/json

{
  "delivery_id": "delivery_20240115001",
  "status": "delivered",
  "timestamp": "2024-01-15T12:15:00Z",
  "location": {
    "latitude": 52.1234,
    "longitude": 106.7890
  }
}
```
### SDK Examples
#### Python SDK
```python
from healthcare_supply_sdk import HealthcareSupplyClient

client = HealthcareSupplyClient(
    base_url="https://api.healthcare-supply.buryatia.ru/v1",
    api_key="your_api_key"
)
```
# Get current temperatures
temperatures = client.temperature.get_current()

# Optimize delivery route
route = client.routes.optimize(route_request)

# Generate compliance document
document = client.compliance.generate_document(document_request)
JavaScript SDK
javascript
import { HealthcareSupplyClient } from 'healthcare-supply-sdk';

const client = new HealthcareSupplyClient({
  baseUrl: 'https://api.healthcare-supply.buryatia.ru/v1',
  apiKey: 'your_api_key'
});

// Get performance metrics
const metrics = await client.analytics.getPerformance();
Changelog
Version 1.1 
Added predictive maintenance endpoints

Enhanced error handling with detailed error codes

Improved documentation with SDK examples

Version 1.0 
Initial API release

Temperature monitoring endpoints

Logistics and route optimization

Compliance validation and document generation

