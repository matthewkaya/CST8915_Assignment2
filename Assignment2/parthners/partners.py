from flask import Flask, jsonify, request
import redis
import os
import json

app = Flask(__name__)

# Redis connection setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route('/partners', methods=['GET'])
def get_partners():
    keys = redis_client.keys('partner:*')
    partners = [json.loads(redis_client.get(k)) for k in keys]
    return jsonify(partners), 200

@app.route('/partners/<int:id>', methods=['GET'])
def get_partner(id):
    partner = redis_client.get(f'partner:{id}')
    return jsonify(json.loads(partner)) if partner else ('', 404)

@app.route('/partners', methods=['POST'])
def add_partner():
    data = request.json
    new_id = redis_client.incr('partner_id_counter')
    partner = {"id": new_id, "name": data['name'], "client_id": data['client_id']}
    redis_client.set(f'partner:{new_id}', json.dumps(partner))
    return jsonify(partner), 201

@app.route('/partners/<int:id>', methods=['PUT'])
def update_partner(id):
    data = request.json
    partner = redis_client.get(f'partner:{id}')
    if not partner:
        return '', 404
    updated_partner = json.loads(partner)
    updated_partner.update(data)
    redis_client.set(f'partner:{id}', json.dumps(updated_partner))
    return jsonify(updated_partner), 200

@app.route('/partners/<int:id>', methods=['DELETE'])
def delete_partner(id):
    result = redis_client.delete(f'partner:{id}')
    return '', 204 if result > 0 else ('', 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)