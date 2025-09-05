from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações do banco
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'ssl_ca': '/etc/ssl/cert.pem'
}

@app.route('/check-access', methods=['GET'])
def check_access():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT allowed FROM devices WHERE device_id = 't-A7670SA'")
        result = cursor.fetchone()
        
        allowed = bool(result[0]) if result else False
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "allowed": allowed,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API funcionando!"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)