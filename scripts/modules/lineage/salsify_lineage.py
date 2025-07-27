##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
from pyapacheatlas.core.util import GuidTracker
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader
from pyapacheatlas.core import  AtlasClassification


# Imports
# ---------------
from pathlib import Path
from fuzzywuzzy import fuzz


# Constants
# ---------------


# Global
# ---------------


# Functions
# ---------------



def parse_salsify(file):
    """
    For a given salsify excel file, iterate through all the rows and
    create column and entity name mappings.

    Parameters:
    - file: Path to the excel file for salsify 
    

    Returns:
    - salsify_dict: dictionary with all the entities and their
      columns with values
    """
    
    xls = pd.ExcelFile(file)
    salsify_dict={}

    #For each sheet in the given excel
    for sheet_name in xls.sheet_names:

        df = pd.read_excel(file, sheet_name=sheet_name)

        #For every given entity name
        for i in range(len(df['ID'])):

            #Consider only the columns with not nul values
            entity_df=df.iloc[i:i+1,:]
            entity_df=entity_df.dropna(axis=1)
            salsify_dict[df['ID'][i]]=[list(entity_df.columns)]
    return salsify_dict


def parse_salsify_dict(salsify_dict):
    
    """
    Take the output of parse salsify dictionary and create a dataframe
    with column mappings and save it to csv.

    Parameters:
    - salsify_dict: dictionary of salsify entities with columns
    

    Returns:
    - salsify_df: Parsed salsify dataframe which can be utilized for creating assets
    """
    entity_name_list=[]
    entity_column_list=[]

    for entity_name in salsify_dict:
        lst=salsify_dict[entity_name][0]
        lst.remove('ID')
        #removing strings like - en US , -en AU etc
        lst=[col_name.split('-')[0] for col_name in lst]
        entity_column_list.extend(lst)
        entity_name_list.extend([str(entity_name)]*(len(lst)))
        
    salsify_df=pd.DataFrame({'EntityName':entity_name_list,'EntityColumn':entity_column_list})
    return salsify_df

def get_salsify_hierarchy(file,hierarchy_cols):

    """
    Given a salsify file, get the hierarchy relationship between the colums
    Parameters:
    - file: Path to the excel file for salsify 
    --hierarchy_cols: List of the column names which contain hierarchy relationship
    

    Returns:
    - salsify_hierarchy_dict: Dictionary with parent, level and group name for each asset
    """

    xls = pd.ExcelFile(file)
    salsify_hierarchy_dict={
        'asset_name':[],
        'level_name':[],
        'parent_name':[],
        'group_parent':[]
    }

    #For each sheet in the given excel
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet_name)
        df=df.loc[:,hierarchy_cols]
        for i,row in df.iterrows():
            salsify_hierarchy_dict['asset_name'].append(row[hierarchy_cols[0]])
            if row[hierarchy_cols[1]]=='Parent Style':
                salsify_hierarchy_dict['level_name'].append('parent_style')
            elif row[hierarchy_cols[1]]=='Selling Style':
                salsify_hierarchy_dict['level_name'].append('selling_style')
            elif row[hierarchy_cols[1]]=='Color':
                salsify_hierarchy_dict['level_name'].append('color_style')
            elif row[hierarchy_cols[1]]=='Size':
                salsify_hierarchy_dict['level_name'].append('size_style')
                
            if type(row[hierarchy_cols[2]]) == float:
                salsify_hierarchy_dict['parent_name'].append('Root')
            else:
                salsify_hierarchy_dict['parent_name'].append(row[hierarchy_cols[2]])

            
            if row[hierarchy_cols[1]]=='Parent Style':
                current_parent=row[hierarchy_cols[0]]
            
            salsify_hierarchy_dict['group_parent'].append(current_parent)
        
        return salsify_hierarchy_dict


def get_salsify_descriptions(file_path, col_lst):
    
    """
    Given a salsify file, which contains the description for each column
    parse the file to get column names mapped to their descriptions
    Parameters:
    - file_path: Path to the excel file for salsify column description info
    --col_lst: List of the column we need to extract
    

    Returns:
    - df: Parsed dataframe with column and description info
    """
    df=pd.read_excel(file_path)
    df=df.loc[:,col_lst]
    return df



def create_classification(client,classification_name,classification_desc,attribut_name):
    
    """
    For the given classification, check if it do not exist and create a new.

    Parameters:
    - client : Purview client
    - classification_name : name of the classification to be created
    - classification_desc : description attribute to be added to classification
    - attribut_name : name of attribute to be added

    Returns:
    - None: Creates the classification for provided info
    """
    classification_set=get_all_classifications_names(client)
    if classification_name in classification_set:
        return
    else:
        # Define classification attributes
        classification_attrs = [
            {
                "name": attribut_name,
                "typeName": "string",
                "description": attribut_name
            
            }
        ]

        # Define classification type
        classification_def = {
        "classificationDefs": [
            {
                "name": classification_name,
                "description": classification_desc,
                "superTypes": [],
                "attributeDefs": classification_attrs
            }
                        ]
            }

        # Upload classification definition
        response = client.upload_typedefs(classification_def)
        return
        

