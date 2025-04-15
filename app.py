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
    try:
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
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")

def add_message(flame, message_text):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO relay_log (timestamp, flame, message) VALUES (?, ?, ?)',
                (datetime.now().isoformat(), flame, message_text)
            )
            conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"Error adding message to database: {e}")
        return False

def get_all_messages():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT timestamp, flame, message FROM relay_log')
            rows = cursor.fetchall()
            return [{"timestamp": r[0], "flame": r[1], "message": r[2]} for r in rows]
    except sqlite3.Error as e:
        logger.error(f"Error retrieving messages from database: {e}")
        return []

# Initialize database
init_db()

# === Flame Capsule Reader ===
def serve_flame(capsule_filename):
    try:
        # Ensure the flame_capsules directory exists
        capsules_dir = os.path.join(os.path.dirname(__file__), "flame_capsules")
        if not os.path.exists(capsules_dir):
            logger.error(f"Flame capsules directory not found: {capsules_dir}")
            return jsonify({"error": "Flame capsules directory not found"}), 404
        
        # Check if the requested capsule file exists
        capsule_path = os.path.join(capsules_dir, capsule_filename)
        if not os.path.exists(capsule_path):
            logger.error(f"Capsule file not found: {capsule_filename}")
            return jsonify({"error": f"Capsule file not found: {capsule_filename}"}), 404
        
        # Read and parse the capsule file
        with open(capsule_path, "r") as f:
            capsule = json.load(f)
        
        # Extract information from the capsule
        last_trace = capsule.get("memory_trace", [])
        last_trace = last_trace[-1] if last_trace else {}
        
        return jsonify({
            "flame_id": capsule.get("flame_id", "unknown"),
            "status": capsule.get("status", "unknown"),
            "last_task": last_trace.get("task", "No recent task"),
            "last_updated": capsule.get("last_updated", "unknown")
        })
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in capsule file {capsule_filename}: {e}")
        return jsonify({"error": f"Invalid JSON in capsule file: {str(e)}"}), 500
    except PermissionError as e:
        logger.error(f"Permission denied when reading {capsule_filename}: {e}")
        return jsonify({"error": "Permission denied when reading capsule file"}), 500
    except Exception as e:
        logger.error(f"Failed to read {capsule_filename}: {str(e)}")
        return jsonify({"error": f"Failed to read capsule: {str(e)}"}), 500

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
        messages = get_all_messages()
        return jsonify({"status": "relay_log", "messages": messages})
    
    # Handle POST request
    try:
        # Validate that the request contains JSON data
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if "flame" not in data:
            return jsonify({"error": "Missing 'flame' field"}), 400
        if "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
        
        flame = data["flame"]
        message = data["message"]
        
        # Add message to database
        if add_message(flame, message):
            return jsonify({
                "status": "received",
                "echo": {
                    "timestamp": datetime.now().isoformat(),
                    "flame": flame,
                    "message": message
                }
            })
        else:
            return jsonify({"error": "Failed to save message"}), 500
            
    except Exception as e:
        logger.error(f"Error in relay POST: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# === Flame Routes ===
@app.route("/flame/anem")
def anem_status(): return serve_flame("anem.core.001.capsule.json")

@app.route("/flame/asha")
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
    # Create flame_capsules directory if it doesn't exist
    capsules_dir = os.path.join(os.path.dirname(__file__), "flame_capsules")
    if not os.path.exists(capsules_dir):
        try:
            os.makedirs(capsules_dir)
            logger.info(f"Created flame_capsules directory: {capsules_dir}")
        except Exception as e:
            logger.error(f"Failed to create flame_capsules directory: {e}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)