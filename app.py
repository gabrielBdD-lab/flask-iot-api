from flask import Flask, jsonify, request  # ⬅️ ADICIONE 'request' aqui
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

# ⬇️ COLE A FUNÇÃO handle_http AQUI (ANTES das rotas)
@app.before_request
def handle_http():
    if request.url.startswith('http://'):
        # Permite HTTP sem redirecionar - não faz nada
        pass

@app.route('/check-access', methods=['GET'])
def check_access():
    try:
        # Busca o dispositivo no MongoDB
        device = devices_collection.find_one({"device_id": "t-A7670SA"})
        
        if device and device.get("allowed", False):
            allowed = True
            status_msg = "access_granted"
        else:
            allowed = False
            status_msg = "access_denied"
        
        return jsonify({
            "allowed": allowed,
            "status": status_msg,
            "server": "render",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "message": "API Flask + MongoDB funcionando!",
        "status": "success", 
        "protocol": "http"
    })

@app.route('/')
def home():
    return jsonify({
        "message": "Bem-vindo à API IoT",
        "endpoints": {
            "test": "/test", 
            "check_access": "/check-access"
        },
        "note": "HTTP permitido para dispositivos IoT"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
