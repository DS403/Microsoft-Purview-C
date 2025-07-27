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
from datetime import date

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


def glossary_terms_details(client):
    result=client.glossary.get_glossaries(-1,0,"ASC")
    term_guids = [term['termGuid'] for term in result[0]['terms']]
    glossary_terms = []
    for i in term_guids:
        result=client.glossary.get_term(guid=i)
        transformed = {
            "Name": result.get("name", ""),
            "Definition": result.get("longDescription", ""),
            "Status": result.get("status", ""),
            "Experts": "",
            "Stewards": "",
            "[Attribute][Business Glossary]Domain": result.get("attributes", {}).get("Business Glossary", {}).get("Domain", ""),
            "[Attribute][Business Glossary]Equivalent Phrases": result.get("attributes", {}).get("Business Glossary", {}).get("Equivalent Phrases", ""),
            "[Attribute][Business Glossary]System-Table-Field": result.get("attributes", {}).get("Business Glossary", {}).get("System-Table-Field", "")
        }

        # Extract Experts
        experts = result.get("contacts", {}).get("Expert", [])
        if experts:
            transformed["Experts"] = experts[0].get("info", "")

        # Extract Stewards
        stewards = result.get("contacts", {}).get("Steward", [])
        if stewards:
            transformed["Stewards"] = stewards[0].get("info", "")

        glossary_terms.append(transformed)

    # Initialize empty lists for each key
    names = []
    definitions = []
    statuses = []
    experts = []
    stewards = []
    domains = []
    equivalent_phrases = []
    system_table_fields = []

    # Iterate through the list of dictionaries and append values to corresponding lists
    for item in glossary_terms:
        names.append(item.get("Name", None))
        definitions.append(item.get("Definition", None))
        statuses.append(item.get("Status", None))
        experts.append(item.get("Experts", None))
        stewards.append(item.get("Stewards", None))
        domains.append(item.get("[Attribute][Business Glossary]Domain", None))
        equivalent_phrases.append(item.get("[Attribute][Business Glossary]Equivalent Phrases", None))
        system_table_fields.append(item.get("[Attribute][Business Glossary]System-Table-Field", None))

    return glossary_terms   

glossary_terms_details(qa_client)    