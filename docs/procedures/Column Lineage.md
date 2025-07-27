<!-- Improved compatibility of Back to Top link -->
<a name="Column Lineage-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Column Level Lineage

*Column-level lineage refers to the detailed tracking of data as it moves and transforms at the column level across different datasets, tables, or reports. It allows organizations to trace the flow of individual columns from their source to their destination, including any transformations or calculations applied along the way.*

## Table of Contents

- [Overview](#overview)
- [Key Benefits](#key-benefits)
- [Function Workflow](#function-workflow)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

### Overview

Column-level lineage provides a detailed view of how individual data columns move and transform across various datasets, tables, and processes within an organization’s data ecosystem. Unlike table-level lineage, which tracks the flow of entire datasets, column-level lineage focuses on the journey of specific columns, capturing how data is derived, transformed, and passed between systems.Column-level lineage is essential for organizations that require a deep understanding of their data flows, particularly in complex data environments where multiple transformations and aggregations occur.

<p align="right">(<a href="#Column Lineage-top">Back to Top</a>)</p>

### Key Benefits

#### 1. Granular Data Tracking: 
Allows organizations to trace the flow of specific data points, helping in understanding the origin, transformation, and destination of each column.

#### 2. Impact Analysis: 
Facilitates the assessment of how changes to a column in one system might impact downstream processes, reports, or data models.

#### 3. Compliance and Governance: 
Helps ensure that sensitive data is appropriately handled and that data flows comply with regulatory requirements.

#### 4. Root Cause Analysis: 
Provides insights into the source of data issues by pinpointing exactly where data changes or errors may have occurred in the pipeline.

<p align="right">(<a href="#Column Lineage-top">Back to Top</a>)</p>

### Function Workflow

#### 1. Excel Configuration and Reader Initialization:
The function begins by initializing an ExcelConfiguration object (ec) and an ExcelReader object (reader). These are used to configure and read the Excel file containing the column lineage mappings.

#### 2. Parsing and Updating Lineage:
The function calls reader.parse_update_lineage_with_mappings(file_path) to parse the Excel file. This method reads the file, extracts the necessary mappings, and updates the lineage data according to the specified transformations and relationships.

#### 3. Uploading Lineage Data:

The processed lineage entities (processes) are then uploaded to the client using client.upload_entities(processes). This step pushes the lineage data to the data catalog, making it available for visualization and analysis. We are currently supporting column lineage between SAP assets.

#### 4. Output:
The results of the upload operation are printed in a formatted JSON structure. This output provides a detailed view of the entities that were successfully uploaded, as well as any errors encountered during the process.

<p align="right">(<a href="#Column Lineage-top">Back to Top</a>)</p>

### Best Practices

#### 1. Validate Excel Mappings: 
Ensure that the Excel file is correctly formatted and contains all necessary columns for mapping source to destination fields.

#### 2. Error Handling: 
Implement additional error handling to manage potential issues during the upload process, such as invalid mappings or network errors.

#### 3. Regular Updates: 
Regularly update lineage information to reflect changes in data pipelines and schemas.

<p align="right">(<a href="#Column Lineage-top">Back to Top</a>)</p>

### Troubleshooting

If encountering issues in building column level lineage in purview:

#### 1. Upload Failures: 
If the upload fails, check the JSON output for error messages. Common issues include missing or incorrect entity types, invalid GUIDs, or network connectivity problems.

#### 2. Incorrect Mappings: 
Ensure that the mappings in the Excel file accurately represent the desired lineage. Incorrect mappings can lead to inaccurate lineage representations in the data catalog.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Column Lineage-top">Back to Top</a>)</p>



