<!-- Improved compatibility of Back to Top link -->
<a name="Custom Data Assets-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Custom Data Assets

*Custom data assets refer to data entities or resources that are not automatically recognized or ingested by a data cataloging tool like Purview. These assets are typically specific to an organization's unique data landscape and may include various types of data sources.Custom data assets require manual or scripted processes to extract metadata, lineage information, and other relevant details and then register them within purview. These processes may involve parsing metadata from source systems, transforming data into compatible formats, and programmatically registering assets in the catalog.By ingesting custom data assets into the catalog, organizations can achieve a more comprehensive view of their data landscape, enabling better data governance, metadata management, and data discovery capabilities. It allows stakeholders to understand and leverage data assets across the organization, regardless of their origin or format.*

## Table of Contents

- [Overview](#overview)
- [Current Custom Import Systems](#current-custom-import-systems)
- [Importing Custom Assets](#importing-custom-assets)
- [Importing Custom Lineage Connections](#importing-custom-lineage-connections)
- [Troubleshooting](#troubleshooting)

### Overview

In many organizations, there are data sources that Purview does not currently support scanning directly. This could be due to various reasons such as proprietary formats, legacy systems, or niche applications. In such cases, custom import processes are necessary to bring the metadata and lineage information from these sources into Purview. Custom importing allows organizations to maintain a comprehensive data catalog that includes assets and connections from diverse sources, enabling better governance and understanding of their data landscape.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>

### Current Custom Import Systems

#### 1. PKMS:
   - **Description:** PKMS (Placeholder name for a custom system) is one of the data sources that Purview does not support scanning directly.
   - **Import Method:** We utilize a custom Python script [`pkms_lineage.py`](https://github.com/hanes-brands/Purview/blob/main/scripts/modules/lineage/pkms_lineage.py) to parse Excel exports provided by PKMS.
   - **Process:** The script extracts asset information from the Excel exports and creates corresponding assets in Purview, ensuring that attributes outlined in the exports are accurately represented.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>

#### 2. Salsify:
   - **Description:** Salsify (Another placeholder name) is another data source not supported by Purview scanning capabilities.
   - **Import Method:** Similar to PKMS, we employ a custom Python script [`salsify_lineage.py`](https://github.com/hanes-brands/Purview/blob/main/scripts/modules/lineage/salsify_lineage.py) to process Excel exports from Salsify.
   - **Process:** The script parses the Excel exports, extracting asset details, and programmatically creates assets in Purview, adhering to the attributes specified in the exports.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>

#### 3. Informatica:
   - **Description:** Informatica is a widely used data integration tool that requires custom handling for importing lineage connections into Purview.
   - **Import Method:** We receive XML exports from Informatica detailing the connections between assets.
   - **Process:** Using a dedicated Python script [`informatica_lineage.py`](https://github.com/hanes-brands/Purview/blob/main/scripts/modules/lineage/informatica_lineage.py), we interpret the XML exports to identify the relationships between assets. The script then creates corresponding connection assets in Purview, establishing the lineage between the related assets.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>

### Importing Custom Assets

For PKMS and Salsify, the import process involves:

1. Receiving Excel exports representing assets from the HBI.
2. Parsing the Excel files using custom Python scripts [`pkms_lineage.py`](https://github.com/hanes-brands/Purview/blob/main/scripts/modules/lineage/pkms_lineage.py) and [`salsify_lineage.py`](https://github.com/hanes-brands/Purview/blob/main/scripts/modules/lineage/salsify_lineage.py).
3. Creating assets in Purview programmatically based on the extracted information from the exports.
4. Ensuring that the attributes outlined in the exports are accurately reflected in the created assets.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>

### Importing Custom Lineage Connections

For Informatica, the import process includes:

1. Receiving XML exports from Informatica outlining the connections between assets.
2. Interpreting the XML exports using a dedicated Python script [`informatica_lineage.py`](https://github.com/hanes-brands/Purview/blob/main/scripts/modules/lineage/informatica_lineage.py).
3. Identifying the relationships between assets within the XML data.
4. Creating connection assets in Purview to represent the lineage between the related assets, as specified in the XML exports.

Custom importing of assets and lineage connections ensures that data from unsupported sources is integrated into Purview, allowing organizations to maintain a comprehensive and unified data catalog.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>

### Troubleshooting

If encountering issues during importing custom assets into purview:

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Custom Data Assets-top">Back to Top</a>)</p>



