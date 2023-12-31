from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import app


def login(username, password):
    sql = text("SELECT id, password, usertype FROM users WHERE username=:username")
    result = app.db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        return True
    return False

def register(username, password, usertype):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password,usertype) VALUES (:username,:password,:usertype)")
        app.db.session.execute(sql, {"username":username, "password":hash_value, "usertype":usertype})
        app.db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]

def id():
    return session["user_id"]

def is_admin(username):
    try:
        sql = text("SELECT usertype FROM users WHERE username=:username")
        result = app.db.session.execute(sql, {"username":username})
        usertype = result.fetchone()
        session["usertype"] = usertype[0]
        if usertype[0] == "admin":
            return True
        return False
    except:
        return False