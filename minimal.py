from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"status": "online", "message": "API is working"})

@app.route('/test')
def test():
    return jsonify({"test": "success"})

# Add any other routes before this line
# The if __name__ block should only contain run configuration
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)