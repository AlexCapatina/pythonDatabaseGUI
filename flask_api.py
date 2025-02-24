from flask import Flask, request, jsonify, render_template
from database import Database
from table_operations import TableOperations

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


db = Database("root", "BestPassword89", "testPython_db")
student_ops = TableOperations(db)


@app.route("/students", methods=["GET"])
def get_students():
    rows, columns = student_ops.get_table_data()
    students = [dict(zip(columns, row)) for row in rows]
    return jsonify(students)


@app.route('/students', methods=["POST"])
def insert_student():
    data = request.json
    values = (data["name"], data["branch"], data["roll"], data["section"], data["age"])
    student_ops.insert_record(values)
    return jsonify({"message": "Student added successfully"}), 201


@app.route("/students/<int:roll>", methods=["PUT"])
def update_student(roll):
    data = request.json
    values = (data["name"], data["branch"], data["roll"], data["section"], data["age"])
    student_ops.update_record(values)
    return jsonify({"message": "Student updated successfully"}), 200


@app.route("/students/<int:roll>", methods=["DELETE"])
def delete_student(roll):
    student_ops.delete_record(roll)
    return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
