#!/bin/bash

# Create a new virtual environment
virtualenv -p python3 .venv

# Activate the virtual environment
source .venv/bin/activate

# Install packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
