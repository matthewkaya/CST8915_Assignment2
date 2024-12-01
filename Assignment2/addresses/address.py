# Updated 'address.py' for MongoDB integration
from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.addresses_db

@app.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = list(db.addresses.find({}, {"_id": 0}))
    return jsonify(addresses), 200

@app.route('/addresses/<int:id>', methods=['GET'])
def get_address(id):
    address = db.addresses.find_one({"id": id}, {"_id": 0})
    return jsonify(address) if address else ('', 404)

@app.route('/addresses', methods=['POST'])
def add_address():
    data = request.json
    new_address = {"id": db.addresses.count_documents({}) + 1, "street": data['street'], "city": data['city'], "client_id": data['client_id']}
    db.addresses.insert_one(new_address)
    return jsonify(new_address), 201

@app.route('/addresses/<int:id>', methods=['PUT'])
def update_address(id):
    data = request.json
    result = db.addresses.update_one({"id": id}, {"$set": data})
    return jsonify(data) if result.matched_count > 0 else ('', 404)

@app.route('/addresses/<int:id>', methods=['DELETE'])
def delete_address(id):
    result = db.addresses.delete_one({"id": id})
    return '', 204 if result.deleted_count > 0 else ('', 404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
