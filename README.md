# video_translation_status_project

This project simulates a backend server for video translation and a client library that can poll the server for job status. 

## Server

The server is a simple Flask application that mimics a job status backend.

### Run the server:

```bash
cd server
pip install -r requirements.txt
python -m unittest tests/test_integration.py