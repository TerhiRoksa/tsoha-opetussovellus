from db import db
from flask import session
import users

def get_courses():
    sql = "select id, name from courses where visible=true order by name"
    return db.session.execute(sql).fetchall()

def get_polls():
    sql = "select id, topic, course_id from polls order by topic"
    return db.session.execute(sql).fetchall()

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
   
