"""
Document Automation Script
Automates generation of compliance documents for pharmaceutical shipments
Adapted from meat export document processing
"""

import json
from datetime import datetime, date
from typing import Dict, List
import logging
from pathlib import Path

class DocumentAutomation:
    """
    Automates generation of pharmaceutical compliance documents
    Enhanced from meat export document processing
    """
    
    def __init__(self, template_directory: str = "templates"):
        self.setup_logging()
        self.template_directory = Path(template_directory)
        self.template_directory.mkdir(exist_ok=True)
        self.load_templates()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DocumentAutomation')
    
    def load_templates(self):
        """Load document templates"""
        self.templates = {
            'certificate_of_analysis': self._load_template('certificate_of_analysis'),
            'customs_declaration': self._load_template('customs_declaration'),
            'health_certificate': self._load_template('health_certificate'),
            'temperature_log': self._load_template('temperature_log')
        }
    
    def _load_template(self, template_name: str) -> Dict:
        """Load template from file or use default"""
        template_file = self.template_directory / f"{template_name}.json"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._get_default_template(template_name)
    
    def _get_default_template(self, template_name: str) -> Dict:
        """Get default template structure"""
        default_templates = {
            'certificate_of_analysis': {
                'document_type': 'certificate_of_analysis',
                'required_fields': [
                    'batch_number', 'manufacturer', 'test_results', 
                    'expiry_date', 'approval_signature'
                ],
                'template_structure': {
                    'header': 'Certificate of Analysis',
                    'sections': ['product_info', 'test_results', 'approval']
                }
            },
            'customs_declaration': {
                'document_type': 'customs_declaration',
                'required_fields': [
                    'exporter', 'importer', 'hs_codes', 'value', 
                    'weight', 'purpose'
                ],
                'template_structure': {
                    'header': 'Customs Declaration',
                    'sections': ['parties', 'goods_description', 'valuation']
                }
            }
        }
        return default_templates.get(template_name, {})
    
    def generate_document(self, document_type: str, data: Dict) -> Dict:
        """
        Generate compliance document based on template and data
        """
        try:
            template = self.templates.get(document_type)
            if not template:
                raise ValueError(f"Unknown document type: {document_type}")
            
            # Validate required fields
            self._validate_required_fields(template, data)
            
            # Generate document content
            document_content = self._build_document_content(template, data)
            
            # Add metadata
            document = {
                'document_id': self._generate_document_id(document_type),
                'document_type': document_type,
                'content': document_content,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'generated_by': 'DocumentAutomationSystem',
                    'version': '1.0'
                },
                'status': 'generated'
            }
            
            self.logger.info(f"Generated {document_type} document: {document['document_id']}")
            return document
            
        except Exception as e:
            self.logger.error(f"Error generating {document_type} document: {e}")
            raise
    
    def _validate_required_fields(self, template: Dict, data: Dict):
        """Validate that all required fields are present"""
        required_fields = template.get('required_fields', [])
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
    
    def _build_document_content(self, template: Dict, data: Dict) -> Dict:
        """Build document content based on template structure"""
        content = {}
        template_structure = template.get('template_structure', {})
        
        # Build header
        content['header'] = {
            'title': template_structure.get('header', 'Document'),
            'document_id': self._generate_document_id(template['document_type']),
            'issue_date': datetime.now().date().isoformat()
        }
        
        # Build sections based on template
        for section in template_structure.get('sections', []):
            content[section] = self._build_section(section, data)
        
        return content
    
    def _build_section(self, section: str, data: Dict) -> Dict:
        """Build specific document section"""
        section_builders = {
            'product_info': self._build_product_info_section,
            'test_results': self._build_test_results_section,
            'approval': self._build_approval_section,
            'parties': self._build_parties_section,
            'goods_description': self._build_goods_description_section,
            'valuation': self._build_valuation_section
        }
        
        builder = section_builders.get(section)
        if builder:
            return builder(data)
        else:
            return {'content': 'Section content not available'}
    
    def _build_product_info_section(self, data: Dict) -> Dict:
        """Build product information section"""
        return {
            'product_name': data.get('product_name', ''),
            'batch_number': data.get('batch_number', ''),
            'manufacturer': data.get('manufacturer', ''),
            'manufacturing_date': data.get('manufacturing_date', ''),
            'expiry_date': data.get('expiry_date', ''),
            'storage_conditions': data.get('storage_conditions', {})
        }
    
    def _build_test_results_section(self, data: Dict) -> Dict:
        """Build test results section"""
        return {
            'purity': data.get('purity', '99.8%'),
            'potency': data.get('potency', 'Within specification'),
            'sterility': data.get('sterility', 'Pass'),
            'endotoxins': data.get('endotoxins', 'Below limit'),
            'testing_laboratory': data.get('testing_laboratory', 'Quality Control Lab Buryatia')
        }
    
    def _build_approval_section(self, data: Dict) -> Dict:
        """Build approval section"""
        return {
            'approval_status': 'Approved',
            'approval_date': datetime.now().date().isoformat(),
            'approved_by': data.get('approval_signature', 'Quality Manager'),
            'remarks': data.get('approval_remarks', 'Product meets all quality standards')
        }
    
    def _build_parties_section(self, data: Dict) -> Dict:
        """Build parties section for customs declaration"""
        return {
            'exporter': {
                'name': data.get('exporter', 'Lara Pharmacy Network'),
                'address': data.get('exporter_address', ''),
                'tax_id': data.get('exporter_tax_id', '')
            },
            'importer': {
                'name': data.get('importer', ''),
                'address': data.get('importer_address', ''),
                'tax_id': data.get('importer_tax_id', '')
            }
        }
    
    def _build_goods_description_section(self, data: Dict) -> Dict:
        """Build goods description section"""
        return {
            'description': data.get('goods_description', 'Pharmaceutical products'),
            'hs_codes': data.get('hs_codes', ['3004.90']),
            'quantity': data.get('quantity', 0),
            'weight_kg': data.get('weight_kg', 0),
            'package_type': data.get('package_type', 'Refrigerated container')
        }
    
    def _build_valuation_section(self, data: Dict) -> Dict:
        """Build valuation section"""
        return {
            'total_value_usd': data.get('total_value_usd', 0),
            'currency': data.get('currency', 'USD'),
            'insurance_value': data.get('insurance_value', 0),
            'freight_charges': data.get('freight_charges', 0)
        }
    
    def _generate_document_id(self, document_type: str) -> str:
        """Generate unique document ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        doc_prefix = {
            'certificate_of_analysis': 'COA',
            'customs_declaration': 'CD',
            'health_certificate': 'HC',
            'temperature_log': 'TLOG'
        }.get(document_type, 'DOC')
        
        return f"{doc_prefix}-{timestamp}"
    
    def batch_generate_documents(self, batch_data: List[Dict]) -> List[Dict]:
        """
        Generate multiple documents in batch
        """
        generated_documents = []
        
        for doc_data in batch_data:
            try:
                document_type = doc_data.get('document_type')
                document_data = doc_data.get('data', {})
                
                document = self.generate_document(document_type, document_data)
                generated_documents.append(document)
                
            except Exception as e:
                self.logger.error(f"Error in batch generation for {doc_data}: {e}")
                # Continue with other documents
        
        self.logger.info(f"Batch generation completed: {len(generated_documents)} documents created")
        return generated_documents
    
    def save_document(self, document: Dict, output_directory: str = "output") -> str:
        """
        Save document to file
        """
        output_path = Path(output_directory)
        output_path.mkdir(exist_ok=True)
        
        filename = f"{document['document_id']}.json"
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(document, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Document saved: {file_path}")
        return str(file_path)


# Example usage
def main():
    automation = DocumentAutomation()
    
    # Generate Certificate of Analysis
    coa_data = {
        'document_type': 'certificate_of_analysis',
        'data': {
            'product_name': 'COVID-19 Vaccine',
            'batch_number': 'BATCH-VAC-2024-001',
            'manufacturer': 'PharmStandard',
            'expiry_date': '2024-12-31',
            'approval_signature': 'Dr. Ivan Petrov',
            'purity': '99.9%',
            'potency': '102% of labeled potency',
            'storage_conditions': {'temperature': '2-8°C', 'humidity': '≤65%'}
        }
    }
    
    coa_document = automation.generate_document(
        coa_data['document_type'], 
        coa_data['data']
    )
    
    print("Generated Certificate of Analysis:")
    print(f"Document ID: {coa_document['document_id']}")
    print(f"Status: {coa_document['status']}")
    
    # Save document
    saved_path = automation.save_document(coa_document)
    print(f"Saved to: {saved_path}")
    
    # Batch generation example
    batch_data = [
        {
            'document_type': 'certificate_of_analysis',
            'data': {
                'product_name': 'Insulin Glargine',
                'batch_number': 'BATCH-INS-2024-001',
                'manufacturer': 'Geropharm',
                'expiry_date': '2024-10-15'
            }
        },
        {
            'document_type': 'customs_declaration', 
            'data': {
                'exporter': 'Lara Pharmacy Network',
                'importer': 'Regional Hospital Kyakhta',
                'total_value_usd': 15000,
                'weight_kg': 25.5
            }
        }
    ]
    
    batch_documents = automation.batch_generate_documents(batch_data)
    print(f"\nBatch generation: {len(batch_documents)} documents created")

if __name__ == "__main__":
    main()
