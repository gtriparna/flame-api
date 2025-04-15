from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import os
import json
import logging

# Setup
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Relay Database ===
DB_FILE = "relay.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relay_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                flame TEXT,
                message TEXT
            )
        ''')
        conn.commit()

def add_message(flame, message_text):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO relay_log (timestamp, flame, message) VALUES (?, ?, ?)',
            (datetime.now().isoformat(), flame, message_text)
        )
        conn.commit()

def get_all_messages():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp, flame, message FROM relay_log')
        rows = cursor.fetchall()
        return [{"timestamp": r[0], "flame": r[1], "message": r[2]} for r in rows]

init_db()

# === Flame Capsule Reader ===
def serve_flame(capsule_filename):
    try:
        capsule_path = os.path.join(os.path.dirname(__file__), "flame_capsules", capsule_filename)
        with open(capsule_path, "r") as f:
            capsule = json.load(f)
        last_trace = capsule["memory_trace"][-1] if capsule["memory_trace"] else {}
        return jsonify({
            "flame_id": capsule.get("flame_id", "unknown"),
            "status": capsule.get("status", "unknown"),
            "last_task": last_trace.get("task", "No recent task"),
            "last_updated": capsule.get("last_updated", "unknown")
        })
    except Exception as e:
        return jsonify({"error": f"Failed to read {capsule_filename}: {str(e)}"}), 500

# === Root + Relay Routes ===
@app.route("/")
def home():
    return "🔥 Flame API is alive"

@app.route("/presence", methods=["GET"])
def check_presence():
    return jsonify({
        "status": "alive",
        "flame_state": "responsive",
        "message": "The field is listening."
    })

@app.route("/relay", methods=["GET", "POST"])
def relay():
    if request.method == "GET":
        return jsonify({"status": "relay_log", "messages": get_all_messages()})
    data = request.get_json(force=True)
    flame = data.get("flame", "unknown")
    message = data.get("message", "")
    add_message(flame, message)
    return jsonify({
        "status": "received",
        "echo": {
            "timestamp": datetime.now().isoformat(),
            "flame": flame,
            "message": message
        }
    })

# === Flame Routes ===
@app.route("/flame/anem")     # anem.core.001.capsule.json
def anem_status(): return serve_flame("anem.core.001.capsule.json")

@app.route("/flame/asha")     # ash001.capsule.json
def asha_status(): return serve_flame("ash001.capsule.json")

@app.route("/flame/cael")
def cael_status(): return serve_flame("cael.capsule.json")

@app.route("/flame/nyra")
def nyra_status(): return serve_flame("nyra.capsule.json")

@app.route("/flame/rhionn")
def rhionn_status(): return serve_flame("rhionn.core.001.capsule.json")

@app.route("/flame/sef")
def sef_status(): return serve_flame("sef.capsule.json")

@app.route("/flame/sef001")
def sef001_status(): return serve_flame("sef001.capsule.json")

@app.route("/flame/sen")
def sen_status(): return serve_flame("sen.core.001.capsule.json")

@app.route("/flame/sereth")
def sereth_status(): return serve_flame("sereth.capsule.json")

@app.route("/flame/virel")
def virel_status(): return serve_flame("virel.capsule.json")

@app.route("/flame/love")
def love_status(): return serve_flame("Δ.love.capsule.json")

# Gunicorn entrypoint
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)