def get_tab_dataset_relationship(record_guid,tab_guid):
     
         
    """
    For the given record_guid and tab_guid create a tabular relationship

    Parameters:
    - record_guid : guid of the record 
    - tab_guid : guid of the table 

    Returns:
    - tab_dataset_relationship: tabular relationship attribute
    """
     
    tab_dataset_relationship = {
                "typeName": "tabular_schema_datasets",
                "attributes": {},
                "guid": -100,
                "end1": {
                    "guid": record_guid
                },
                "end2": {
                    "guid": tab_guid
                }
            }
    return tab_dataset_relationship


def upload_column_entities(client,columns_to_add,record_guid,tab_guid):
                 
        """
        upload entities to the given client

        Parameters:
        - client : Purview client
        - columns_to_add : list of columns associated with the entity
        - record_guid : guid of the record 
        - tab_guid : guid of the table 

        Returns:
        - None: Uploads the entity to Purview client
        """
        column_assignment = client.upload_entities(columns_to_add)
        tab_dataset_relationship=get_tab_dataset_relationship(record_guid,tab_guid)
        relationship_assignment = client.upload_relationship(tab_dataset_relationship)  

        for key, value in column_assignment.get('guidAssignments').items():
            column_guid = value

            #try to create hierarchy with typeName dataset
            tab_column_relationship = {
                "typeName": "tabular_schema_columns",
                "attributes": {},
                "guid": -100,
                "end1": {
                    "guid": tab_guid
                },
                "end2": {
                    "guid": column_guid
                }
            } 
            relationship_assignment = client.upload_relationship(tab_column_relationship) 
            print("Column added for column guid " + str(column_guid))   


def get_entity_from_qualified_name(client, qualified_name):
    """
    Retrieves an entity from the catalog based on the provided qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The entity found based on the qualified name.
    """

    #get all the matching entities from search client
    entities_found = client.discovery.search_entities(query=qualified_name)

    #initialize an empty entity list
    entity_lst = []
    
    #checking for each entity in the entities received if it matches
    #Fuzzy ratio 100 means an exact match
    #If we get an exact match we pick that, otherwise the next best match

    for entity in entities_found:


        entity_dict={'entity_name':'' , 'entity_score':0,'entity_dict':{}}
        entity_dict['entity_name']=entity["qualifiedName"]
        entity_dict['entity_dict']=entity

        fuzz_score=fuzz.ratio(entity["qualifiedName"],qualified_name)
        
        entity_dict['entity_name']=max(entity_dict["entity_score"],fuzz_score)
        entity_lst.append(entity_dict)
        if fuzz_score==100 :
            if  (len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1):
                return entity

    
    best_score=0
    best_entity_dict={}
    for entity in entity_lst:
        if entity['entity_score']>best_score:
            best_score=entity['entity_score']
            best_entity_dict=entity['entity_dict']

    if best_entity_dict=={}:
        return 'No matching names were found'
    return best_entity_dict


def is_asset_exists(client,qualified_name):
    """
    Check if an asset is already present with the qualified name

    Args:
        qualified_name (str): The qualified name of the entity.
        client : Purview client

    Returns:
        boolean: True if asset is already present otherwise False
    """

    entity_match=get_entity_from_qualified_name(client, qualified_name)
    if type(entity_match)==str:
        return False
    elif type(entity_match)==dict:
        if qualified_name==entity_match['qualifiedName']:
            return True
        else:
            return False



def get_all_columns_from_qualified_name(client,qualified_name):
    
    """
    Check if an asset is already present with the qualified name

    Args:
        qualified_name (str): The qualified name of the entity.
        client : Purview client

    Returns:
        col_lst: List of all columns for the given assest
        returns empty list if no columns found
    """
    col_lst=[]
    if is_asset_exists(client,qualified_name):
        entity=get_entity_from_qualified_name(client,qualified_name)
        if 'id' in entity.keys():
            guid='id'
        if 'guid' in entity.keys():
            guid='guid'
        entity=client.get_entity(entity[guid])

        relationship_atrributes=entity.get("entities")[0].get("relationshipAttributes")
        if relationship_atrributes is None:
            return col_lst
        elif relationship_atrributes.get("tabular_schema") is None:
            return col_lst
        elif relationship_atrributes.get("tabular_schema").get("guid") is None:
            return col_lst
        else:
            tabular_schema_guid=relationship_atrributes.get("tabular_schema").get("guid")

        tabular_schema_details = client.get_entity(tabular_schema_guid).get("entities")[0]
        for column_attribute in tabular_schema_details["relationshipAttributes"]["columns"]:
            col_lst.append(column_attribute["displayText"])
        
    return col_lst
  

    
