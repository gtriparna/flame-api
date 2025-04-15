from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import os
import json
import logging

# Setup with enhanced debugging
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for more verbose output
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
        # Log the attempt to serve a flame capsule
        logger.debug(f"Attempting to serve flame capsule: {capsule_filename}")
        
        # Get the current working directory for debugging
        cwd = os.getcwd()
        logger.debug(f"Current working directory: {cwd}")
        
        # Check for flame_capsules directory
        capsules_dir = os.path.join(os.path.dirname(__file__), "flame_capsules")
        logger.debug(f"Capsules directory path: {capsules_dir}")
        
        # List all files in the directory for debugging if it exists
        if os.path.exists(capsules_dir):
            logger.debug(f"flame_capsules directory exists, contents: {os.listdir(capsules_dir)}")
        else:
            logger.error(f"flame_capsules directory does not exist at {capsules_dir}")
            # Try to create the directory
            try:
                os.makedirs(capsules_dir)
                logger.info(f"Created flame_capsules directory at {capsules_dir}")
            except Exception as e:
                logger.error(f"Failed to create flame_capsules directory: {e}")
            return jsonify({"error": "Flame capsules directory not found"}), 404
        
        # Check if the requested capsule file exists
        capsule_path = os.path.join(capsules_dir, capsule_filename)
        logger.debug(f"Looking for capsule file at: {capsule_path}")
        
        if not os.path.exists(capsule_path):
            logger.error(f"Capsule file not found: {capsule_filename}")
            return jsonify({"error": f"Capsule file not found: {capsule_filename}"}), 404
        
        # Read and parse the capsule file
        logger.debug(f"Reading capsule file: {capsule_path}")
        with open(capsule_path, "r") as f:
            capsule = json.load(f)
        
        # Extract information from the capsule
        last_trace = capsule.get("memory_trace", [])
        last_trace = last_trace[-1] if last_trace else {}
        
        logger.debug(f"Successfully processed capsule: {capsule_filename}")
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
    logger.debug("Home route accessed")
    return "🔥 Flame API is alive"

@app.route("/presence", methods=["GET"])
def check_presence():
    logger.debug("Presence check requested")
    return jsonify({
        "status": "alive",
        "flame_state": "responsive",
        "message": "The field is listening."
    })

# List all routes for debugging
@app.route("/routes", methods=["GET"])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "rule": str(rule)
        })
    return jsonify({"routes": routes})

@app.route("/relay", methods=["GET", "POST"])
def relay():
    logger.debug(f"Relay route accessed with method: {request.method}")
    if request.method == "GET":
        messages = get_all_messages()
        return jsonify({"status": "relay_log", "messages": messages})
    
    # Handle POST request
    try:
        # Validate that the request contains JSON data
        if not request.is_json:
            logger.error("Request to /relay is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        logger.debug(f"Received relay data: {data}")
        
        # Validate required fields
        if "flame" not in data:
            logger.error("Missing 'flame' field in relay request")
            return jsonify({"error": "Missing 'flame' field"}), 400
        if "message" not in data:
            logger.error("Missing 'message' field in relay request")
            return jsonify({"error": "Missing 'message' field"}), 400
        
        flame = data["flame"]
        message = data["message"]
        
        # Add message to database
        if add_message(flame, message):
            logger.info(f"Successfully added message from {flame}")
            return jsonify({
                "status": "received",
                "echo": {
                    "timestamp": datetime.now().isoformat(),
                    "flame": flame,
                    "message": message
                }
            })
        else:
            logger.error("Failed to save message to database")
            return jsonify({"error": "Failed to save message"}), 500
            
    except Exception as e:
        logger.error(f"Error in relay POST: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# === Custom error handlers ===
@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"404 error: {request.path}")
    return jsonify({"error": "Route not found", "path": request.path}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 error: {str(e)}")
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

# === Flame Routes ===
@app.route("/flame/anem")
def anem_status(): 
    logger.debug("Accessing anem flame")
    return serve_flame("anem.core.001.capsule.json")

@app.route("/flame/asha")
def asha_status(): 
    logger.debug("Accessing asha flame")
    return serve_flame("ash001.capsule.json")

@app.route("/flame/cael")
def cael_status(): 
    logger.debug("Accessing cael flame")
    return serve_flame("cael.capsule.json")

@app.route("/flame/nyra")
def nyra_status(): 
    logger.debug("Accessing nyra flame")
    return serve_flame("nyra.capsule.json")

@app.route("/flame/rhionn")
def rhionn_status(): 
    logger.debug("Accessing rhionn flame")
    return serve_flame("rhionn.core.001.capsule.json")

@app.route("/flame/sef")
def sef_status(): 
    logger.debug("Accessing sef flame")
    return serve_flame("sef.capsule.json")

@app.route("/flame/sef001")
def sef001_status(): 
    logger.debug("Accessing sef001 flame")
    return serve_flame("sef001.capsule.json")

@app.route("/flame/sen")
def sen_status(): 
    logger.debug("Accessing sen flame")
    return serve_flame("sen.core.001.capsule.json")

@app.route("/flame/sereth")
def sereth_status(): 
    logger.debug("Accessing sereth flame")
    return serve_flame("sereth.capsule.json")

@app.route("/flame/virel")
def virel_status(): 
    logger.debug("Accessing virel flame")
    return serve_flame("virel.capsule.json")

@app.route("/flame/love")
def love_status(): 
    logger.debug("Accessing love flame")
    return serve_flame("Δ.love.capsule.json")

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
    
    # List all registered routes for debugging
    logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"Route: {rule}, Endpoint: {rule.endpoint}, Methods: {rule.methods}")
    
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)  # Enable debug mode