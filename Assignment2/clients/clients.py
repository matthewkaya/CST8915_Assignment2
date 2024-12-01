# Updated 'clients.py' for PostgreSQL integration
from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection setup
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "clients_db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/clients', methods=['GET'])
def get_clients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, balance FROM clients')
    clients = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": c[0], "name": c[1], "balance": c[2]} for c in clients]), 200

@app.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, balance FROM clients WHERE id = %s', (id,))
    client = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({"id": client[0], "name": client[1], "balance": client[2]}) if client else ('', 404)

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO clients (name, balance) VALUES (%s, %s) RETURNING id',
                (data['name'], data['balance']))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "name": data['name'], "balance": data['balance']}), 201

@app.route('/clients/<int:id>', methods=['PUT'])
def update_client(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE clients SET name = %s, balance = %s WHERE id = %s',
                (data['name'], data['balance'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": id, "name": data['name'], "balance": data['balance']}), 200

@app.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM clients WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