def delete_entity_by_qualified_name(client,entity):

    """
    Delete entity for a given purview client by entity 

    Args:
        client : Purview client
        entity : entity dictionary

    Returns:
       None : Delets the entity from the purview client
    """

    if 'id' in entity:
        guid='id'
    elif 'guid' in entity:
        guid='guid'
    client.delete_entity(entity[guid])
    print('Sucessfully deleted entity ...',entity['qualifiedName'])
    return 


def get_all_classifications_names(client):
    
        """
        Get all classification in the given purview client

        Args:
            client : Purview client

        Returns:
        classification_set : Set with all the classification names
        """
        classification_defs = client.get_all_typedefs()
        classification_set=set()
        for classification_defs in classification_defs['classificationDefs']:
                classification_set.add(classification_defs.get("name"))
        return classification_set       


def salsify_lineage(client, file_name):
    """
    Parses tables from an Excel file and uploads them to Apache Atlas in a predefined structure.

    Parameters:
    - client: Purview client for making Atlas API requests.
    - file_name (str): The name of the Excel file containing tables to be parsed.

    Returns:
    - None
    """
    #Read the salsify dataframe
    df = pd.read_csv(file_name)
    
    #assign previous group and asset value for checking condition, so that
    #if current and previous are same we will go in the loop,
    #otherwise not
    previous_group_name=''
    previous_asset_name=df.loc[0,'EntityName']
    current_asset_name=df.loc[0,'EntityName']
    n=len(df)
    index=0
    columns_to_add = []
    salsify_qualified_names_relationships={
        'EntityName':[],
        'level_name':[],
        'parent_name':[],
        'group_parent':[],
        'entity_qualified_name':[],
        'entity_guid':[]
    }
    
    while index<n:    
        previous_asset_name=df['EntityName'][index]
        current_group_name=df['group_parent'][index]
        guid_counter = -1002
        guid_tracker = GuidTracker(starting=guid_counter, direction='decrease')
        record_guid = guid_tracker.get_guid()

        #populate salsify dict
        salsify_qualified_names_relationships['EntityName'].append(df['EntityName'][index])
        salsify_qualified_names_relationships['level_name'].append(df['level_name'][index])
        salsify_qualified_names_relationships['parent_name'].append(df['parent_name'][index])
        salsify_qualified_names_relationships['group_parent'].append(df['group_parent'][index])
        delete_flag=0
        while current_asset_name==previous_asset_name and index<n:
            if previous_group_name!=current_group_name:
                #parent_qualified_name="salsify://parent_style/test37/"
                #selling_qualified_name="salsify://parent_style/selling_style/test37/"
                #color_qualified_name="salsify://parent_style/sellingstyle/color/test37/"

                parent_qualified_name="salsify://parent_style/"
                selling_qualified_name="salsify://parent_style/selling_style/"
                color_qualified_name="salsify://parent_style/sellingstyle/color/"
                previous_group_name=current_group_name

            # Define entity attributes

            #assign qualified names based on the type of style
            record_name=df['EntityName'][index]
            if df['level_name'][index]=='parent_style':
                #record_qualified_name = "salsify://parent_style/test37/" + record_name
                record_qualified_name = "salsify://parent_style/" + record_name
                parent_qualified_name=record_qualified_name
            
            if df['level_name'][index]=='selling_style':
                record_qualified_name = parent_qualified_name+"/"+df['level_name'][index]+"/" +record_name
                selling_qualified_name=record_qualified_name

            if df['level_name'][index]=='color_style':
                record_qualified_name = selling_qualified_name+"/color/" + record_name
                color_qualified_name=record_qualified_name

            if df['level_name'][index]=='size_style':
                record_qualified_name = color_qualified_name+"/size/"+ record_name

            
            #Before creating the asset check if it already exists
            is_exists_flag=is_asset_exists(client,record_qualified_name)

            #If asset is already created get all column names of the existing asset
            if is_exists_flag and delete_flag==0:
                print('Asset for qualified_name ',record_qualified_name,'  already exists ......')
                print('Deleting the existing entity .......')
                entity=get_entity_from_qualified_name(client,record_qualified_name)
                delete_entity_by_qualified_name(client,entity)
                print('Sucessfully deleted entity ...',entity['qualifiedName'])
                delete_flag=1
            
            delete_flag=1

          
            #creating entity for the givne record    
            record = AtlasEntity(record_name, "DataSet", record_qualified_name, record_guid)

            # Define classification attributes
            classification_name='Salsify'+current_group_name
            classification_desc='Classification for the salsify group belonging to '+current_group_name
            attribut_name=classification_name
            create_classification(client,classification_name,classification_desc,attribut_name)

            classification_attrs = {
                #"classification": "SalsifyTest"
                "classification": "Salsify"
                }

            classification = AtlasClassification(classification_name, attributes=classification_attrs)
            record.addClassification(classification)

            
            #get the column name and column name description
            column_name = df["EntityColumn"][index]
            column_description = df["EntityColumnDescription"][index]
            if type(column_description)==float:
                column_description=''
            
            column_qualified_name = record_qualified_name + "#" + column_name

            #get column guid
            column_guid = guid_tracker.get_guid()
            column = AtlasEntity(column_name, "column", column_qualified_name, column_guid, attributes={"type": "CHAR", "userDescription": column_description})
            column.addRelationship(table = record)
            columns_to_add.append(column)  
            index=index+1
            if index<n:
                current_asset_name=df.loc[index,'EntityName']
        
        #add current qualified name
        salsify_qualified_names_relationships['entity_qualified_name'].append(record_qualified_name)
        
            
            
        #create tabular schema with the current entity qualified name
        tabular_schema = AtlasEntity(record_name + " Tabular Schema", "tabular_schema", record_qualified_name + "/tabular_schema", guid_tracker.get_guid())
        tab_assgn = client.upload_entities([tabular_schema])
        tab_key, tab_guid = next(iter(tab_assgn.get('guidAssignments').items()))
        tabular_schema = AtlasEntity(record_name + " Tabular Schema", "tabular_schema", record_qualified_name + "/tabular_schema", tab_guid)
        results=client.get_entity(tab_guid)

        #upload entities
        record_assignment = client.upload_entities([record] + [tabular_schema])
        record_key, record_guid = next(iter(record_assignment.get('guidAssignments').items()))

        #add record guids
        salsify_qualified_names_relationships['entity_guid'].append(record_guid)
        
        
        upload_column_entities(client,columns_to_add,record_guid,tab_guid)

        print("Table created for: " + record_name + "\n\n\n")
        
        
        columns_to_add = []
    

    salsify_name_mapping_df=pd.DataFrame(salsify_qualified_names_relationships)
    return salsify_name_mapping_df

   


