from sqlalchemy.sql import text
from flask import Flask, flash
from flask import url_for
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import users
import operations
import input_check

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
    picture = url_for('static', filename='melamar.jpg')
    return render_template("index.html", counter=len(places), places=places, npcs=npcs, picture=picture)
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.is_admin(username)
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", error="Wrong username or password")

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


@app.route("/new_location_note")
def new_location_note():
    result = db.session.execute(text('SELECT id, name FROM Locations ORDER BY id'))
    places = result.fetchall()
    return render_template("new_location_note.html", places=places)

@app.route("/send_location_note", methods=["POST"])
def send_location_note():
    note = request.form["note"]
    if len(note) > 10000:
        return render_template("error.html", error="Note is too long. You can try ro save it in multiple notes")
    region = request.form["region"]
    user = users.id()
    sql = text("INSERT INTO Location_notes (note,location_id,user_id) VALUES (:note,:region,:user_id)")
    db.session.execute(sql, {"note":note, "user_id":user, "region":region})
    db.session.commit()
    return redirect("/")

@app.route("/send", methods=["POST"])
def send():
    try:
        name = request.form["name"]
        describtion = request.form["describtion"]
        table = "Locations"
        name_check = input_check.check_name_and_describtion(name, describtion)
        if name_check != True:
            return render_template("error.html", error=name_check)
        operations.send(name, describtion, table)
    except:
        return render_template("error.html", error="Name already in use")
    return redirect("/")

@app.route("/send_npc", methods=["POST"])
def send_npc():
    try:
        name = request.form["name"]
        describtion = request.form["describtion"]
        table = "Npcs"
        name_check = input_check.check_name_and_describtion(name, describtion)
        if name_check != True:
           return render_template("error.html", error=name_check)
        region = request.form["region"]
        operations.send(name, describtion, table, region)
        return redirect("/")
    except:
       return render_template("error.html", error="Please choose a region for this npc")
    

@app.route("/edit/<int:id>")
def edit(id):
    table = "Locations"
    place = operations.get_one(id, table)
    return render_template("edit.html", place=place)

@app.route("/edit_npc/<int:id>")
def edit_npc(id):
    table = "Npcs"
    npc = operations.get_one(id, table)
    return render_template("edit_npc.html", npc=npc)

@app.route("/edit_location_note/<int:id>")
def edit_location_note(id):
    table = "Note"
    note = operations.get_one(id, table)
    return render_template("edit_location_note.html", note=note)

@app.route("/save_location_note/<int:id>", methods=["POST"])
def save_location_note(id):
    note = request.form["note"]
    note_check = input_check.check_note(note)
    if note_check == "delete":
        sql = text("DELETE From Location_notes WHERE id=:id")
        db.session.execute(sql, {"id":id, "note":note})
        db.session.commit()
    elif note_check != True:
        return render_template("error.html", error=note_check)
    else:
        sql = text("UPDATE Location_notes SET note=:note WHERE id=:id")
        db.session.execute(sql, {"id":id, "note":note})
        db.session.commit()
    return redirect("/")

@app.route("/save/<int:id>", methods=["POST"])
def save(id):
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Location"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check != True:
        return render_template("error.html", error=name_check)
    operations.save(id, name, describtion, table)
    return redirect("/")

@app.route("/save_npc/<int:id>", methods=["POST"])
def save_npc(id):
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Npcs"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check != True:
        return render_template("error.html", error=name_check)
    operations.save(id, name, describtion, table)
    return redirect("/")

@app.route("/npc/<int:id>")
def npc(id):
    table = "Npcs"
    npc = operations.get_one(id, table)
    return render_template("npc.html", npc=npc)

@app.route("/region/<int:id>")
def region(id):
    table = "Locations"
    place = operations.get_one(id, table)
    npcs = operations.get_locations_npcs(id)
    user = users.id()
    notes = operations.get_notes(id, user)
    return render_template("operations.html", place=place, npcs=npcs, notes=notes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        sql = text("SELECT * FROM users")
        result = db.session.execute(sql)
        user_amount = len(result.fetchall())
        if user_amount == 0:
            usertype = "admin"
        else:
            usertype = "user"
        if password1 != password2:
            return render_template("error.html", error="Passwords are different")
        if users.register(username, password1, usertype):
            users.is_admin(username)
            return redirect("/")
        else:
            return render_template("error.html", error="Registration failed")
