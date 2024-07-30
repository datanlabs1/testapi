import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_student"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "root123"
app.config["MYSQL_DATABASE_DB"] = "sdnldb"
app.config["MYSQL_DATABASE_HOST"] = "db"
app.config["MYSQL_DATABASE_PORT"] = 3306
mysql.init_app(app)


@app.route("/")
def index():
    return "Welcome to Data & Labs !!!!"


@app.route("/create", methods=["POST"])
def add_student():
    json = request.json
    name = json["name"]
    email = json["email"]
    password = json["password"]
    course = json["course"]
    if name and email and password and course and request.method == "POST":
        sql = "INSERT INTO students(student_name, student_email, student_password, student_course) " \
              "VALUES(%s, %s, %s, %s)"
        data = (name, email, password, course)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("Added to the training successfully!!!!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please enter Name and email or contact us at info@datanlabs.com")


@app.route("/students", methods=["GET"])
def students():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/student/<int:student_id>", methods=["GET"])
def student(student_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=%s", student_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_student():
    json = request.json
    name = json["name"]
    email = json["email"]
    password = json["password"]
    course = json["course"]
    student_id = json["student_id"]

    if name and email and password and student_id and request.method == "POST":
        sql = "UPDATE students SET student_name=%s, student_email=%s, " \
              "student_password=%s,student_course=%s WHERE student_id=%s"
        data = (name, email, password, course, student_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("Details have been updated successfully!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please enter name and emails or contact us @ info@datanlabs.com !!!")


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=%s", student_id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("student deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
