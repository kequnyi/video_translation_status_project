import sys
import os

# Add the project root to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import time
from client.status_client import StatusClient

# Start the Flask server as a subprocess
server_process = subprocess.Popen(["python", "server/server.py"])
time.sleep(2)  # Give the server time to start

# Initialize the client
client = StatusClient("http://127.0.0.1:5000/status", initial_backoff=1, max_backoff=16)

# Poll the server and log the outcome
client.check_status(lambda status: print(f"Integration Test - Job finished with status: {status}"))

# Shutdown the server
server_process.terminate()
