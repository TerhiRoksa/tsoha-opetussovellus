from db import db

def get_courses():
    sql = "select id, name from courses order by name"
    return db.session.execute(sql).fetchall()
