from app import app
from flask import render_template, request, redirect, session
from db import db
from sqlalchemy.sql import text
import users
import courses

@app.route("/")
def index():
    return render_template("index.html", courses=courses.get_courses())

@app.route("/remove", methods=["GET", "POST"])
def remove_course():
    users.check_csrf()
    if "course" in request.form:
        course = request.form["course"]
        courses.remove_course(course)
    return redirect("/")

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
        if len(username) < 4 or len(username) > 30:
            return render_template("error.html", message="Käyttäjätunnuksen tulee olla 4-30 merkkiä pitkä.")
        if len(password1) <4 or len(password1) > 30:
            return render_template("error.html", message="Salasanan tulee olla 4-30 merkkiä pitkä.")
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
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        return render_template("material.html")
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/result2/<int:id>")
def result2(id):
    allow = False
    user_id = users.user_id()  
    if user_id > 0:
        allow = True
        sql = "SELECT content FROM material WHERE course_id=:id"
        result = db.session.execute(sql, {"id":id}) 
        content = result.fetchone()[0]   
        return render_template("result2.html", id=id, content=content)
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")


@app.route("/create_material", methods=["GET", "POST"])
def create_material():
    allow = False
    user_id = users.user_id()  
    if user_id > 0:
        allow = True
        users.check_csrf()
        name = request.form["name"]
        if len(name) < 1 or len(name) > 200:
            return render_template("error.html", message="Nimen tulee olla vähintään 1 ja enintään 200 merkkiä pitkä.")
        sql = "INSERT INTO courses (name, visible) VALUES (:name, true) RETURNING id"
        result = db.session.execute(sql, {"name":name})
        course_id = result.fetchone()[0]
        content = request.form["material"]
        if len(content) < 1 or len(content) > 5000:
            return render_template("error.html", message="Materiaalin tulee olla vähintään 1 ja enintään 5000 merkkiä.")
        sql = "INSERT INTO material (content, course_id) VALUES (:content, :course_id) RETURNING course_id"    
        result = db.session.execute(sql, {"content":content, "course_id":course_id})
        course_id = result.fetchone()[0]
        db.session.commit()
        return redirect("/result2/" + str(course_id))
    if not allow: 
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/polls/<int:id>")
def polls(id):
    allow = False
    user_id = users.user_id()   
    if user_id > 0:
        allow = True
        sql = "SELECT id, topic FROM polls WHERE course_id=:id"
        result = db.session.execute(sql, {"id":id})
        topic = result.fetchall()
        return render_template("polls.html", id=id, topic=topic)
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/new")
def new():
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        return render_template("new.html")
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/create", methods=["GET", "POST"])
def create():
    users.check_csrf()
    name = request.form["name"]
    if len(name) < 1 or len(name) > 100:
        return render_template("error.html", message="Nimen tulee olla vähintään 1 ja enintään 100 merkkiä pitkä.")
    sql = "SELECT id FROM courses where name=:name"
    result = db.session.execute(sql, {"name":name})
    course_id = result.fetchone()[0]
    topic = request.form["topic"]
    if len(topic) < 1 or len(topic) > 200:
        return render_template("error.html", message="Kysymyksen tulee olla vähintään 1 ja enintään 200 merkkiä pitkä.")
    answer = request.form["answer"]
    if len(answer) < 1 or len(answer) > 100:
            return render_template("error.html", message="Vastauksen tulee olla vähintään 1 ja enintään 100 merkkiä pitkä.")
    sql = "INSERT INTO polls (topic, course_id, answer) VALUES (:topic, :course_id, :answer) RETURNING id"
    result = db.session.execute(sql, {"topic":topic, "course_id":course_id, "answer":answer})
    poll_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    for choice in choices:
        if len(choice) < 1 or len(choice) > 100:
            return render_template("error.html", message="Vastausvaihtoehdon tulee olla vähintään 1 ja enintään 100 merkkiä pitkä.")
        if choice != "":
            sql = "INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)"
            db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
    db.session.commit()
    return redirect("/polls/" + str(course_id))

@app.route("/poll/<int:id>")
def poll(id):
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        sql = "SELECT topic FROM polls WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        topic = result.fetchone()[0]
        sql = "SELECT id, choice FROM choices WHERE poll_id=:id"
        result = db.session.execute(sql, {"id":id})
        choices = result.fetchall()
        return render_template("poll.html", id=id, topic=topic, choices=choices)
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/answer", methods=["POST"])
def answer():
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        poll_id = request.form["id"]
        if "answer" in request.form:  
            choice_id = request.form["answer"]  
            sql = "INSERT INTO answers (choice_id) VALUES (:choice_id)"
            db.session.execute(sql, {"choice_id":choice_id})
            db.session.commit()
        return redirect("/result/" + str(poll_id))
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")    

@app.route("/result/<int:id>")
def result(id):
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
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
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/statistics/<int:id>")
def statistics(id):
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        sql = "SELECT answer FROM polls WHERE id=:id"
        result = db.session.execute(text(sql), {"id":id})
        answer = result.fetchone()[0]
        sql = "SELECT c.choice FROM choices c RIGHT JOIN answers a " \
              "ON c.id=a.choice_id ORDER BY a.id DESC"
        result = db.session.execute(sql, {"id":id})
        choice = result.fetchone()[0]
        return render_template("statistics.html", id=id, answer=answer, choice=choice, students=courses.get_students())
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
