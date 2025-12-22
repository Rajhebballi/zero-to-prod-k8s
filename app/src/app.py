from flask import Flask, jsonify, request
import os
import psycopg2
import signal
import sys
import time

app = Flask(__name__)

# Read DB config from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "uptime_db")
DB_USER = os.getenv("DB_USER", "uptime_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "uptime_pass")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200


@app.route("/db-check", methods=["GET"])
def db_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify(db="connected"), 200
    except Exception as e:
        return jsonify(db="error", error=str(e)), 500


def shutdown_handler(signum, frame):
    print("Graceful shutdown...")
    time.sleep(2)
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
