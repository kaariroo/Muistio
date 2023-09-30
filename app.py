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
    result = db.session.execute(text('SELECT id, name, describtion FROM Locations ORDER BY id'))
    places = result.fetchall()
    result = db.session.execute(text('SELECT id, name, describtion FROM Npcs ORDER BY id'))
    npcs = result.fetchall()
    return render_template("index.html", counter=len(places), places=places, npcs=npcs)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.is_admin(username)
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Wrong username or password")
    
    

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/new_npc")
def new_npc():
    result = db.session.execute(text('SELECT id, name, describtion FROM Locations ORDER BY id'))
    places = result.fetchall()
    return render_template("new_npc.html", places=places)

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    describtion = request.form["describtion"]
    sql = text("INSERT INTO Locations (name,describtion) VALUES (:name,:describtion)")
    db.session.execute(sql, {"name":name, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/send_npc", methods=["POST"])
def send_npc():
    name = request.form["name"]
    describtion = request.form["describtion"]
    region = request.form["region"]
    sql = text("INSERT INTO Npcs (name,describtion,location_id) VALUES (:name,:describtion,:region)")
    db.session.execute(sql, {"name":name, "describtion":describtion, "region":region})
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    sql = text("SELECT id, name, describtion FROM Locations WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    place= result.fetchone()
    return render_template("edit.html", place=place)

@app.route("/edit_npc/<int:id>")
def edit_npc(id):
    sql = text("SELECT id, name, describtion FROM Npcs WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    npc = result.fetchone()
    return render_template("edit_npc.html", npc=npc)

@app.route("/save/<int:id>", methods=["POST"])
def save(id):
    describtion = request.form["describtion"]
    sql = text("UPDATE Locations SET describtion=:describtion WHERE id=:id")
    db.session.execute(sql, {"id":id, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/save_npc/<int:id>", methods=["POST"])
def save_npc(id):
    describtion = request.form["describtion"]
    sql = text("UPDATE Npcs SET describtion=:describtion WHERE id=:id")
    db.session.execute(sql, {"id":id, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/npc/<int:id>")
def npc(id):
    sql = text('SELECT id, name, describtion FROM Npcs WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    npc = result.fetchone()
    return render_template("npc.html", npc=npc)

@app.route("/region/<int:id>")
def region(id):
    sql = text('SELECT id, name, describtion FROM Locations WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    place = result.fetchone()
    sql = text('SELECT id, name FROM Npcs WHERE Npcs.location_id=:id ORDER BY id')
    result = db.session.execute(sql, {"id":id})
    npcs = result.fetchall()
    return render_template("location.html", place=place, npcs=npcs)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        usertype = "user"
        if password1 != password2:
            return render_template("error.html", message="Passwords are different")
        if users.register(username, password1, usertype):
            users.is_admin(username)
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")
