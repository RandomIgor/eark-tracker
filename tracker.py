from flask import Flask, request, jsonify
import time

app = Flask(__name__)
peers = {} 

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    port = data.get('port')
    if not port:
        return jsonify({"error": "Puerto requerido"}), 400

    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    peer_address = f"{ip}:{port}"

    peers[peer_address] = time.time()
    return jsonify({"message": "Registrado correctamente", "peer": peer_address}), 200

@app.route('/peers', methods=['GET'])
def get_peers():
    current_time = time.time()
    active_peers = [peer for peer, last_seen in peers.items() if current_time - last_seen < 300]
    
    global peers
    peers = {peer: peers[peer] for peer in active_peers}

    return jsonify({"peers": active_peers}), 200

@app.route('/', methods=['GET'])
def home():
    return "EARK Global Tracker is Online."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
