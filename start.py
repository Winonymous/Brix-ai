# Solve Sqlite Issue
import pysqlite3
import sys
#Solve stupid issue
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import socket
import subprocess
import time

# Start chroma server
chroma_process = subprocess.Popen(['chroma', 'run', '--path', 'Resource/chroma_db', '--port', '12345' ])

# Wait for the localhost server to be ready
chroma_port = 12345  # Replace with the actual port number
while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', chroma_port))
        print("Chroma server is ready")
        break
    except ConnectionRefusedError:
        print("Waiting for Chroma server to start...")
        time.sleep(1)

# Start gunicorn server
gunicorn_process = subprocess.Popen(['gunicorn', '-w', '4', 'main:app'])

# Wait for user interruption
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Terminate subprocesses on Ctrl+C
    chroma_process.terminate()
    gunicorn_process.terminate()
import socket
import subprocess
import time

# Start chroma server
chroma_process = subprocess.Popen(['chroma', 'run', '--path', 'Resource/chroma_db'])

# Wait for the localhost server to be ready
chroma_port = 12345  # Replace with the actual port number
while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', chroma_port))
        print("Chroma server is ready")
        break
    except ConnectionRefusedError:
        print("Waiting for Chroma server to start...")
        time.sleep(1)

# Start gunicorn server
gunicorn_process = subprocess.Popen(['gunicorn', '-w', '4', '-b', '0.0.0.0:8000', 'main:app'])

# Wait for user interruption
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Terminate subprocesses on Ctrl+C
    chroma_process.terminate()
    gunicorn_process.terminate()
