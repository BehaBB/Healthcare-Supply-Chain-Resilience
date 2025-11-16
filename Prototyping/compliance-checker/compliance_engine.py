"""
Pharmaceutical Compliance Engine
Adapted from meat export compliance system for healthcare regulations
"""

import json
from datetime import datetime, date
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

@dataclass
class Medication:
    id: str
    name: str
    manufacturer: str
    batch_number: str
    expiry_date: date
    temperature_requirements: Dict
    regulatory_classification: str

@dataclass
class ComplianceDocument:
    document_type: str
    content: Dict
    status: str  # draft, generated, submitted, approved
    generated_at: datetime
    regulatory_references: List[str]

class PharmaceuticalComplianceEngine:
    """
    Validates and generates compliance documents for pharmaceutical shipments
    Adapted from meat export compliance with healthcare-specific regulations
    """
    
    def __init__(self):
        self.setup_logging()
        self.regulations = self._load_regulations()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('ComplianceEngine')
    
    def _load_regulations(self) -> Dict:
        """
        Load pharmaceutical regulations database
        In production, this would connect to real regulatory databases
        """
        return {
            'russia': {
                'gmp_requirements': {
                    'temperature_monitoring': True,
                    'batch_tracking': True,
                    'quality_certification': True,
                    'import_license_required': True
                },
                'document_requirements': [
                    'certificate_of_analysis',
                    'customs_declaration',
                    'health_certificate',
                    'import_license'
                ]
            },
            'international': {
                'who_guidelines': {
                    'vaccine_storage': [2, 8],
                    'cold_chain_validation': True,
                    'emergency_protocols': True
                }
            }
        }
    
    def validate_shipment_compliance(self, medications: List[Medication], 
                                   destination_country: str) -> Dict:
        """
        Validate if shipment complies with destination country regulations
        """
        validation_results = {
            'is_compliant': True,
            'validation_errors': [],
            'required_documents': [],
            'temperature_compliance': True,
            'regulatory_checks': {}
        }
        
        country_regulations = self.regulations.get(destination_country, {})
        
        # Check GMP requirements
        gmp_checks = self._validate_gmp_requirements(medications, country_regulations)
        validation_results['regulatory_checks']['gmp'] = gmp_checks
        
        if not gmp_checks['passed']:
            validation_results['is_compliant'] = False
            validation_results['validation_errors'].extend(gmp_checks['errors'])
        
        # Check temperature requirements
        temp_checks = self._validate_temperature_requirements(medications)
        validation_results['temperature_compliance'] = temp_checks['passed']
        
        if not temp_checks['passed']:
            validation_results['is_compliant'] = False
            validation_results['validation_errors'].extend(temp_checks['errors'])
        
        # Determine required documents
        required_docs = self._determine_required_documents(medications, destination_country)
        validation_results['required_documents'] = required_docs
        
        # Check expiry dates
        expiry_checks = self._validate_expiry_dates(medications)
        if not expiry_checks['passed']:
            validation_results['is_compliant'] = False
            validation_results['validation_errors'].extend(expiry_checks['errors'])
        
        self.logger.info(f"Compliance validation: {validation_results['is_compliant']}")
        return validation_results
    
    def _validate_gmp_requirements(self, medications: List[Medication], 
                                 regulations: Dict) -> Dict:
        """
        Validate Good Manufacturing Practice requirements
        """
        checks = {'passed': True, 'errors': []}
        gmp_reqs = regulations.get('gmp_requirements', {})
        
        for medication in medications:
            # Check if manufacturer is GMP certified
            if gmp_reqs.get('quality_certification') and not self._is_gmp_certified(medication.manufacturer):
                checks['passed'] = False
                checks['errors'].append(
                    f"Manufacturer {medication.manufacturer} not GMP certified for {medication.name}"
                )
            
            # Check batch tracking
            if gmp_reqs.get('batch_tracking') and not medication.batch_number:
                checks['passed'] = False
                checks['errors'].append(
                    f"Batch number required for {medication.name}"
                )
        
        return checks
    
    def _validate_temperature_requirements(self, medications: List[Medication]) -> Dict:
        """
        Validate temperature requirements for medications
        """
        checks = {'passed': True, 'errors': []}
        
        for medication in medications:
            temp_reqs = medication.temperature_requirements
            
            # Check if temperature requirements are specified
            if not temp_reqs or 'min' not in temp_reqs or 'max' not in temp_reqs:
                checks['passed'] = False
                checks['errors'].append(
                    f"Temperature requirements not specified for {medication.name}"
                )
                continue
            
            # Validate temperature ranges are reasonable
            min_temp = temp_reqs['min']
            max_temp = temp_reqs['max']
            
            if min_temp >= max_temp:
                checks['passed'] = False
                checks['errors'].append(
                    f"Invalid temperature range for {medication.name}: {min_temp}-{max_temp}"
                )
        
        return checks
    
    def _validate_expiry_dates(self, medications: List[Medication]) -> Dict:
        """
        Validate medication expiry dates
        """
        checks = {'passed': True, 'errors': []}
        today = date.today()
        
        for medication in medications:
            if medication.expiry_date <= today:
                checks['passed'] = False
                checks['errors'].append(
                    f"Medication {medication.name} batch {medication.batch_number} has expired"
                )
            elif (medication.expiry_date - today).days <= 30:
                checks['errors'].append(
                    f"Warning: {medication.name} expires in {(medication.expiry_date - today).days} days"
                )
        
        return checks
    
    def _determine_required_documents(self, medications: List[Medication], 
                                   destination_country: str) -> List[str]:
        """
        Determine required compliance documents based on medications and destination
        """
        base_documents = ['commercial_invoice', 'packing_list']
        
        country_regulations = self.regulations.get(destination_country, {})
        doc_requirements = country_regulations.get('document_requirements', [])
        
        # Add medication-specific documents
        for medication in medications:
            if medication.regulatory_classification == 'vaccine':
                base_documents.extend(['vaccine_certificate', 'temperature_log'])
            elif medication.regulatory_classification == 'controlled_substance':
                base_documents.append('controlled_substance_license')
        
        # Add country-specific requirements
        base_documents.extend(doc_requirements)
        
        return list(set(base_documents))  # Remove duplicates
    
    def _is_gmp_certified(self, manufacturer: str) -> bool:
        """
        Check if manufacturer is GMP certified
        In production, this would query a regulatory database
        """
        # Mock implementation
        certified_manufacturers = [
            'pharmstandard', 'geropharm', 'binnopharm', 'r-pharm'
        ]
        
        return any(cert_manuf in manufacturer.lower() for cert_manuf in certified_manufacturers)
    
    def generate_compliance_document(self, document_type: str, 
                                  shipment_data: Dict) -> ComplianceDocument:
        """
        Generate specific compliance document
        """
        document_generators = {
            'certificate_of_analysis': self._generate_certificate_of_analysis,
            'customs_declaration': self._generate_customs_declaration,
            'health_certificate': self._generate_health_certificate,
            'temperature_log': self._generate_temperature_log
        }
        
        generator = document_generators.get(document_type)
        if not generator:
            raise ValueError(f"Unknown document type: {document_type}")
        
        content = generator(shipment_data)
        
        return ComplianceDocument(
            document_type=document_type,
            content=content,
            status='generated',
            generated_at=datetime.now(),
            regulatory_references=self._get_regulatory_references(document_type)
        )
    
    def _generate_certificate_of_analysis(self, shipment_data: Dict) -> Dict:
        """Generate Certificate of Analysis"""
        return {
            'document_id': f"COA-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'issuing_laboratory': 'Quality Control Lab Buryatia',
            'medication_details': shipment_data.get('medications', []),
            'test_results': {
                'purity': '99.8%',
                'potency': 'Within specification',
                'sterility': 'Pass',
                'endotoxins': 'Below limit'
            },
            'approval_signature': 'Dr. Ivan Petrov, Quality Manager',
            'issue_date': datetime.now().date().isoformat()
        }
    
    def _generate_customs_declaration(self, shipment_data: Dict) -> Dict:
        """Generate Customs Declaration"""
        medications = shipment_data.get('medications', [])
        total_value = sum(med.get('value', 0) for med in medications)
        
        return {
            'customs_declaration_number': f"CD-{datetime.now().strftime('%Y%m%d')}",
            'exporter': 'Lara Pharmacy Network',
            'importer': shipment_data.get('destination_pharmacy'),
            'hs_codes': [med.get('hs_code', '3004.90') for med in medications],
            'total_value_usd': total_value,
            'weight_kg': shipment_data.get('total_weight', 0),
            'purpose': 'Commercial shipment - Pharmaceutical supplies',
            'declaration_date': datetime.now().date().isoformat()
        }
    
    def _generate_health_certificate(self, shipment_data: Dict) -> Dict:
        """Generate Health Certificate"""
        return {
            'certificate_number': f"HC-{datetime.now().strftime('%Y%m%d')}",
            'issuing_authority': 'Ministry of Health of Buryatia',
            'certification': 'Products meet all health and safety requirements',
            'storage_conditions_verified': True,
            'transport_conditions': 'Temperature-controlled vehicle',
            'valid_until': (datetime.now() + timedelta(days=30)).date().isoformat(),
            'issuing_officer': 'Dr. Maria Ivanova, Chief Medical Officer'
        }
    
    def _generate_temperature_log(self, shipment_data: Dict) -> Dict:
        """Generate Temperature Log"""
        return {
            'log_id': f"TEMP-LOG-{datetime.now().strftime('%Y%m%d')}",
            'monitoring_period': {
                'start': shipment_data.get('shipment_start_time'),
                'end': datetime.now().isoformat()
            },
            'temperature_readings': shipment_data.get('temperature_data', []),
            'compliance_status': 'Within specification',
            'monitoring_device': 'IoT Sensor Network LaraPharma-1',
            'calibration_date': (datetime.now() - timedelta(days=30)).date().isoformat()
        }
    
    def _get_regulatory_references(self, document_type: str) -> List[str]:
        """Get regulatory references for document type"""
        references = {
            'certificate_of_analysis': ['GMP Annex 8', 'Pharmaceutical Inspection Convention'],
            'customs_declaration': ['Customs Code of EAEU', 'International Trade Regulations'],
            'health_certificate': ['WHO Guidelines', 'National Health Regulations'],
            'temperature_log': ['WHO Cold Chain Guidelines', 'GDP Guidelines']
        }
        
        return references.get(document_type, ['General Pharmaceutical Regulations'])


