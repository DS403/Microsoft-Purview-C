<!-- Improved compatibility of Back to Top link -->
<a name="Collection-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Data Catalog Strategy

---

## 1. Introduction:
   The Data Catalog Strategy serves as a comprehensive framework for managing and utilizing data assets within our organization. This documentation outlines our approach to cataloging data, including the processes involved, the types of data sources scanned, and how we leverage the catalog for various purposes such as lineage development and data governance.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 2. Utilization of the Catalog:
   Our approach to utilizing the data catalog involves scanning different data sources to capture metadata of assets within the system. When a scan occurs, it retrieves essential information about the assets, such as their structure, attributes, and relationships. Subsequently, we enrich these assets with additional context and annotations to enhance their usability and relevance.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 3. Scanned Data Sources:
   Below is a list of data sources we have scanned, categorized by type:

   - **SAP Systems:**
     - SAP S4 HANA - MDG
     - SAP HANA - DSP
     - SAP S4 HANA - S4 Fashion

   - **Databases:**
     - Oracle Database
     - SQL Server

   - **Cloud Services:**
     - Azure Databricks
     - Azure Data lake Gen2
     - Azure Synapse Analytics
     - Azure Datawarehouse

   - **Other Sources:**
     - Power BI

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 4. Asset Collections:
   We organize assets into collections whenever feasible to facilitate better management and discovery. By grouping related assets together, users can easily navigate the catalog and find relevant data entities. Collections may be based on various criteria such as business function, data domain, or project affiliation.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 5. Glossary Management:
   Our data catalog includes a glossary section dedicated to capturing definitions related to tables and fields. This glossary serves as a centralized repository of data terminology, ensuring consistency and clarity in communication across the organization. Definitions are maintained and updated collaboratively to reflect changes in the data landscape.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 6. Definition of Assets:
   In our data catalog, an asset refers to any entity or resource that holds value or significance in the context of data management and analysis. This includes tables, columns, servers, databases, files, etc. By considering a broad range of assets, we ensure comprehensive coverage of our data landscape within the catalog.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 6. Metadata Ingested with an Asset:
   When an asset is scanned and ingested into the data catalog, various types of metadata are captured to provide a comprehensive understanding of its characteristics and usage. Some examples of metadata ingested with an asset include:

   - **Name:** The name of the asset, such as table name, file name, or server name.
   - **Description:** A brief description or summary of the asset's purpose and content.
   - **Data Type:** It specifies the data source to which the asset belongs. 
   Few of the types are:
      - SAP S/4Hana Table
      - SAP S/4Hana View
      - Sap Hana View
      - Sap Hana Table
      - Azure Data Lake Storage Gen2
      - Azure Dedicated SQL Pool Table
      - Power BI Dataset
      - Power BI Report
      - Hive Table
      - Oracle Package
      - Oracle Synonym
      - SQL View
      - SQL Table
   - **Contact:** The individual or team responsible for managing and maintaining the asset.
   - **Classification:** Annotations used to identify an attribute of an asset or column.
   - **Qualified Name :** A path that defines the location of an asset within its data source.
   - **Related Assets:** It Specifies any dependencies or relationships with other assets.
   - **Schema:** It brings the name of each column in the table and specifies the data type of each column ingested. 
   - **Usage Statistics:** Information on how frequently the asset is accessed or modified.
   - **Tags/Keywords:** Descriptive tags or keywords associated with the asset for search and categorization purposes.
   - **Related:** Related tab specifies the hierarchy of the table within the sap s4 hana server.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>

## 7. Conclusion:
   The Data Catalog Strategy outlines our systematic approach to managing data assets, from scanning diverse sources to enriching metadata and organizing assets into collections. By leveraging the catalog and its associated glossary, we empower users to discover, understand, and utilize data effectively, thereby enhancing data-driven decision-making and fostering a culture of data governance and stewardship.

<p align="right">(<a href="#Collection-top">Back to Top</a>)</p>
