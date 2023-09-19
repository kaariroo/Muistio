from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import users
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///kaariroo"
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text('SELECT id, name, describtion FROM Locations'))
    places = result.fetchall()
    return render_template("index.html", counter=len(places), places=places)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Wrong username or password")
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    describtion = request.form["describtion"]
    sql = text("INSERT INTO Locations (name,describtion) VALUES (:name,:describtion)")
    db.session.execute(sql, {"name":name, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    sql = text("SELECT id, name, describtion FROM Locations WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    place= result.fetchone()
    return render_template("edit.html", place=place)

@app.route("/save/<int:id>", methods=["POST"])
def save(id):
    describtion = request.form["describtion"]
    sql = text("UPDATE Locations SET describtion=:describtion WHERE id=:id")
    db.session.execute(sql, {"id":id, "describtion":describtion})
    db.session.commit()
    return redirect("/")


@app.route("/region/<int:id>")
def region(id):
    sql = text('SELECT id, name, describtion FROM Locations WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    place = result.fetchone()
    return render_template("location.html", place=place)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords are differen")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")
