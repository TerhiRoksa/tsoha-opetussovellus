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
        content = courses.get_material(id)   
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
        if len(name) < 1 or len(name) > 50:
            return render_template("error.html", message="Nimessä tulee olla 1-50 merkkiä.")
        course_id = courses.create_course(name)
        content = request.form["material"]
        if len(content) < 1 or len(content) > 5000:
            return render_template("error.html", message="Materiaalin tulee olla vähintään 1 ja enintään 5000 merkkiä.")
        courses.create_material(content, course_id)
        return redirect("/result2/" + str(course_id))
    if not allow: 
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/polls/<int:id>")
def polls(id):
    allow = False
    user_id = users.user_id()   
    if user_id > 0:
        allow = True
        topic = courses.get_polls(id)
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
    course_id = courses.get_course(name)
    topic = request.form["topic"]
    if len(topic) < 1 or len(topic) > 200:
        return render_template("error.html", message="Kysymyksen tulee olla vähintään 1 ja enintään 200 merkkiä pitkä.")
    answer = request.form["answer"]
    if len(answer) < 1 or len(answer) > 100:
            return render_template("error.html", message="Vastauksen tulee olla vähintään 1 ja enintään 100 merkkiä pitkä.")
    poll_id = courses.create_poll(topic, course_id, answer)
    choices = request.form.getlist("choice")
    for choice in choices:
        if len(choice) < 1 or len(choice) > 100:
            return render_template("error.html", message="Vastausvaihtoehdon tulee olla vähintään 1 ja enintään 100 merkkiä pitkä.")
        if choice != "":
            courses.create_choices(poll_id, choice)
    return redirect("/polls/" + str(course_id))

@app.route("/poll/<int:id>")
def poll(id):
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        topic = courses.get_poll(id)
        choices = courses.get_choice(id)
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
            courses.create_answer(choice_id, user_id)
        return redirect("/result/" + str(poll_id))
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")    

@app.route("/result/<int:id>")
def result(id):
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        topic = courses.get_topic(id)
        choices = courses.get_choices(id)
        answer = courses.get_answers(id)
        return render_template("result.html", id=id, answer=answer, topic=topic, choices=choices)
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")

@app.route("/statistics/<int:id>")
def statistics(id):
    allow = False
    user_id = users.user_id()
    if user_id > 0:
        allow = True
        answer = courses.get_answers(id)
        choice = courses.get_your_answer(id)
        return render_template("statistics.html", id=id, answer=answer, choice=choice, students=courses.get_students(), points=courses.get_right_answers())   
    if not allow:
        return render_template("error.html", message="Sinulla ei ole oikeutta nähdä sivua")
