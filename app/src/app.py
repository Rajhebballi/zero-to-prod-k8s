from flask import Flask, jsonify, request
import signal
import sys
import time

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(force=True, silent=True)
    return jsonify(received=data), 200

def shutdown_handler(signum, frame):
    print("Graceful shutdown...")
    time.sleep(2)
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
