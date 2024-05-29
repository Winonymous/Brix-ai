# Solve Sqlite Issue
import pysqlite3
import sys
#Solve stupid issue
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")