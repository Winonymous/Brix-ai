__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import socket
import subprocess
import time

# import chromadb
chroma_port = 12345  # Replace with the actual port number

# Start chroma server# Python code to be executed before starting the chroma process
python_code = '__import__("pysqlite3"); import sys; sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")'

python_process = subprocess.Popen(['python', '-c', python_code])
python_process.wait()

# # Start ChromaDB server with the Python code executed first
command = ['chroma', 'run', '--path', 'Resource/chroma_db', '--port', str(chroma_port)]

chroma_process = subprocess.Popen(command)

# Wait for the localhost server to be ready
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
 