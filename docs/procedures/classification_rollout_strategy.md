# Classification Rollout Strategy

This document covers the steps to be taken when rolling out additional classifications.

<br />

### STEP 1
## Selecting the classifications to create
- Identify which data domain to create classifications for
- The Purview Developer and Governance Lead will meet to select glossary terms pertaining to the selected data domain
    - These individuals will decide what phrases or acronyms could represent these glossary terms in data sets
    - For example, consider the glossary term **Bill of Materials** and how it could be represented as the following
        - Bill of Materials
        - Bill of Material
        - BOM

<br />

### STEP 2
## Writing the REGEX rules for the selected classifications
- Now that the phrases and acronyms associated with each glossary term are identified, the Purview Developer needs to write REGEX rules that extract any and all combinations of these phrases and acronyms
    - The Purview Developer needs to identify all potential scenarios this term could appear in either column names or table names
    - Using **Bill of Materials** as an example again, the REGEX rule needs to be able to identify that this term is represented by the follwing scenarios:
        - BoM
        - _Bill_Of_Materials_
        - _Bom
        - billofmaterials
        - BillofMaterial
        - BOMTest
        - Testing_bom
    - **Note:** These are just a few examples, **Bill of Materials** needs many more test cases than the ones listed here
- The Purview Developer needs to thoroughly test their REGEX rules before officially creating the classification with that rule
    - One way to test a REGEX rule is directly through Purview
        - When creating a classification rule, after a classification has been created already, one can test the REGEX rule by uploading a test **.csv** file
        - The Purview Developer can then see which column or table names were correctly identified and which were not detected by the REGEX rule
        
<br />

### STEP 3
## Creating and applying the classifications
- Now that the REGEX rules have been appropriately tested, the Purview Developer can officially create the associated classifications and classification rules with the REGEX rules
- Once all of the selected classifications and classification rules have been created, the Purview Developer will create a new scan rule set
    - The Purview Developer will check the boxes for each of the custom classifications they're created that they would like to apply
- Once the new scan rule set is created, the Purview Developer will re-scan any relevant data sets with this new scan rule set that contains the new classifications
