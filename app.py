from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Conexão com MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.iot_database
devices_collection = db.devices

@app.route('/check-access', methods=['GET'])
def check_access():
    try:
        # Busca o dispositivo no MongoDB
        device = devices_collection.find_one({"device_id": "t-A7670SA"})
        
        if device and device.get("allowed", False):
            allowed = True
        else:
            allowed = False
        
        return jsonify({
            "allowed": allowed,
            "status": "success",
            "server_region": "sao-paulo"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API com MongoDB funcionando!"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
