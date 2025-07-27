
## Propagate glossary terms for all the data lake assets 

```python
from scripts.modules.glossary import *

def example_propagate_glossary_terms_across_data_lake_resource_sets():
    input_filename = purview_acct_short_name + "_pulled_entities.json"
    pulled_entities = {}
    with open(input_filename, "r", encoding="utf-8") as json_file:
        pulled_entities = json.load(json_file)

    glossary_terms_dict = get_glossary_terms_dict()
    directory = 'outputs/glossary_propagation_outputs/datalake_outputs/' + purview_acct_short_name
    output_file_path = purview_acct_short_name + "_datalake_glossary_propagation_results"
    os.makedirs(directory, exist_ok=True) # Create the directory if it doesn't exist
    output_file_path = os.path.join(directory, output_file_path)

    datalake_resource_set_entities = pulled_entities.get("data_sources").get("azure_datalake_gen2").get("azure_datalake_gen2_resource_set").get("all_entity_details")

    glossary_term_name="AFS Account"
    fields="ZZDACCOUNT"
    datalake_result=propagate_glossary_terms_across_data_lake_resource_sets(datalake_resource_set_entities,glossary_term_name, fields)
    print(result)
    
```
<br />

## Propagate glossary terms for all the data lake assets 

```python
from scripts.modules.glossary import *

def example_glossary_propagation_of_datalake():
    purview_acct_short_name="prod"
    result=glossary_propagation_of_datalake(purview_acct_short_name)
    print(result)

```
<br />