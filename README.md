<!-- Improved compatibility of Back to Top link -->
<a name="readme-top"></a>

<!-- PROJECT TITLE AND OVERVIEW -->

<center>

# Microsoft Purview

*Our project focuses on leveraging Microsoft Purview to establish a comprehensive Data Catalog and Data Lineage infrastructure. Through diligent scanning of diverse data sources, we seamlessly integrate data into Purview, ensuring a centralized and organized repository. We also create a detailed business glossary, defining key terms, and establishing a structured collection hierarchy. This initiative not only enhances data accessibility but also facilitates a clear understanding of data lineage, promoting efficient data management and governance within the organization.*

<!-- INCLUDE AN ARCHITECTURE DIAGRAM HERE -->

</center>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#design-considerations">Design Considerations</a></li>
    <li><a href="#solution-overview">Solution Overview</a></li>
    <li><a href="#technical-specifications">Technical Specifications</a></li>
    <li><a href="#datasets">Datasets</a></li>
    <li><a href="#future-enhancements">Future Enhancements</a></li>
    <li><a href="#support-information">Support Information</a></li>
  </ol>
</details>

<!-- DESIGN CONSIDERATIONS -->

# Design Considerations

| Name | Description | Overview | 
| ---- | ---- | ---- | 
| Solution overview | Our project leverages Microsoft Purview to create a robust Data Catalog and Data Lineage infrastructure. By meticulously scanning varied data sources, we seamlessly integrate data into Purview, establishing a centralized and organized repository. Additionally, our initiative involves developing a detailed business glossary, defining key terms, and structuring a collection hierarchy to enhance data accessibility and promote efficient data management and governance within the organization. |   |
| Problem Statement | We aim to work with Purview using Pyapacheatlas, but many essential functionalities are missing, leading us to develop our own solution in this repository. There is a lack of demos on how to use pyapacheatlas, making it challenging to figure out how to develop lineage and catalog features. |   | 
| Business Goals and Objectives | 1. Establishing Comprehensive Data Management: Utilize Microsoft Purview to create a robust Data Catalog and Data Lineage infrastructure, ensuring a centralized repository for efficient data management.</br>2. Enhancing Data Accessibility: Through diligent scanning of diverse data sources, seamlessly integrate data into Purview to enhance accessibility across the organization.</br>3. Defining Business Terminology: Craft a nuanced business glossary, defining key terms to foster a common understanding of data within the organization.</br>4. Structuring Information Hierarchy: Establish a structured collection hierarchy to organize and manage data effectively.</br>5. Promoting Data Governance: Facilitate a clear understanding of data lineage, promoting efficient data governance practices within the organization.  |   |
| Project Deliverables | Our primary deliverables encompass the creation of glossary terms across all data assets. This involves meticulously crafting glossary terms to ensure a standardized understanding of critical business terminology. Additionally, we commit to developing lineage, providing transparent insights into the data flow and dependencies. The project also includes the establishment of a structured collection hierarchy, enhancing the organization and accessibility of data assets. Through these deliverables, we aim to fortify data governance, streamline accessibility, and foster a cohesive understanding of our data landscape within the organization. | | 

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

<!-- SOLUTION OVERVIEW -->

# Solution Overview

A complete review of the project to provide context for some of the design decisions, explanation for some of the technical implementations and other key pieces of information that are essential to understanding the work contained in this repository. This includes but is not limited to the following points:

- **Describe the features:** Our project encompasses three core features: Data Catalog, Glossary, and Data Lineage. The Data Catalog centralizes diverse data sources using Microsoft Purview, promoting seamless data accessibility. The Glossary involves crafting 800 terms, standardizing business terminology, while Data Lineage offers transparent insights into data flow and dependencies, enhancing data governance.</br>**Benefits:**</br>-*Data Catalog:* Simplifies data discovery and enhances accessibility.</br>-*Glossary:* Fosters a common understanding with standardized business terminology.</br>-*Data Lineage:* Provides valuable insights for robust data governance and decision-making..
- **Include project-specific information:** This initiative is integral to our data governance strategy, specifically addressing data quality, data cataloging, and data lineage. Aligned with our commitment to excellence, this project contributes to optimizing data management practices within our organization.
- **Execution Flow:** The project execution involves scanning and integrating data into Microsoft Purview, crafting a detailed glossary, developing lineage, and establishing a structured collection hierarchy. This seamless flow aims to fortify data governance, enhance accessibility, and streamline our data landscape.
- **Repository Structure:** Our repository adopts a structured approach with three main folders:</br> -*Scripts Folder:* This section serves as the code repository, containing the actual scripts along with input and output files. All coding components are neatly organized within this folder, facilitating easy access and maintenance of the project's core functionality.</br> 
-*Examples Folder:*
In this segment, we provide practical examples corresponding to each code snippet. These examples serve as valuable resources for users, offering a hands-on understanding of how to implement and adapt the code for specific scenarios. This folder enhances the repository's user-friendliness and ensures clarity in code usage.</br> 
-*Docs Folder:* The documentation hub, housed within this folder, encapsulates all project-related documents. Ranging from project specifications to development processes, this comprehensive collection aids users and contributors in understanding the project's nuances and contributes to a smoother development experience.

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>


