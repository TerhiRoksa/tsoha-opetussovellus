from db import db
from flask import session
import users

def create_course(name):
    sql = "INSERT INTO courses (name, visible) VALUES (:name, true) RETURNING id"
    course_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    db.session.commit()
    return course_id

def create_material(content, course_id):
    sql = "INSERT INTO material (content, course_id) VALUES (:content, :course_id)"
    db.session.execute(sql, {"content":content, "course_id":course_id})
    db.session.commit()

def get_courses():
    sql = "select id, name from courses where visible=true order by name"
    return db.session.execute(sql).fetchall()

def get_course(name):
    sql = "SELECT id FROM courses where name=:name"
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def get_material(id):
    sql = "SELECT content FROM material WHERE course_id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0] 

def create_poll(topic, course_id, answer):
    sql = "INSERT INTO polls (topic, course_id, answer) VALUES (:topic, :course_id, :answer) RETURNING id"
    poll_id = db.session.execute(sql, {"topic":topic, "course_id":course_id, "answer":answer}).fetchone()[0]
    db.session.commit()
    return poll_id

def create_choices(poll_id, choice):
    sql = "INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)"
    db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
    db.session.commit()

def get_polls(id):
    sql = "SELECT id, topic FROM polls WHERE course_id=:id"
    return db.session.execute(sql, {"id":id}).fetchall()

def get_poll(id):
    sql = "SELECT topic FROM polls WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def get_topic(id):
    sql = "SELECT id, topic FROM polls WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[1]

def get_choice(id):
    sql = "SELECT id, choice FROM choices WHERE poll_id=:id"
    return db.session.execute(sql, {"id":id}).fetchall()

def get_choices(id):
    sql = "SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
              "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id order by c.id"
    return db.session.execute(sql, {"poll_id":id}).fetchall()

def get_answers(id):
    sql = "SELECT answer FROM polls WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()[0]

def create_answer(choice_id, user_id):
    sql = "INSERT INTO answers (choice_id, user_id) VALUES (:choice_id, :user_id)"
    db.session.execute(sql, {"choice_id":choice_id, "user_id":user_id})
    db.session.commit()

def get_answer():
    sql = "select id, answer from polls"
    return db.session.execute(sql).fetchone()

def get_students():
    sql = "select username from users where usertype != 2"
    return db.session.execute(sql).fetchall()

def remove_course(course_id):
    sql = "UPDATE courses SET visible=false WHERE id=:id"
    db.session.execute(sql, {"id":course_id})
    db.session.commit()

def get_right_answers():
   sql = "select a.user_id from answers a, choices c, polls p where c.poll_id=p.id and c.choice=p.answer and a.choice_id=c.id;"
   return db.session.execute(sql).fetchall()
   
def get_your_answer(id):
    sql = "select a.id, a.user_id, c.choice from choices c, answers a where c.id=a.choice_id and c.poll_id=:id order by a.id desc"
    return db.session.execute(sql, {"id":id}).fetchall()
