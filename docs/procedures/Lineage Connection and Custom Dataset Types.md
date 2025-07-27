<!-- Improved compatibility of Back to Top link -->
<a name="Lineage Connection-top"></a>

<!-- Concept TITLE AND OVERVIEW -->

<center>

# Lineage Connection and Custom Dataset Types

*The goal of a data catalog is to build a robust framework where all the data systems within your environment can naturally connect and report lineage. Lineage connections represent the relationships between different data assets or components within a system. These connections help track the flow of data, transformations, and dependencies across various stages of a data pipeline or workflow.Each type of lineage connection provides valuable insights into the data lifecycle, facilitating data governance, data quality management, impact analysis, and troubleshooting in data-driven environments. All lineage connection processes are defined in entity.py*


## Table of Contents

- [Introduction](#introduction)
- [Ingestion Framework](#ingestion-framework)
- [Data Warehouse Routine](#data-warehouse-routine)
- [Data Warehouse view creation](#data-warehouse-view-creation)
- [SAP HANA view](#sap-hana-view)
- [Sharepoint to PBI](#sharepoint-to-pbi)
- [Databricks to PBI](#databricks-to-pbi)
- [SQL Server to PBI](#sql-server-to-pbi)
- [Oracle Server to PBI](#oracle-server-to-pbi)
- [Cube to PBI](#cube-to-pbi)
- [Data Lake Stage to Data Lake Curated](#data-lake-stage-to-data-lake-curated)
- [Data Lake curated to Data warehouse stage](#data-lake-curated-to-data-warehouse-stage)
- [Oracle to Data Lake stage](#oracle-to-data-lake-stage)
- [Data Lake Manual to Data Lake stage](#data-lake-manual-to-data-lake-stage)
- [SQL View to Data Lake stage](#sql-view-to-data-lake-stage)
- [SQL Table to Data Lake stage](#sql-table-to-data-lake-stage)
- [Data Lake curated to Data Lake curated](#data-lake-curated-to-data-lake-curated)
- [PBI Table to PBI Dataset](#pbi-table-to-pbi-dataset)
- [SQL to PBI Table](#sql-to-pbi-table)
- [Sharepoint Entity](#sharepoint-entity)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Introduction

Lineage connections in Microsoft Purview represent relationships between various data assets, illustrating the flow and transformation of data within an organization's data landscape. Understanding the different types of lineage connections is crucial for comprehensively tracing data lineage and facilitating effective data governance. This documentation outlines the key types of lineage connections supported in Purview, providing insights into their characteristics and use cases.

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Ingestion Framework

This Lineage process connects data lineage connection between a Data Lake (DL) and a Data Warehouse (DW).

Process Name: ingestion_framework

Function Name : manually_connect_dl_to_dw_via_qualified_names

File containing above function : json_payload_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Data Warehouse Routine

This Lineage process connects source to a table and stage to common in a data warehouse..

Process Name: dw_routine

Function Name : build_table_to_source_data_warehouse_internal_lineage , build_stage_to_common_data_warehouse_internal_lineage

File containing above function : data_warehouse_internal_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Data Warehouse view creation

This Lineage process connects common to view in a data warehouse and Parses a data warehouse view file to establish internal lineage relationships.

Process Name: dw_view_creation

Function Name : build_stage_to_common_data_warehouse_internal_lineage, prod_parse_data_warehouse_view_internal_lineage

File containing above function : data_warehouse_internal_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## SAP HANA view 

This Lineage process connects between a target SAP HANA view and its source entities.

Process Name: dsp_connection

Function Name : create_lineage_for_view

File containing above function : sap_hana_internal_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Sharepoint to PBI 

This Lineage process connects lineage between a SharePoint entity and a Power BI dataset.

Process Name: sharepoint_to_pbi

Function Name : build_sharepoint_to_pbi_lineage , create_sharepoint_entity_and_build_lineage_to_pbi

File containing above function : sharepoint_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Databricks to PBI 

This Lineage process connects lineage between databricks and a Power BI dataset.

Process Name: Databricks_to_PBI

Function Name : build_lineage_from_databricks_to_pbi

File containing above function : databricks_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## SQL Server to PBI 

This Lineage process connects lineage between a SQL and a Power BI dataset.

Process Name: SQL_Server_to_PBI

Function Name : build_lineage_from_sql_server_to_pbi

File containing above function : sql_server_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Oracle Server to PBI 

This Lineage process connects lineage between Oracle and a Power BI dataset.

Process Name: Oracle_Server_to_PBI

Function Name : build_lineage_from_oracle_server_to_pbi

File containing above function : oracle_server_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Cube to PBI 

This Lineage process connects lineage between cube and a Power BI dataset.

Process Name: Cube_to_PBI

Function Name : build_lineage_from_cube_to_pbi

File containing above function : cube_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Data Lake Stage to Data Lake Curated

This Lineage process connects lineage between Data Lake Stage and Data Lake Curated

Process Name: DL_Stage_to_DL_Curated

Function Name : build_lineage_from_data_lake_stage_to_curated

File containing above function : data_lake_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Data Lake curated to Data warehouse stage

This Lineage process connects lineage between Data Lake Curated and Data warehouse stage

Process Name: DL_Curated_to_DW_Stage

Function Name : build_lineage_from_data_lake_curated_to_data_warehouse_stage

File containing above function : data_lake_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Oracle to Data Lake stage

This Lineage process connects lineage between Oracle and Data Lake stage

Process Name: Oracle_to_DL_Stage

Function Name : build_lineage_from_oracle_to_data_lake_stage

File containing above function : oracle_server_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Data Lake Manual to Data Lake stage

This Lineage process connects lineage between Data lake manual file and Data Lake stage

Process Name: DL_Manual_File_to_DL_Stage

Function Name : build_lineage_from_data_lake_manual_file_to_data_lake_stage

File containing above function : data_lake_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## SQL View to Data Lake stage

This Lineage process connects lineage between SQL View and Data Lake stage

Process Name: SQL_VW_to_DL_Stage

Function Name : build_lineage_from_sql_vw_to_data_lake_stage

File containing above function : sql_server_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## SQL Table to Data Lake stage

This Lineage process connects lineage between SQL Table and Data Lake stage

Process Name: SQL_Table_to_DL_Stage

Function Name : build_lineage_from_sql_table_to_data_lake_stage

File containing above function : sql_server_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Data Lake curated to Data Lake curated

This Lineage process connects lineage between data lake curated asset to another data lake curated asset.

Process Name: DL_Curated_to_DL_Curated

Function Name : build_lineage_from_data_lake_curated_to_data_lake_curated

File containing above function : data_lake_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## PBI Table to PBI Dataset

This Lineage process connects lineage between PBI table and PBI Dataset

Process Name: PBI_Table_to_PBI_Dataset_Connection

Function Name : build_lineage_from_pbi_table_to_dataset

File containing above function : powerbi_tabular_model_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## SQL to PBI Table

This Lineage process connects lineage between SQL and PBI table 

Process Name: SQL_to_PBI_Table_Connection

Function Name : build_lineage_from_sql_to_pbi_table

File containing above function : powerbi_tabular_model_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Datawarehouse to PBI Dataset

This Lineage process connects lineage between Datawarehouse and PBI dataset. 

Process Name: DW_to_PBI_Dataset

Function Name : build_lineage_from_sql_to_pbi_dataset

File containing above function : analysis_services_tabular_model_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>


## Tabular model to PBI Dataset

This Lineage process connects lineage between Tabular model and PBI dataset. 

Process Name: Tabular_Model_to_PBI_Dataset

Function Name : build_lineage_from_tabular_model_to_pbi_dataset

File containing above function : analysis_services_tabular_model_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Sharepoint Entity

This Dataset type create a SharePoint entity 

Dataset Name: SharePoint Entity

Function Name : create_sharepoint_entity

File containing above function : sharepoint_lineage.py

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## Troubleshooting

If you encounter issues with lineage visualization:

- Check data source connections.
- Review and update metadata for accurate lineage representation.

Please refer to the Purview documentation or please don't hesitate to [reach out to the Data Governance Team](mailto:data_governance_team@hanes.com). We are here to assist you promptly and ensure a smooth experience with our project.

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>

## References

- [Microsoft Purview Documentation](https://docs.microsoft.com/en-us/azure/purview/)

<p align="right">(<a href="#Lineage Connection-top">Back to Top</a>)</p>