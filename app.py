from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import Redis
from redis.connection import SSLConnection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Connect to Redis using SSL
redis_client = Redis.from_url(
    os.getenv("REDIS_URL"),
    connection_class=SSLConnection
)

# Prefixes
GRADE_PREFIX = "grade:"
ID_KEY = "grades:next_id"  # metadata key for auto-increment ID

# Build Redis key for a given grade ID
def build_key(id):
    return f"{GRADE_PREFIX}{id}"

# GET /grades - List all grades
@app.route('/grades', methods=['GET'])
def list_grades():
    keys = redis_client.keys(f"{GRADE_PREFIX}*")
    result = []
    for key in keys:
        try:
            value = redis_client.hgetall(key)
            result.append({
                "id": key.decode().split(":")[1],
                "name": value.get(b'name', b'').decode(),
                "grade": value.get(b'grade', b'').decode()
            })
        except Exception as e:
            # Skip keys that aren't valid hash entries
            continue
    return jsonify(result)

# GET /grades/<id> - Get a single grade by ID
@app.route('/grades/<id>', methods=['GET'])
def get_grade(id):
    key = build_key(id)
    if not redis_client.exists(key):
        return jsonify({'error': 'Grade not found'}), 404
    value = redis_client.hgetall(key)
    return jsonify({
        "id": id,
        "name": value.get(b'name', b'').decode(),
        "grade": value.get(b'grade', b'').decode()
    })

# POST /grades - Add a new grade
@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')

    if not name or not grade:
        return jsonify({'error': 'Missing name or grade'}), 400

    new_id = redis_client.incr(ID_KEY)
    key = build_key(new_id)
    redis_client.hset(key, mapping={"name": name, "grade": grade})

    return jsonify({"id": new_id, "name": name, "grade": grade}), 201

# PUT /grades/<id> - Update existing grade
@app.route('/grades/<id>', methods=['PUT'])
def update_grade(id):
    key = build_key(id)
    if not redis_client.exists(key):
        return jsonify({'error': 'Grade not found'}), 404

    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')

    if not name or not grade:
        return jsonify({'error': 'Missing name or grade'}), 400

    redis_client.hset(key, mapping={"name": name, "grade": grade})
    return jsonify({"id": id, "name": name, "grade": grade})

# DELETE /grades/<id> - Delete a grade
@app.route('/grades/<id>', methods=['DELETE'])
def delete_grade(id):
    key = build_key(id)
    if not redis_client.exists(key):
        return jsonify({'error': 'Grade not found'}), 404
    redis_client.delete(key)
    return jsonify({'message': f'Grade with id {id} deleted'})

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
