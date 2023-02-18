from app import app
from flask import render_template, request, redirect, session
from db import db
from sqlalchemy.sql import text
import users
import courses

@app.route("/")
def index():
    return render_template("index.html", courses=courses.get_courses())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]  
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        usertype = request.form["usertype"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, usertype):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/material")
def material():
    return render_template("material.html")

@app.route("/result2/<int:id>")
def result2(id):
    sql = "SELECT content FROM material WHERE id=:id"
    result = db.session.execute(sql, {"id":id}) 
    content = result.fetchone()[0]   
    return render_template("result2.html",id=id, content=content)

@app.route("/create_material", methods=["GET", "POST"])
def create_material():
    name = request.form["name"]
    sql = "INSERT INTO courses (name) VALUES (:name) RETURNING id"
    result = db.session.execute(sql, {"name":name})
    course_id = result.fetchone()[0]
    content = request.form["material"]
    sql = "INSERT INTO material (content, course_id) VALUES (:content, :course_id) RETURNING id"    
    result = db.session.execute(sql, {"content":content, "course_id":course_id})
    material_id = result.fetchone()[0]
    db.session.commit()
    return redirect("/result2/" + str(material_id))

@app.route("/polls/<int:id>")
def polls(id):
    sql = "SELECT id, topic FROM polls WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()
    return render_template("polls.html", id=id, topic=topic, polls=courses.get_polls())

@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    name = request.form["name"]
    sql = "SELECT id FROM courses where name=:name"
    result = db.session.execute(sql, {"name":name})
    course_id = result.fetchone()[0]
    topic = request.form["topic"]
    answer = request.form["answer"]
    sql = "INSERT INTO polls (topic, course_id, answer) VALUES (:topic, :course_id, :answer) RETURNING id"
    result = db.session.execute(sql, {"topic":topic, "course_id":course_id, "answer":answer})
    poll_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            sql = "INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)"
            db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
    db.session.commit()
    return redirect("/polls/" + str(course_id))

@app.route("/poll/<int:id>")
def poll(id):
    sql = "SELECT topic FROM polls WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = "SELECT id, choice FROM choices WHERE poll_id=:id"
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return render_template("poll.html", id=id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    poll_id = request.form["id"]
    if "answer" in request.form:  
        choice_id = request.form["answer"]  
        sql = "INSERT INTO answers (choice_id) VALUES (:choice_id)"
        db.session.execute(sql, {"choice_id":choice_id})
        db.session.commit()
    return redirect("/result/" + str(poll_id))
    
@app.route("/result/<int:id>")
def result(id):
    sql = "SELECT id, topic FROM polls WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[1]
    sql = "SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
          "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id"
    result = db.session.execute(sql, {"poll_id":id})
    choices = result.fetchall()
    sql = "SELECT answer FROM polls WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    answer = result.fetchone()[0]
    return render_template("result.html", id=id, answer=answer, topic=topic, choices=choices)

@app.route("/statistics/<int:id>")
def statistics(id):
    sql = "SELECT answer FROM polls WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    answer = result.fetchone()[0]
    sql = "SELECT c.choice FROM choices c RIGHT JOIN answers a " \
          "ON c.id=a.choice_id ORDER BY a.id DESC"
    result = db.session.execute(sql, {"id":id})
    choice = result.fetchone()[0]
    return render_template("statistics.html", id=id, answer=answer, choice=choice, students=courses.get_students())
