from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def login(username, password):
    sql = "SELECT id, username, password, usertype FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_username"] = username
            session["user_usertype"] = user[3]
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]

def register(username, password, usertype):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, usertype) VALUES (:username, :password, :usertype)"
        db.session.execute(sql, {"username":username, "password":hash_value, "usertype":usertype})
        db.session.commit()
    except:
        return False
    return login(username, password)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
