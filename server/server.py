from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

start_time = time.time()
pending_duration = 10  # Configurable duration for the job to stay pending
status_outcomes = ["completed", "error"]  # Possible end results

@app.route('/status', methods=['GET'])
def get_status():
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time < pending_duration:
        return jsonify({"result": "pending"})
    else:
        return jsonify({"result": random.choice(status_outcomes)})

if __name__ == "__main__":
    app.run(debug=True)
