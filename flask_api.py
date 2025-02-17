from flask import Flask, request, jsonify
from database import Database
from table_operations import TableOperations

app =Flask(__name__)

db = Database("your_user", "your_password", "your_database")
student_ops = TableOperations(db)

@app.route('/students', methods=["POST"])
def insert_student():
    data = request.json
    student_ops.insert_record(data["name"], data["branch"], data["roll"], data["section"], data["age"])
    return jsonify({"message":"Student added successfully"})

if __name__ == "__main__":
    app.run(debug=True)