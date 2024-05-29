#!/bin/bash

python -c '__import__("pysqlite3"); import sys; sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")'

chroma run --path Resource/chroma_db --port 12345