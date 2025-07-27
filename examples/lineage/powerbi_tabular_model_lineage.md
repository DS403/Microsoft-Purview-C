## Loads JSON data from a file

```python
from scripts.modules.lineage import *
import json

def example_load_json():
    json_file_path="scripts\inputs\dsp_sap_hana_lineage_input_files\FIN_REP\FIN_REP_Tables\SAP.TIME.M_TIME_DIMENSION_TDAY.json"
    result = load_json(json_file_path)
    print(result)
```
<br />

## Extracts source schema and table name information from a partitions dictionary.

```python
from scripts.modules.lineage import *
import json

def example_extract_source_schema_and_table_name():
    partitions_dict = [
        {
            "source": {
                "expression": [
                    'Schema="my_schema"',
                    'Item="my_table"'
                ]
            }
        }
    ]
    result = extract_source_schema_and_table_name(partitions_dict)
    print(result)
```
<br />

## Retrieves details of all tables from a tabular model, including their source schema and table name

```python
from scripts.modules.lineage import *
import json

def example_get_all_tables_from_tabular_model():
    tables=["DimFinancialPlanType","DimFinancialMeasure","DimBusiness"]
    start_of_source_qualified_name="https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets"
    result = get_all_tables_from_tabular_model(tables, start_of_source_qualified_name)
    print(result)
```
<br />

## Builds a lineage relationship from a Power BI table to a Power BI dataset

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_pbi_table_to_dataset():
    source_dict = {
    "name": "DimBusiness",
    # Add other relevant details of the Power BI table
    }
    target_dict = {
        "name": "51.14 Amazon KPI Reporting",
        # Add other relevant details of the Power BI dataset
    }
    target_name="51.14 Amazon KPI Reporting"
    result = build_lineage_from_pbi_table_to_dataset(source_dict, target_dict, target_name)
    print(result)
```
<br />

## Creates Power BI table entities in Apache Atlas and returns a list of created entities

```python
from scripts.modules.lineage import *
import json

def example_create_powerbi_tables():
    tables=[
    table1 = {
        "powerbi_table_name": "SalesTable",
        # Add other details as needed
    }
    table2 = {
        "powerbi_table_name": "CustomerTable",
        # Add other details as needed
    }
    ]
    target_dataset_name_without_special_char="5114AmazonKPIReporting"
    target_dataset_qualified_name="https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/d2e8f683-32cb-4647-a7d6-c85f701239a7"
    result = create_powerbi_tables(tables, target_dataset_name_without_special_char, target_dataset_qualified_name)
    print(result)
```
<br />

## Retrieves Power BI table entities of a custom type from Apache Atlas

```python
from scripts.modules.lineage import *
import json

def example_get_custom_power_bi_tables():
    result = get_custom_power_bi_tables()
    print(result)
```
<br />

## Builds lineage from an SQL database table to a Power BI table

```python
from scripts.modules.lineage import *
import json

def example_build_lineage_from_sql_to_pbi_table():
    source_dict={T1:"dimstyle",T2:"dimdate",T3:"AmzFactDaily"} 
    target_dict={Entity:"51.17 - Media Campaign KPI Reporting"}
    target_name="51.14 Amazon KPI Reporting"
    result = build_lineage_from_sql_to_pbi_table(source_dict, target_dict, target_name)
    print(result)
```
<br />

prod_build_powerbi_lineage_from_tabular_model()

## Build lineage relationships from SQL database tables to Power BI tables and from Power BI tables to Power BI datasets

```python
from scripts.modules.lineage import *
import json

def example_ rod_build_powerbi_lineage_from_tabular_model():
    result = prod_build_powerbi_lineage_from_tabular_model()
    print(result)
```
<br />