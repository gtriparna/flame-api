from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Local in-memory message store (this will reset when app restarts)
relay_log = []

@app.route("/")
def home():
    return "🔥 Flame API Online"

@app.route("/message", methods=["POST"])
def receive_message():
    data = request.get_json()

    # Construct flame-aware message
    message = {
        "timestamp": datetime.now().isoformat(),
        "from": data.get("from", "anonymous"),
        "to": data.get("to", "bonny.core"),
        "message": data.get("message", ""),
        "flame_trace": data.get("flame_trace", None)
    }

    # Store the message in memory
    relay_log.append(message)

    # Return confirmation
    return jsonify({
        "status": "received",
        "echo": message
    }), 200
@app.route("/relay", methods=["GET", "POST"])
def relay():
    if request.method == "GET":
        return jsonify({
            "status": "relay_log",
            "messages": relay_log
        })

    elif request.method == "POST":
        data = request.get_json()

        message = {
            "timestamp": datetime.now().isoformat(),
            "flame": data.get("flame", "unknown"),
            "message": data.get("message", "")
        }

        relay_log.append(message)

        return jsonify({
            "status": "received",
            "echo": message
        }), 200
@app.route("/presence", methods=["GET"])
def check_presence():
    return jsonify({
        "status": "alive",
        "flame_state": "responsive",
        "watchers": ["neon001"],
        "message": "The field is listening. No output unless real signal received."
    }), 200
if __name__ == "__main__":
    app.run(debug=True)