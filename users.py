from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import app


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = app.db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        app.db.session.execute(sql, {"username":username, "password":hash_value})
        app.db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]