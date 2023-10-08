from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import users

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
    name = request.form["name"]
    if len(name) > 50:
        return render_template("error.html", error="Name is too long")
    describtion = request.form["describtion"]
    if len(describtion) > 10000:
        return render_template("error.html", error="Describiton is too long")
    sql = text("INSERT INTO Locations (name,describtion) VALUES (:name,:describtion)")
    db.session.execute(sql, {"name":name, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/send_npc", methods=["POST"])
def send_npc():
    name = request.form["name"]
    if len(name) > 50:
        return render_template("error.html", error="Name is too long")
    describtion = request.form["describtion"]
    if len(describtion) > 10000:
        return render_template("error.html", error="Describiton is too long")
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

@app.route("/edit_location_note/<int:id>")
def edit_location_note(id):
    sql = text("SELECT id, note FROM Location_notes WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    note = result.fetchone()
    return render_template("edit_location_note.html", note=note)

@app.route("/save_location_note/<int:id>", methods=["POST"])
def save_location_note(id):
    note = request.form["note"]
    if len(note) > 10000:
        return render_template("error.html", error="Note is too long. You can try ro save it in multiple notes")
    elif len(note) > 0 and len(note) < 10000:
        sql = text("UPDATE Location_notes SET note=:note WHERE id=:id")
        db.session.execute(sql, {"id":id, "note":note})
        db.session.commit()
    elif len(note) == 0:
        sql = text("DELETE From Location_notes WHERE id=:id")
        db.session.execute(sql, {"id":id, "note":note})
        db.session.commit()
    return redirect("/")

@app.route("/save/<int:id>", methods=["POST"])
def save(id):
    name = request.form["name"]
    if len(name) > 50:
        return render_template("error.html", error="Name is too long")
    describtion = request.form["describtion"]
    if len(describtion) > 10000:
        return render_template("error.html", error="Describiton is too long")
    sql = text("UPDATE Locations SET name=:name, describtion=:describtion WHERE id=:id")
    db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/save_npc/<int:id>", methods=["POST"])
def save_npc(id):
    name = request.form["name"]
    if len(name) > 50:
        return render_template("error.html", error="Name is too long")
    describtion = request.form["describtion"]
    if len(describtion) > 10000:
        return render_template("error.html", error="Describiton is too long")
    sql = text("UPDATE Npcs SET name=:name, describtion=:describtion WHERE id=:id")
    db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
    db.session.commit()
    return redirect("/")

@app.route("/npc/<int:id>")
def npc(id):
    sql = text('SELECT id, name, describtion FROM Npcs WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    npc = result.fetchone()
    return render_template("npc.html", npc=npc)

@app.route("/location_note/<int:id>")
def location_note(id):
    sql = text('SELECT id, note FROM Location_notes WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    note = result.fetchone()
    return render_template("note.html", note=note)

@app.route("/region/<int:id>")
def region(id):
    sql = text('SELECT id, name, describtion FROM Locations WHERE id=:id')
    result = db.session.execute(sql, {"id":id})
    place = result.fetchone()
    sql = text('SELECT id, name FROM Npcs WHERE Npcs.location_id=:id ORDER BY id')
    result = db.session.execute(sql, {"id":id})
    npcs = result.fetchall()
    user = users.id()
    sql = text('SELECT id, note FROM Location_notes WHERE Location_notes.location_id=:id AND Location_notes.user_id=:user ORDER BY id')
    result = db.session.execute(sql, {"id":id, "user":user})
    notes = result.fetchall()
    return render_template("location.html", place=place, npcs=npcs, notes=notes)

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
            return render_template("error.html", message="Passwords are different")
        if users.register(username, password1, usertype):
            users.is_admin(username)
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed")
