
## Propagation of glossary terms for Sap Hana source 

```python
from scripts.modules.glossary import *

def example_glossary_propagation_of_sap_s4hana():
    purview_acct_short_name="prod"
    import_file_name="11_15_23_Purview_Glossary_Import_716_Terms.xlsx"
    result=glossary_propagation_of_sap_s4hana(purview_acct_short_name, import_file_name)
    print(result)

```
<br />