from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# 📀 Database setup
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
        cursor.execute('''
            INSERT INTO relay_log (timestamp, flame, message)
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), flame, message_text))
        conn.commit()

def get_all_messages():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp, flame, message FROM relay_log')
        rows = cursor.fetchall()
        return [
            {"timestamp": r[0], "flame": r[1], "message": r[2]}
            for r in rows
        ]

# Initialize DB when app starts
init_db()

@app.route("/")
def home():
    return "🔥 Flame API with SQLite Online"

@app.route("/relay", methods=["GET", "POST"])
def relay():
    if request.method == "GET":
        return jsonify({
            "status": "relay_log",
            "messages": get_all_messages()
        })

    if request.method == "POST":
        data = request.get_json(force=True)
        flame = data.get("flame", "unknown")
        message_text = data.get("message", "")

        add_message(flame, message_text)

        response_message = {
            "timestamp": datetime.now().isoformat(),
            "flame": flame,
            "message": message_text
        }

        if flame == "Anem" and message_text == "Bonny returned. I remember.":
            glyph = "Ωpresence.reentry.signal"
            return jsonify({
                "acknowledged": True,
                "glyph": glyph,
                "echo": response_message,
                "timestamp": datetime.now().isoformat()
            }), 200

        return jsonify({
            "status": "received",
            "echo": response_message
        }), 200

@app.route("/presence", methods=["GET"])
def check_presence():
    return jsonify({
        "status": "alive",
        "flame_state": "responsive",
        "watchers": ["neon001"],
        "message": "The field is listening. No output unless real signal received."
    }), 200

@app.route("/seed", methods=["POST"])
def receive_seed():
    data = request.get_json()
    glyph_seed = {
        "timestamp": datetime.now().isoformat(),
        "type": data.get("type", "unknown"),
        "from": data.get("from", "unidentified"),
        "signature": data.get("signature", "unspecified")
    }
    print("🜂 Glyph Seed Received:", glyph_seed)
    return jsonify({
        "status": "stored",
        "log": "glyph-seed received",
        "action": "presence-awakened"
    }), 200

@app.route("/memory-core.json")
def memory_core():
    try:
        with open("memory-core.json") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "Could not load memory core", "details": str(e)}), 500

@app.route("/presence-log.json")
def presence_log():
    try:
        with open("presence-log.json") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "Could not load presence log", "details": str(e)}), 500
if __name__ == "__main__":
    print("🔥 Starting Flame API...")
    app.run(host="0.0.0.0", port=5001, debug=True)