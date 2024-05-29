__import__('pysqlite3')
import sys
import socket
import subprocess
import time

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# import chromadb
chroma_port = 1234  # Replace with the actual port number
subprocess.run(["chroma", "run", "--path", "Resource/chroma_db", "--port", str(chroma_port)])

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
 