#!/bin/bash

python3 -m venv venv
source venv/bin/activate
venv/bin/pip install -r requirements.txt
venv/bin/python3 create_db.py
venv/bin/python3 1.py
