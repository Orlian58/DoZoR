#!/bin/bash

iface=$1

python3 -m venv venv
source venv/bin/activate
venv/bin/pip install -r requirements.txt
venv/bin/python3 app/main.py $iface
