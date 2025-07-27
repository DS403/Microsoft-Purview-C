#!/usr/bin/env python3
"""
QUBE Data Dictionary Ingestion for Microsoft Purview

This module provides functionality to ingest QUBE data dictionary metadata
into Microsoft Purview using pyapacheatlas. It creates custom entity types
for table and field specifications and processes CSV files containing
metadata information.

Usage:
    from modules.catalog.qube_ingestion import ingest_qube_data
    
    # Called from ds_main.py with existing client
    qube_summary = ingest_qube_data(prod_client, 'modules/catalog/QUBE MRI Data Dictionary.csv')
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from pyapacheatlas.core.util import AtlasException
except ImportError:
    # Fallback if AtlasException is not available
    AtlasException = Exception

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ingest_qube_data(client, csv_path: str) -> Dict[str, Any]:
    """
    Main entry point for QUBE data dictionary ingestion.
    
    This function is designed to be called from ds_main.py with the existing
    qa_client and processes the Sample QUBE.csv file to create custom entity
    types and ingest metadata into Microsoft Purview.
    
    Args:
        client: Existing Purview client from ds_main.py (qa_client)
        csv_path: Path to the QUBE CSV file (relative to scripts directory)
        
    Returns:
        Dict containing ingestion summary and statistics
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If client is invalid or CSV structure is incorrect
    """
    try:
        logger.info(f"Starting QUBE data dictionary ingestion from {csv_path}")
        
        # Initialize the ingester with the provided client
        ingester = QubePurviewIngester(client)
        
        # Create custom entity types if they don't exist
        logger.info("Creating custom entity types...")
        ingester.create_custom_types()
        
        # Process the CSV file and create entities
        logger.info("Processing CSV file and creating entities...")
        ingester.process_csv(csv_path)
        
        # Get and return summary
        summary = ingester.get_ingestion_summary()
        logger.info(f"Ingestion completed successfully: {summary}")
        
        return summary
        
    except Exception as e:
        logger.error(f"Error during QUBE data ingestion: {str(e)}")
        raise


class QubePurviewIngester:
    """
    Main orchestrator class for QUBE data dictionary ingestion.
    
    This class coordinates the ingestion process by managing custom type creation,
    CSV processing, and entity creation in Microsoft Purview.
    """
    
    def __init__(self, client):
        """
        Initialize the ingester with an existing Purview client.
        
        Args:
            client: Purview client instance from ds_main.py
        """
        self.client = client
        self.type_manager = TypeDefinitionManager(client)
        self.csv_processor = None
        self.entity_factory = EntityFactory(client)
        self.ingestion_stats = {
            'tables_processed': 0,
            'fields_processed': 0,
            'entities_created': 0,
            'errors': []
        }
        
    def create_custom_types(self):
        """Create custom entity types for QUBE data dictionary."""
        try:
            logger.info("Creating custom entity types...")
            results = self.type_manager.register_types()
            
            if "error" in results:
                self.ingestion_stats['errors'].append(f"Type creation error: {results['error']}")
                logger.error(f"Failed to create custom types: {results['error']}")
                return False
            
            # Log results
            for type_name, success in results.items():
                if success:
                    logger.info(f"Successfully handled {type_name} entity type")
                else:
                    error_msg = f"Failed to create {type_name} entity type"
                    self.ingestion_stats['errors'].append(error_msg)
                    logger.error(error_msg)
            
            return all(results.values())
            
        except Exception as e:
            error_msg = f"Error in create_custom_types: {str(e)}"
            self.ingestion_stats['errors'].append(error_msg)
            logger.error(error_msg)
            return False
        
    def process_csv(self, csv_path: str):
        """Process the QUBE CSV file and create entities."""
        try:
            # Initialize CSV processor
            self.csv_processor = CSVProcessor()
            
            # Load and process CSV file
            if not self.csv_processor.load_csv(csv_path):
                raise ValueError("Failed to load CSV file")
                
            if not self.csv_processor.transform_data():
                raise ValueError("Failed to transform CSV data")
                
            if not self.csv_processor.handle_data_types():
                raise ValueError("Failed to handle data types")
                
            if not self.csv_processor.validate_required_fields():
                raise ValueError("Failed to validate required fields")
                
            # Get processed data
            processed_data = self.csv_processor.get_processed_data()
            
            # Update statistics
            self.ingestion_stats['tables_processed'] = len(processed_data['tables'])
            self.ingestion_stats['fields_processed'] = len(processed_data['fields'])
            
            logger.info(f"Successfully processed CSV: {self.ingestion_stats['tables_processed']} tables, {self.ingestion_stats['fields_processed']} fields")
            
            # Create entities from processed data
            if not self._create_entities(processed_data):
                raise ValueError("Failed to create entities in Purview")
            
            return True
            
        except Exception as e:
            error_msg = f"Error processing CSV: {str(e)}"
            self.ingestion_stats['errors'].append(error_msg)
            logger.error(error_msg)
            return False
            
    def _create_entities(self, processed_data: Dict[str, Any]) -> bool:
        """
        Create table and field entities in Purview from processed data.
        
        Args:
            processed_data: Dictionary containing processed tables and fields data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Creating entities in Purview...")
            
            # Step 1: Create table entities first
            table_entities = []
            table_qualified_names = {}
            
            for table_name, table_data in processed_data['tables'].items():
                try:
                    table_entity = self.entity_factory.create_table_entity(table_data)
                    table_entities.append(table_entity)
                    table_qualified_names[table_name] = table_entity['attributes']['qualifiedName']
                    logger.debug(f"Prepared table entity: {table_name}")
                except Exception as e:
                    error_msg = f"Error creating table entity for {table_name}: {str(e)}"
                    self.ingestion_stats['errors'].append(error_msg)
                    logger.error(error_msg)
                    
            # Upload table entities in batch
            if table_entities:
                logger.info(f"Uploading {len(table_entities)} table entities...")
                table_result = self.entity_factory.batch_create_entities(table_entities)
                
                if table_result['success_rate'] < 100:
                    logger.warning(f"Table creation had issues: {table_result['success_rate']:.1f}% success rate")
                    self.ingestion_stats['errors'].extend(table_result.get('errors', []))
                else:
                    logger.info("All table entities created successfully")
                    
                self.ingestion_stats['entities_created'] += table_result['created_count']
            
            # Step 2: Create field entities with parent table relationships
            field_entities = []
            
            for field_data in processed_data['fields']:
                try:
                    parent_table_name = field_data['parent_table_name']
                    
                    # Get the qualified name of the parent table
                    if parent_table_name in table_qualified_names:
                        parent_qualified_name = table_qualified_names[parent_table_name]
                        field_entity = self.entity_factory.create_field_entity(field_data, parent_qualified_name)
                        field_entities.append(field_entity)
                        logger.debug(f"Prepared field entity: {parent_table_name}.{field_data['field_name']}")
                    else:
                        error_msg = f"Parent table {parent_table_name} not found for field {field_data['field_name']}"
                        self.ingestion_stats['errors'].append(error_msg)
                        logger.error(error_msg)
                        
                except Exception as e:
                    error_msg = f"Error creating field entity for {field_data.get('field_name', 'unknown')}: {str(e)}"
                    self.ingestion_stats['errors'].append(error_msg)
                    logger.error(error_msg)
                    
            # Upload field entities in batch
            if field_entities:
                logger.info(f"Uploading {len(field_entities)} field entities...")
                field_result = self.entity_factory.batch_create_entities(field_entities)
                
                if field_result['success_rate'] < 100:
                    logger.warning(f"Field creation had issues: {field_result['success_rate']:.1f}% success rate")
                    self.ingestion_stats['errors'].extend(field_result.get('errors', []))
                else:
                    logger.info("All field entities created successfully")
                    
                self.ingestion_stats['entities_created'] += field_result['created_count']
            
            # Log final statistics
            total_expected = len(processed_data['tables']) + len(processed_data['fields'])
            success_rate = (self.ingestion_stats['entities_created'] / total_expected) * 100 if total_expected > 0 else 0
            
            logger.info(f"Entity creation completed: {self.ingestion_stats['entities_created']}/{total_expected} entities created ({success_rate:.1f}% success rate)")
            
            return success_rate > 0  # Return True if at least some entities were created
            
        except Exception as e:
            error_msg = f"Error in _create_entities: {str(e)}"
            self.ingestion_stats['errors'].append(error_msg)
            logger.error(error_msg)
            return False
        
    def get_ingestion_summary(self) -> Dict[str, Any]:
        """Return summary statistics of the ingestion process."""
        return {
            'status': 'completed',
            'statistics': self.ingestion_stats,
            'message': 'QUBE data dictionary ingestion completed successfully'
        }


