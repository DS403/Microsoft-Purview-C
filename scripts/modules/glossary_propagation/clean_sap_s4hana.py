##! /usr/bin/env python3

# Function Imports
# ---------------

from pyapacheatlas.core import AtlasEntity ,AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.readers import ExcelConfiguration,ExcelReader
from utils import get_credentials,create_purview_client
from pyapacheatlas.core.glossary import *

# Imports
# ---------------

import pandas as pd
import json
from pathlib import Path
import random
import string
import time

# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
prod_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

def fetch_display_name(file_path):
	with open(file_path, 'r') as file:
		data = json.load(file)
		if 'Packages' in file_path:
			Display_Text = data['Display_Text']
			return Display_Text
		elif 'Application_Components' in file_path:
			Display_Text = list(data.values())
			return Display_Text
	

def delete_SAP_S4_Hana_Packages(client,qualified_name,type_name):
	Display_Text=fetch_display_name('SAP_S4_Hana_Packages.json')
	Failed_Display_Text=[]
	for i in Display_Text:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text.append(i)

	Failed_Display_Text_two=[]
	for i in Failed_Display_Text:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text_two.append(i)
	print(Failed_Display_Text_two)

def delete_SAP_S4_Hana_Sub_Application_Components(client,qualified_name,type_name):
	Display_Text=fetch_display_name('SAP_S4_Hana_Sub_Application_Components.json')
	Failed_Display_Text=[]
	for i in Display_Text:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text.append(i)
	print(Failed_Display_Text)

	Failed_Display_Text_two=[]
	for i in Failed_Display_Text:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text_two.append(i)
	print(Failed_Display_Text_two)

	Failed_Display_Text_three=[]
	for i in Failed_Display_Text_two:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text_three.append(i)
	print(Failed_Display_Text_three)

def delete_SAP_S4_Hana_Application_Components(client,qualified_name,type_name):
	Display_Text=fetch_display_name('SAP_S4_Hana_Application_Components.json')
	Failed_Display_Text=[]
	for i in Display_Text:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text.append(i)
	print(Failed_Display_Text)

	Failed_Display_Text_two=[]
	for i in Failed_Display_Text:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text_two.append(i)
	print(Failed_Display_Text_two)

	Failed_Display_Text_three=[]
	for i in Failed_Display_Text_two:
		try:
			fully_qualified_name=qualified_name+i
			client.delete_entity(qualifiedName=fully_qualified_name, typeName=type_name)
		except:
			Failed_Display_Text_three.append(i)
	print(Failed_Display_Text_three)

            

#delete_SAP_S4_Hana_Packages(qa_client,'sap_s4hana://vhhbrds4ci_DS4_00_100/','sap_s4hana_package')
#delete_SAP_S4_Hana_Sub_Application_Components(qa_client,'sap_s4hana://vhhbrqs4ci_QS4_00_100/','sap_s4hana_application_component')
delete_SAP_S4_Hana_Application_Components(qa_client,'sap_s4hana://vhhbrmd1ci_MD1_00_220/','sap_s4hana_application_component')