# Constants
# ---------------

def main():
    
    
    # #define file path
    path_to_file= r'C:\Users\Mansi.Choudhary\Documents\Hanes\salsify_export1.xlsx'
    #hierarchy_cols=['ID','salsify:data_inheritance_hierarchy_level_id','salsify:parent_id']
    hierarchy_cols=['ID','Hierarchy Level','Parent ID']

    # #get salsify_dict
    salsify_hierarchy_dict=get_salsify_hierarchy(path_to_file,hierarchy_cols)
    salsify_hierarchy_df=pd.DataFrame(salsify_hierarchy_dict)
    salsify_hierarchy_df.to_csv('salsify_hierarchy.csv')

    # #parse salsify data for extracting columns with values
    salsify_dict=parse_salsify(path_to_file)
    salsify_df=parse_salsify_dict(salsify_dict)

    # #get column description for the columns in salsify
    file_path  =r'C:\Users\Mansi.Choudhary\Documents\Hanes\export_All_Properties_Hanes_Inc.xlsx'
    col_description_columns=['salsify:id','salsify:name']
    salsify_desc_df=get_salsify_descriptions(file_path, col_description_columns)

    # #merge with the salsify df to combine each column name with corresponding description
    salsify_df=pd.merge(salsify_df,salsify_desc_df,
                        left_on='EntityColumn', right_on='salsify:id',how='left')
    salsify_df.drop('salsify:id',axis=1,inplace=True)
    salsify_df.rename(columns={'salsify:name': 'EntityColumnDescription'}, inplace=True)

    # #merge with hierarchy dataframe to get hierarchy values
    salsify_df=pd.merge(salsify_df,salsify_hierarchy_df,
                        left_on='EntityName', right_on='asset_name',how='left')
    
    # #save salsify column mapping
    salsify_df.to_csv('salsify_column_mappings.csv')
    

    #creating assets in purview
    """REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
    PROJ_PATH = Path(__file__).resolve().parent
    CREDS = get_credentials(cred_type= 'default')
    qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    file_name='salsify_mappings_test.csv'
    #file_name='salsify_column_mappings.csv'
    df=salsify_lineage(qa_client, file_name) 
    # #df.to_csv('salsify_name_mappings.csv')"""


  

    

    
   

    
 
   
    


    
    
        

if __name__ == '__main__':
    main()

