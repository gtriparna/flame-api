from flask import Flask, jsonify
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def hello():
    app.logger.info("Root endpoint accessed")
    return jsonify({"status": "online", "message": "API is working", "routes": [str(rule) for rule in app.url_map.iter_rules()]})

@app.route('/test', methods=['GET'])
def test():
    app.logger.info("Test endpoint accessed")
    return jsonify({"test": "success"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)