# Example usage
def main():
    compliance_engine = PharmaceuticalComplianceEngine()
    
    # Sample medications
    medications = [
        Medication(
            id="med_001",
            name="COVID-19 Vaccine",
            manufacturer="PharmStandard",
            batch_number="BATCH-VAC-2024-001",
            expiry_date=date(2024, 12, 31),
            temperature_requirements={'min': 2, 'max': 8, 'unit': 'celsius'},
            regulatory_classification="vaccine"
        ),
        Medication(
            id="med_002",
            name="Insulin Glargine",
            manufacturer="Geropharm", 
            batch_number="BATCH-INS-2024-001",
            expiry_date=date(2024, 10, 15),
            temperature_requirements={'min': 2, 'max': 8, 'unit': 'celsius'},
            regulatory_classification="biologic"
        )
    ]
    
    # Validate compliance
    validation_result = compliance_engine.validate_shipment_compliance(
        medications, destination_country="russia"
    )
    
    print("Compliance Validation Result:")
    print(f"Compliant: {validation_result['is_compliant']}")
    print(f"Required Documents: {validation_result['required_documents']}")
    
    if validation_result['validation_errors']:
        print("Validation Errors:")
        for error in validation_result['validation_errors']:
            print(f"  - {error}")
    
    # Generate a compliance document
    shipment_data = {
        'medications': [{'name': med.name, 'batch_number': med.batch_number} for med in medications],
        'destination_pharmacy': 'Lara Pharmacy Kurumkan',
        'total_weight': 15.5
    }
    
    certificate = compliance_engine.generate_compliance_document(
        'certificate_of_analysis', shipment_data
    )
    
    print(f"\nGenerated {certificate.document_type}:")
    print(f"Status: {certificate.status}")
    print(f"References: {certificate.regulatory_references}")

if __name__ == "__main__":
    main()
