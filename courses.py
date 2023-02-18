from db import db

def get_courses():
    sql = "select id, name from courses order by name"
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
