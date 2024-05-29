#!/bin/bash
pip install -r requirements.txt

python3 module/solvesqliteissue.py
python3 module/createdb.py