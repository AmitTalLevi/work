from flask import Flask, jsonify, request
import base64
import os
import time
from datetime import datetime

app = Flask(__name__)

TOKEN = None
TOKEN_EXPIRY = 0

LOG_FILE_PATH = "/logs/app.log"  # Log file path inside the container

def generate_token():
    token_bytes = os.urandom(24)
    token = base64.b64encode(token_bytes).decode('utf-8')
    return token

def log_request():
    # Log timestamp, IP, path, and method (GET/POST etc.)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr or 'unknown'
    method = request.method
    path = request.path
    log_line = f"{timestamp} | {ip} | {method} | {path}\n"
    # Write to log file
    with open(LOG_FILE_PATH, "a") as f:
        f.write(log_line)

@app.before_request
def before_request_func():
    log_request()

@app.route('/token')
def get_token():
    global TOKEN, TOKEN_EXPIRY
    current_time = time.time()
    if not TOKEN or current_time > TOKEN_EXPIRY:
        TOKEN = generate_token()
        TOKEN_EXPIRY = current_time + 600
    return jsonify({'token': TOKEN, 'expires_in_seconds': int(TOKEN_EXPIRY - current_time)})

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
