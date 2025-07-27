## Parses a JSON file representing a table in a Data Services Project (DSP) and creates corresponding Atlas entities

```python
from scripts.modules.lineage import *
import json

def example_parse_dsp_json_of_table():
    parse_dsp_json_of_table="scripts\inputs\dsp_sap_hana_lineage_input_files\FIN_REP\FIN_REP_Tables\SAP.TIME.M_TIME_DIMENSION_TDAY.json"
    table_qualified_name_header_with_schema="sap_hana://86c39b57-6b4c-4172-a3ac-68fa3b408270.hana.prod-us10.hanacloud.ondemand.com/databases/H00/tables"
    result = parse_dsp_json_of_table(parse_dsp_json_of_table, table_qualified_name_header_with_schema)
    print(result)
```
<br />

## Parses a JSON file representing a table in a Data Services Project (DSP) 

```python
from scripts.modules.lineage import *
import json

def example_parse_dsp_json_of_table():
    # Example JSON dictionary representing a table in a Data Services Project (DSP)
    json_dict = {
        "elements": {
            "column1": {"@EndUserText.label": "Description for Column 1"},
            "column2": {"@EndUserText.label": "Description for Column 2"},
            # Add more columns as needed
        },
        # Add other necessary information
    }
    table_name="ZV_DWC_PRDF_LET"
    table_qualified_name="sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/MD_STG/tables/ZV_DWC_PRDF_LET"
    result = parse_dsp_json_and_create_table(json_dict, table_name, table_qualified_name)
    print(result)
```
<br />

## Parses a JSON file representing a view in a Data Services Project (DSP)

```python
from scripts.modules.lineage import *
import json

def example_parse_dsp_json_and_create_view():
    # Example JSON dictionary representing a table in a Data Services Project (DSP)
    json_dict = {
        "elements": {
            "column1": {"@EndUserText.label": "Description for Column 1"},
            "column2": {"@EndUserText.label": "Description for Column 2"},
            # Add more columns as needed
        },
        # Add other necessary information
    }
    view_name="PL_OTC_ZETA_ORDERHDR_INF"
    view_qualified_name="sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/PL_OTC_ZETA_ORDERHDR_INF"
    result = parse_dsp_json_and_create_view(json_dict, view_name, view_qualified_name)
    print(result)
```
<br />

## Retrieves SAP HANA views with a substring match in their qualified name

```python
from scripts.modules.lineage import *
import json

def example_get_sap_hana_views_with_substring_of_qualified_name():
    
    entity_type="sap_hana_view"
    qualified_name_header="sap_hana://86c39b57-6b4c-4172-a3ac-68fa3b408270.hana.prod-us10.hanacloud.ondemand.com/databases/H00/tables"
    result = get_sap_hana_views_with_substring_of_qualified_name(entity_type, qualified_name_header)
    print(result)
```
<br />

## Extracts the schema name from the given qualified name

```python
from scripts.modules.lineage import *
import json

def example_extract_schema_from_qualified_name():
    
    qualified_name="sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/PL_OTC_ZETA_ORDERHDR_INF"
    result = extract_schema_from_qualified_name(qualified_name)
    print(result)
```
<br />

## Extracts the entity name from the given qualified name

```python
from scripts.modules.lineage import *
import json

def example_extract_entity_name_from_qualified_name():
    
    qualified_name="sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/PL_OTC_ZETA_ORDERHDR_INF"
    result = extract_entity_name_from_qualified_name(qualified_name)
    print(result)
```
<br />

## Creates lineage connections between a target SAP HANA view and its source entities

```python
from scripts.modules.lineage import *
import json

def example_create_lineage_for_view():
    
    target_qualified_name="sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/TD_STG/views/PL_OTC_ZETA_ORDERHDR_INF"
    qualified_names_of_sources=["sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/SAP/views/TIME","sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/MD_STG/tables/ZV_DWC_T006A"]
    result = create_lineage_for_view(target_qualified_name, qualified_names_of_sources)
    print(result)
```
<br />

## Parses a JSON file containing SAP HANA view information and creates entities

```python
from scripts.modules.lineage import *
import json

def example_create_lineage_for_view():
    json_file="scripts\inputs\dsp_sap_hana_lineage_input_files\FIN_REP\FIN_REP_Tables\SAP.TIME.M_TIME_DIMENSION_TDAY.json"
    dsp_header_without_schema="sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/"
    schema="dsp_connection"
    result = parse_json_for_sap_hana_view(json_file, dsp_header_without_schema, schema)
    print(result)
```
<br />

## Adds manual DSP lineage connection between source and target entities

```python
from scripts.modules.lineage import *
import json

def example_add_manual_dsp_lineage():
    source_entity = {
    "name": "ZV_DWC_T006A",
    "entityType": "sap_hana_table",
    "qualifiedName": "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/MD_STG/tables/ZV_DWC_T006A",
    "id": "62075204-2212-47ff-8a6a-0bf6f6f60000"
    }

    target_entity = {
        "name": "RL_MD_MATUNIT",
        "entityType": "sap_hana_view",
        "qualifiedName": "sap_hana://ff43de60-f60e-41a3-98ed-cec560c93756.hana.prod-us10.hanacloud.ondemand.com/databases/H00/schemas/OTC_REP/views/RL_MD_MATUNIT",
        "id": "3e4c88f1-b49d-4648-b3ad-b0f6f6f60000"
    }
    process_type_name="dsp_connection"
    source_schema="sap_hana_table"
    target_schema="sap_hana_view"
    result = add_manual_dsp_lineage(source_entity, target_entity, process_type_name,source_schema, target_schema)
    print(result)
```
<br />

## Retrieves the qualified names of existing SAP HANA views and tables

```python
from scripts.modules.lineage import *
import json

def example_get_existing_prod_sap_hana_view_and_tables_qualified_names():

    result = get_existing_prod_sap_hana_view_and_tables_qualified_names()
    print(result)
```
<br />

## Retrieves the qualified names of existing DSP connections

```python
from scripts.modules.lineage import *
import json

def example_get_existing_prod_dsp_connection_qualified_names():

    result = get_existing_prod_dsp_connection_qualified_names()
    print(result)
```
<br />

## Main function to parse SAP HANA internal lineage, create entities, and build lineage connections

```python
from scripts.modules.lineage import *
import json

def example_parse_sap_hana_internal_lineage():

    result = parse_sap_hana_internal_lineage()
    print(result)
```
<br />