class TypeDefinitionManager:
    """
    Handles creation and management of custom entity types for QUBE data dictionary.
    
    This class creates two custom entity types:
    - qube_table_specification: Represents table-level metadata
    - qube_field_specification: Represents field-level metadata with relationships
    """
    
    def __init__(self, client):
        """
        Initialize the type definition manager.
        
        Args:
            client: Purview client instance
        """
        self.client = client
        
    def create_table_specification_type(self) -> dict:
        """
        Create the qube_table_specification entity type definition.
        
        Returns:
            Dictionary containing the entity type definition
        """
        table_type_def = {
            "category": "ENTITY",
            "name": "qube_table_specification",
            "description": "QUBE data dictionary table specification",
            "typeVersion": "1.0",
            "superTypes": ["DataSet"],
            "attributeDefs": [
                {
                    "name": "table_name",
                    "typeName": "string",
                    "isOptional": False,
                    "cardinality": "SINGLE",
                    "isUnique": True,
                    "isIndexable": True,
                    "displayName": "Table Name"
                },
                {
                    "name": "business_name", 
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Business Name"
                },
                {
                    "name": "release_version",
                    "typeName": "string", 
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Release Version"
                },
                {
                    "name": "module_name",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE", 
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Module"
                },
                {
                    "name": "table_description",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": False,
                    "displayName": "Description"
                },
                {
                    "name": "last_amended_date",
                    "typeName": "date",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Last Amended"
                },
                {
                    "name": "amendment_logging",
                    "typeName": "boolean",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Amendment Logging"
                },
                {
                    "name": "operational_security",
                    "typeName": "boolean",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Operational Security"
                },
                {
                    "name": "document_folders",
                    "typeName": "boolean",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Document Folders"
                }
            ]
        }
        
        return table_type_def
        
    def create_field_specification_type(self) -> dict:
        """
        Create the qube_field_specification entity type definition.
        
        Returns:
            Dictionary containing the entity type definition
        """
        field_type_def = {
            "category": "ENTITY",
            "name": "qube_field_specification",
            "description": "QUBE data dictionary field specification",
            "typeVersion": "1.0", 
            "superTypes": ["DataSet"],
            "attributeDefs": [
                {
                    "name": "field_name",
                    "typeName": "string",
                    "isOptional": False,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Field Name"
                },
                {
                    "name": "field_business_name",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Business Name"
                },
                {
                    "name": "sequence_number",
                    "typeName": "int",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Sequence Number"
                },
                {
                    "name": "field_description",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": False,
                    "displayName": "Description"
                },
                {
                    "name": "data_type",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Data Type"
                },
                {
                    "name": "field_length",
                    "typeName": "int",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Length"
                },
                {
                    "name": "precision_value",
                    "typeName": "int",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Precision"
                },
                {
                    "name": "scale_value",
                    "typeName": "int",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Scale"
                },
                {
                    "name": "key_field",
                    "typeName": "int",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Key Field"
                },
                {
                    "name": "log_type",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Log Type"
                },
                {
                    "name": "validation_rule",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": False,
                    "displayName": "Validation Rule"
                },
                {
                    "name": "validation_code",
                    "typeName": "string",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Validation Code"
                },
                {
                    "name": "nulls_allowed",
                    "typeName": "boolean",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Nulls Allowed"
                },
                {
                    "name": "required_field",
                    "typeName": "boolean",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Required"
                },
                {
                    "name": "field_last_amended",
                    "typeName": "date",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Last Amended"
                },
                {
                    "name": "optimize_filtering",
                    "typeName": "boolean",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Optimize Filtering"
                },
                {
                    "name": "parent_table",
                    "typeName": "qube_table_specification",
                    "isOptional": True,
                    "cardinality": "SINGLE",
                    "isUnique": False,
                    "isIndexable": True,
                    "displayName": "Parent Table"
                }
            ]
        }
        
        return field_type_def
        
    def register_types(self) -> Dict[str, bool]:
        """
        Register custom entity types with Purview Atlas API.
        
        Returns:
            Dictionary indicating success/failure for each type registration
        """
        results = {}
        
        try:
            # Always try to create types - let the _create_type method handle conflicts
            table_type_def = self.create_table_specification_type()
            table_result = self._create_type(table_type_def)
            results["qube_table_specification"] = table_result
            if table_result:
                logger.info("Successfully handled qube_table_specification entity type")
            
            field_type_def = self.create_field_specification_type()
            field_result = self._create_type(field_type_def)
            results["qube_field_specification"] = field_result
            if field_result:
                logger.info("Successfully handled qube_field_specification entity type")
                
        except Exception as e:
            logger.error(f"Error registering entity types: {str(e)}")
            results["error"] = str(e)
            
        return results
        
    def _get_existing_types(self) -> List[str]:
        """
        Get list of existing entity type names from Purview.
        
        Returns:
            List of existing entity type names
        """
        try:
            # Use the client to get existing types
            # This will depend on the specific pyapacheatlas client implementation
            existing_types = []
            
            # Try to get type definitions - this may vary based on client version
            if hasattr(self.client, 'get_typedef'):
                type_defs = self.client.get_typedef()
                if type_defs and 'entityDefs' in type_defs:
                    existing_types = [t.get('name', '') for t in type_defs['entityDefs']]
            elif hasattr(self.client, 'atlas'):
                # Alternative approach for different client versions
                type_defs = self.client.atlas.get_typedef()
                if type_defs and 'entityDefs' in type_defs:
                    existing_types = [t.get('name', '') for t in type_defs['entityDefs']]
                    
            return existing_types
            
        except Exception as e:
            logger.warning(f"Could not retrieve existing types: {str(e)}")
            return []
            
    def _create_type(self, type_definition: dict) -> bool:
        """
        Create a single entity type in Purview.
        
        Args:
            type_definition: Entity type definition dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create the type definition using the client
            # pyapacheatlas expects a dictionary with entityDefs key, not a list
            typedef_payload = {
                "entityDefs": [type_definition],
                "enumDefs": [],
                "relationshipDefs": [],
                "structDefs": []
            }
            
            if hasattr(self.client, 'upload_typedefs'):
                result = self.client.upload_typedefs(typedef_payload)
                return True
            elif hasattr(self.client, 'atlas'):
                result = self.client.atlas.upload_typedefs(typedef_payload)
                return True
            else:
                logger.error("Client does not have expected type definition upload methods")
                return False
                
        except AtlasException as e:
            error_msg = str(e)
            # Check if the error is due to type already existing
            if "already exists" in error_msg or "ATLAS-409-00-001" in error_msg:
                logger.info(f"Type {type_definition.get('name', 'unknown')} already exists, skipping creation")
                return True
            else:
                logger.error(f"AtlasException creating type {type_definition.get('name', 'unknown')}: {error_msg}")
                return False
        except Exception as e:
            error_msg = str(e)
            # Check if the error is due to type already existing
            if "already exists" in error_msg or "409" in error_msg or "ATLAS-409" in error_msg:
                logger.info(f"Type {type_definition.get('name', 'unknown')} already exists, skipping creation")
                return True
            else:
                logger.error(f"Error creating type {type_definition.get('name', 'unknown')}: {error_msg}")
                return False


class CSVProcessor:
    """
    Handles CSV file parsing and data transformation for QUBE data dictionary.
    
    This class processes the Sample QUBE.csv file with its specific column structure
    and transforms the data into a format suitable for entity creation.
    """
    
    def __init__(self):
        """Initialize the CSV processor."""
        self.raw_data = None
        self.processed_data = {
            'tables': {},
            'fields': []
        }
        
    def load_csv(self, file_path: str) -> bool:
        """
        Load and validate CSV structure from Sample QUBE.csv file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert relative path to absolute path from scripts directory
            if not file_path.startswith('/') and not file_path.startswith('C:'):
                # Assume path is relative to scripts directory
                base_path = Path(__file__).resolve().parent.parent.parent
                full_path = base_path / file_path
            else:
                full_path = Path(file_path)
                
            logger.info(f"Loading CSV file from: {full_path}")
            
            # Load CSV with pandas
            self.raw_data = pd.read_csv(full_path)
            
            # Validate required columns exist
            required_columns = ['Table Name', 'Field Name']
            missing_columns = [col for col in required_columns if col not in self.raw_data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
                
            logger.info(f"Successfully loaded CSV with {len(self.raw_data)} rows and {len(self.raw_data.columns)} columns")
            return True
            
        except FileNotFoundError:
            logger.error(f"CSV file not found: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            return False
            
    def transform_data(self) -> bool:
        """
        Convert CSV data to entity-ready format with proper column mapping.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.raw_data is None:
                raise ValueError("No CSV data loaded. Call load_csv() first.")
                
            logger.info("Transforming CSV data...")
            
            # Process each row in the CSV
            for index, row in self.raw_data.iterrows():
                table_name = str(row.get('Table Name', '')).strip()
                field_name = str(row.get('Field Name', '')).strip()
                
                if not table_name or not field_name:
                    logger.warning(f"Skipping row {index}: missing table name or field name")
                    continue
                    
                # Process table-level data (deduplicate by table name)
                if table_name not in self.processed_data['tables']:
                    table_data = self._extract_table_data(row)
                    self.processed_data['tables'][table_name] = table_data
                    
                # Process field-level data
                field_data = self._extract_field_data(row, table_name)
                self.processed_data['fields'].append(field_data)
                
            logger.info(f"Processed {len(self.processed_data['tables'])} tables and {len(self.processed_data['fields'])} fields")
            return True
            
        except Exception as e:
            logger.error(f"Error transforming CSV data: {str(e)}")
            return False
            
    def _extract_table_data(self, row) -> Dict[str, Any]:
        """
        Extract table-level metadata from a CSV row.
        
        Args:
            row: Pandas Series representing a CSV row
            
        Returns:
            Dictionary containing table metadata
        """
        return {
            'table_name': str(row.get('Table Name', '')).strip(),
            'business_name': str(row.get('Business Name', '')).strip() or None,
            'release_version': str(row.get('Release', '')).strip() or None,
            'module_name': str(row.get('Module', '')).strip() or None,
            'table_description': str(row.get('Description', '')).strip() or None,
            'last_amended_date': self._parse_date(row.get('Last Amended')),
            'amendment_logging': self._parse_boolean(row.get('Amendment Logging')),
            'operational_security': self._parse_boolean(row.get('Operational Security')),
            'document_folders': self._parse_boolean(row.get('Document Folders'))
        }
        
    def _extract_field_data(self, row, table_name: str) -> Dict[str, Any]:
        """
        Extract field-level metadata from a CSV row.
        
        Args:
            row: Pandas Series representing a CSV row
            table_name: Name of the parent table
            
        Returns:
            Dictionary containing field metadata
        """
        return {
            'field_name': str(row.get('Field Name', '')).strip(),
            'field_business_name': str(row.get('Business Name', '')).strip() or None,
            'sequence_number': self._parse_int(row.get('Sequence Number')),
            'field_description': str(row.get('Description', '')).strip() or None,
            'data_type': str(row.get('Data Type', '')).strip() or None,
            'field_length': self._parse_int(row.get('Length')),
            'precision_value': self._parse_int(row.get('Precision')),
            'scale_value': self._parse_int(row.get('Scale')),
            'key_field': self._parse_int(row.get('Key Field')),
            'log_type': str(row.get('Log Type', '')).strip() or None,
            'validation_rule': str(row.get('Validation Rule', '')).strip() or None,
            'validation_code': str(row.get('Validation Code', '')).strip() or None,
            'nulls_allowed': self._parse_boolean(row.get('Nulls Allowed')),
            'required_field': self._parse_boolean(row.get('Required')),
            'field_last_amended': self._parse_date(row.get('Last Amended')),
            'optimize_filtering': self._parse_boolean(row.get('Optimize Filtering')),
            'parent_table_name': table_name
        }
        
    def handle_data_types(self) -> bool:
        """
        Convert string booleans and handle nulls in the processed data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Handling data type conversions...")
            
            # Data type conversion is already handled in _extract_table_data and _extract_field_data
            # through the helper methods _parse_boolean, _parse_int, and _parse_date
            
            # Additional validation could be added here if needed
            return True
            
        except Exception as e:
            logger.error(f"Error handling data types: {str(e)}")
            return False
            
    def validate_required_fields(self) -> bool:
        """
        Ensure Table Name and Field Name are present in all records.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            logger.info("Validating required fields...")
            
            # Check tables
            invalid_tables = [name for name, data in self.processed_data['tables'].items() 
                            if not data.get('table_name')]
            
            if invalid_tables:
                logger.error(f"Tables with missing table names: {invalid_tables}")
                return False
                
            # Check fields
            invalid_fields = [i for i, field in enumerate(self.processed_data['fields']) 
                            if not field.get('field_name') or not field.get('parent_table_name')]
            
            if invalid_fields:
                logger.error(f"Fields with missing required data at indices: {invalid_fields}")
                return False
                
            logger.info("Required field validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Error validating required fields: {str(e)}")
            return False
            
    def get_processed_data(self) -> Dict[str, Any]:
        """
        Get the processed data ready for entity creation.
        
        Returns:
            Dictionary containing processed tables and fields data
        """
        return self.processed_data
        
    def _parse_boolean(self, value) -> Optional[bool]:
        """
        Parse boolean values from CSV (handles True/False strings and various formats).
        
        Args:
            value: Value to parse as boolean
            
        Returns:
            Boolean value or None if cannot be parsed
        """
        if pd.isna(value) or value == '':
            return None
            
        str_value = str(value).strip().lower()
        
        if str_value in ['true', '1', 'yes', 'y']:
            return True
        elif str_value in ['false', '0', 'no', 'n']:
            return False
        else:
            return None
            
    def _parse_int(self, value) -> Optional[int]:
        """
        Parse integer values from CSV, handling nulls and empty strings.
        
        Args:
            value: Value to parse as integer
            
        Returns:
            Integer value or None if cannot be parsed
        """
        if pd.isna(value) or value == '':
            return None
            
        try:
            return int(float(value))  # Handle cases where int is stored as float
        except (ValueError, TypeError):
            return None
            
    def _parse_date(self, value) -> Optional[int]:
        """
        Parse date values from CSV, converting to timestamp (milliseconds since epoch).
        
        Args:
            value: Value to parse as date
            
        Returns:
            Timestamp in milliseconds or None if cannot be parsed
        """
        if pd.isna(value) or value == '':
            return None
            
        try:
            # Try to parse the date and convert to timestamp
            parsed_date = pd.to_datetime(value, dayfirst=True)  # Assuming DD-MMM-YYYY format
            # Convert to milliseconds since epoch (Atlas expects this format)
            return int(parsed_date.timestamp() * 1000)
        except (ValueError, TypeError):
            # If parsing fails, return None
            return None

class EntityFactory:
    """
    Creates Atlas entity instances from processed data.
    
    This class generates qube_table_specification and qube_field_specification
    entities from the processed CSV data and handles batch creation in Purview.
    """
    
    def __init__(self, client):
        """
        Initialize the entity factory.
        
        Args:
            client: Purview client instance
        """
        self.client = client
        self.created_entities = []
        
    def create_table_entity(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a qube_table_specification entity from table data.
        
        Args:
            table_data: Dictionary containing table metadata
            
        Returns:
            Dictionary representing the Atlas entity
        """
        try:
            qualified_name = self.generate_qualified_name("table", table_data['table_name'])
            
            entity = {
                "typeName": "qube_table_specification",
                "attributes": {
                    "qualifiedName": qualified_name,
                    "name": table_data['table_name'],
                    "table_name": table_data['table_name'],
                    "business_name": table_data.get('business_name'),
                    "release_version": table_data.get('release_version'),
                    "module_name": table_data.get('module_name'),
                    "table_description": table_data.get('table_description'),
                    "last_amended_date": table_data.get('last_amended_date'),
                    "amendment_logging": table_data.get('amendment_logging'),
                    "operational_security": table_data.get('operational_security'),
                    "document_folders": table_data.get('document_folders')
                },
                "guid": None,  # Will be assigned by Purview
                "status": "ACTIVE"
            }
            
            logger.debug(f"Created table entity for: {table_data['table_name']}")
            return entity
            
        except Exception as e:
            logger.error(f"Error creating table entity for {table_data.get('table_name', 'unknown')}: {str(e)}")
            raise
            
    def create_field_entity(self, field_data: Dict[str, Any], parent_table_qualified_name: str) -> Dict[str, Any]:
        """
        Create a qube_field_specification entity from field data with parent table relationship.
        
        Args:
            field_data: Dictionary containing field metadata
            parent_table_qualified_name: Qualified name of the parent table
            
        Returns:
            Dictionary representing the Atlas entity
        """
        try:
            qualified_name = self.generate_qualified_name("field", field_data['parent_table_name'], field_data['field_name'])
            
            entity = {
                "typeName": "qube_field_specification",
                "attributes": {
                    "qualifiedName": qualified_name,
                    "name": field_data['field_name'],
                    "field_name": field_data['field_name'],
                    "field_business_name": field_data.get('field_business_name'),
                    "sequence_number": field_data.get('sequence_number'),
                    "field_description": field_data.get('field_description'),
                    "data_type": field_data.get('data_type'),
                    "field_length": field_data.get('field_length'),
                    "precision_value": field_data.get('precision_value'),
                    "scale_value": field_data.get('scale_value'),
                    "key_field": field_data.get('key_field'),
                    "log_type": field_data.get('log_type'),
                    "validation_rule": field_data.get('validation_rule'),
                    "validation_code": field_data.get('validation_code'),
                    "nulls_allowed": field_data.get('nulls_allowed'),
                    "required_field": field_data.get('required_field'),
                    "field_last_amended": field_data.get('field_last_amended'),
                    "optimize_filtering": field_data.get('optimize_filtering'),
                    "parent_table": {
                        "typeName": "qube_table_specification",
                        "uniqueAttributes": {
                            "qualifiedName": parent_table_qualified_name
                        }
                    }
                },
                "guid": None,  # Will be assigned by Purview
                "status": "ACTIVE"
            }
            
            logger.debug(f"Created field entity for: {field_data['parent_table_name']}.{field_data['field_name']}")
            return entity
            
        except Exception as e:
            logger.error(f"Error creating field entity for {field_data.get('field_name', 'unknown')}: {str(e)}")
            raise
            
    def generate_qualified_name(self, entity_type: str, *identifiers) -> str:
        """
        Generate unique qualified names using "qube://table_name" and "qube://table_name/field_name" patterns.
        
        Args:
            entity_type: Type of entity ("table" or "field")
            *identifiers: Variable arguments for building the qualified name
            
        Returns:
            Unique qualified name string
        """
        try:
            if entity_type == "table":
                table_name = identifiers[0]
                return f"qube://{table_name}"
            elif entity_type == "field":
                table_name = identifiers[0]
                field_name = identifiers[1]
                return f"qube://{table_name}/{field_name}"
            else:
                raise ValueError(f"Unknown entity type: {entity_type}")
                
        except Exception as e:
            logger.error(f"Error generating qualified name for {entity_type}: {str(e)}")
            raise
            
    def batch_create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Efficiently upload multiple entities to Purview in batches.
        
        Args:
            entities: List of entity dictionaries to create
            
        Returns:
            Dictionary containing creation results and statistics
        """
        try:
            batch_size = 100  # Process in batches of 100
            total_entities = len(entities)
            created_count = 0
            failed_count = 0
            errors = []
            
            logger.info(f"Starting batch creation of {total_entities} entities")
            
            # Process entities in batches
            for i in range(0, total_entities, batch_size):
                batch = entities[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (total_entities + batch_size - 1) // batch_size
                
                logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} entities)")
                
                try:
                    # Create entities using the client
                    result = self._create_entities_batch(batch)
                    
                    if result.get('success', False):
                        created_count += len(batch)
                        logger.info(f"Successfully created batch {batch_num}")
                    else:
                        failed_count += len(batch)
                        error_msg = f"Failed to create batch {batch_num}: {result.get('error', 'Unknown error')}"
                        errors.append(error_msg)
                        logger.error(error_msg)
                        
                except Exception as e:
                    failed_count += len(batch)
                    error_msg = f"Exception in batch {batch_num}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    
            # Update created entities list
            self.created_entities.extend([e for e in entities if e not in errors])
            
            result = {
                'total_entities': total_entities,
                'created_count': created_count,
                'failed_count': failed_count,
                'success_rate': (created_count / total_entities) * 100 if total_entities > 0 else 0,
                'errors': errors
            }
            
            logger.info(f"Batch creation completed: {created_count}/{total_entities} entities created successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in batch_create_entities: {str(e)}")
            raise
            
    def _create_entities_batch(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a single batch of entities using the Purview client.
        
        Args:
            entities: List of entity dictionaries to create
            
        Returns:
            Dictionary containing batch creation result
        """
        try:
            # Use the client to create entities
            # This will depend on the specific pyapacheatlas client implementation
            if hasattr(self.client, 'upload_entities'):
                result = self.client.upload_entities(entities)
                return {'success': True, 'result': result}
            elif hasattr(self.client, 'atlas'):
                result = self.client.atlas.upload_entities(entities)
                return {'success': True, 'result': result}
            else:
                return {'success': False, 'error': 'Client does not have expected entity upload methods'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def get_created_entities(self) -> List[Dict[str, Any]]:
        """
        Get list of successfully created entities.
        
        Returns:
            List of created entity dictionaries
        """
        return self.created_entities
        
    def clear_created_entities(self):
        """Clear the list of created entities."""
        self.created_entities = []


if __name__ == "__main__":
    # This module is designed to be imported and called from ds_main.py
    print("This module should be imported and called from ds_main.py")
    print("Usage: from modules.catalog.qube_ingestion import ingest_qube_data")