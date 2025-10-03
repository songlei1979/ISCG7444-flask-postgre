from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)


# PostgreSQL connection setup
conn = psycopg2.connect(os.getenv("DB_URL"))
cursor = conn.cursor()

# GET /students - list all students
@app.route('/grades', methods=['GET'])
def list_students():
    cursor.execute("SELECT id, name, grade FROM students")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "grade": row[2]
        })
    return jsonify(result)


# GET /students/<id> - get one student
@app.route('/grades/<id>', methods=['GET'])
def get_student(id):
    cursor.execute("SELECT id, name, grade FROM students WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        return jsonify({
            "id": row[0],
            "name": row[1],
            "grade": row[2]
        })
    else:
        return jsonify({"error": "Student not found"}), 404


# POST /students - add student
@app.route('/grades', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')

    if not name or not grade:
        return jsonify({"error": "Missing name or grade"}), 400
    cursor.execute("INSERT INTO students (name, grade) VALUES (%s, %s) RETURNING id", (name, grade))
    new_id = cursor.fetchone()[0]
    conn.commit()

    return jsonify({"id": new_id, "name": name, "grade": grade}), 201


# PUT /students/<id> - update student
@app.route('/grades/<id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')

    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    if not cursor.fetchone():
        return jsonify({"error": "Student not found"}), 404

    cursor.execute("UPDATE students SET name = %s, grade = %s WHERE id = %s", (name, grade, id))
    conn.commit()

    return jsonify({"id": id, "name": name, "grade": grade})


# DELETE /students/<id> - delete student
@app.route('/grades/<id>', methods=['DELETE'])
def delete_student(id):
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    if not cursor.fetchone():
        return jsonify({"error": "Student not found"}), 404

    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"message": f"Student with id {id} deleted"})


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
