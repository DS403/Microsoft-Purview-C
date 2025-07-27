
## Get All Entities guid for a glossary term name

```python
from scripts.modules.glossary import *

def example_get_all_guids_of_entities_with_glossary_term():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    entities_guid = glossary.get_all_guids_of_entities_with_glossary_term(glossary_term_name, glossary_name)
    print(entities_guid)
```

<br />

## Get All Entities a Glossary Term is Associated With

```python
from scripts.modules.glossary import *

def example_get_all_entities_with_glossary_term():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    entities_with_glossary_term = glossary.get_all_entitities_with_glossary_term(glossary_term_name, glossary_name)
    print(entities_with_glossary_term)
```

<br />

## Write output column names for a specified Glossary Term 

```python
from scripts.modules.glossary import *

def example_output_column_names_with_specific_glossary_term():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    result = glossary.output_column_names_with_specific_glossary_term(glossary_term_name, glossary_name)
    print(result)
```

<br />

## Get all column names for a specified Glossary Term 

```python
from scripts.modules.glossary import *

def example_get_column_names_with_specific_glossary_term():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    result = glossary.get_column_names_with_specific_glossary_term(glossary_term_name, glossary_name)
    print(result)
```

<br />

## Remove a Glossary Term from All Entities it's Associated With

```python
from scripts.modules.glossary import *

def example_remove_term_from_all_entities():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    entities_with_glossary_term = glossary.get_all_entitities_with_glossary_term(glossary_term_name, glossary_name)
    result = glossary.remove_term_from_all_entities(entities_with_glossary_term, glossary_term_name, glossary_name)
    print(result)
```

<br />

## Get Glossary Terms for a specified entity type

```python
from scripts.modules.glossary import *

def example_propagate_glossary_term_by_specific_entity_type():
    entity_type="Table"
    glossary_term_name = "Bill of Material"
    fields = "ZZDACCOUNT"
    directory = "desktop/glossary/Table" #specify the path
    result = glossary.propagate_glossary_term_by_specific_entity_type(entity_type, glossary_term_name, fields, directory)
    print(result)
```

<br />

## Propagate glossary for purview

```python
from scripts.modules.glossary import *

def example_prod_glossary_propagation_non_sap():
    result = glossary.prod_glossary_propagation_non_sap()
    print(result)
```

<br />


## Get glossary terms and associated fields

```python
from scripts.modules.glossary import *

def example_get_glossary_terms_dict():
    import_file_name="11_15_23_Purview_Glossary_Import_716_Terms.xlsx"
    result = glossary.get_glossary_terms_dict(import_file_name)
    print(result)
```

<br />

## Reads imported excel file which contains glossary terms and associated fields

```python
from scripts.modules.glossary import *

def example_read_glossary_import_file():
    import_file_name="11_15_23_Purview_Glossary_Import_716_Terms.xlsx"
    result = glossary.read_glossary_import_file(file_name)
    print(result)
```

<br />


## Delete glossary term from the entity and column for the specified GUID

```python
from scripts.modules.glossary import *

def example_delete_term_from_entity_and_columns():
    view_guid="5991f48e-69a3-4598-93bb-83f6f6f60000"
    result = glossary.delete_term_from_entity_and_columns(view_guid)
    print(result)
```

<br />


## Get table columns for the SAP S4 Hana source

```python
from scripts.modules.glossary import *

def example_pull_sap_s4hana_table_columns_without_glossary_terms():
    purview_acct_short_name="prod"
    table_name="MARA"
    result = glossary.pull_sap_s4hana_table_columns_without_glossary_terms(purview_acct_short_name, table_name)
    print(result)
```

<br />

## Get columns for the SAP S4 Hana source

```python
from scripts.modules.glossary import *

def example_pull_sap_s4hana_columns_of_table():
    purview_acct_short_name="prod"
    table_name="MARA"
    result = glossary.pull_sap_s4hana_columns_of_table(purview_acct_short_name, table_name)
    print(result)
```

<br />

## Get tables and columns with out glossary terms for the SAP S4 Hana source

```python
from scripts.modules.glossary import *

def example_pull_s4_table_columns():
    result = glossary.pull_s4_table_columns()
    print(result)
```

<br />

## Get columns for which there no glossary terms is assigned

```python
from scripts.modules.glossary import *

def example_extract_fields_for_which_there_are_not_glossary_terms():
    result = glossary.extract_fields_for_which_there_are_not_glossary_terms()
    print(result)
```

