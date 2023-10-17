from sqlalchemy.sql import text
from flask import Flask
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
    table = "Locations"
    places = operations.get_all(table)
    table = "Npcs"
    npcs = operations.get_all(table)
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
        
@app.route("/npc/<int:id>")
def npc(id):
    table = "Npcs"
    npc = operations.get_one(id, table)
    user = users.id()
    notes = operations.get_notes(id, user, table)
    return render_template("npc.html", npc=npc, notes=notes)

@app.route("/region/<int:id>")
def region(id):
    table = "Locations"
    place = operations.get_one(id, table)
    npcs = operations.get_locations_npcs(id)
    user = users.id()
    notes = operations.get_notes(id, user, table)
    return render_template("location.html", place=place, npcs=npcs, notes=notes)        

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/new_npc")
def new_npc():
    table = "Locations"
    places = operations.get_all(table)
    return render_template("new_npc.html", places=places)

@app.route("/new_location_note/<int:id>")
def new_location_note(id):
    table = "Locations"
    place = operations.get_one(id, table)
    return render_template("new_location_note.html", place=place)

@app.route("/new_npc_note/<int:id>")
def new_npc_note(id):
    table = "Npcs"
    npc = operations.get_one(id, table)
    return render_template("new_npc_note.html", npc=npc)

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Locations"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check != True:
        return render_template("error.html", error=name_check)
    region = None
    result = operations.send(name, describtion, table, region)
    if result != True:
        return render_template("error.html", error=result)
    return redirect("/")

@app.route("/send_npc", methods=["POST"])
def send_npc():
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Npcs"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check != True:
        return render_template("error.html", error=name_check)
    try:
        region = request.form["region"]
    except:
        return render_template("error.html", error="Choose a region") 
    result = operations.send(name, describtion, table, region)
    if result != True:
        return render_template("error.html", error=result)
    return redirect("/")
 
    
@app.route("/send_location_note/<int:id>", methods=["POST"])
def send_location_note(id):
    note = request.form["note"]
    table = "Locations"
    name_check = input_check.check_note(note)
    if name_check != True:
        return render_template("error.html", error=name_check)
    user = users.id()
    operations.save_note(note, user, id, table)
    return redirect("/")

@app.route("/send_npc_note/<int:id>", methods=["POST"])
def send_npc_note(id):
    note = request.form["note"]
    table = "Npcs"
    name_check = input_check.check_note(note)
    if name_check != True:
        return render_template("error.html", error=name_check)
    user = users.id()
    operations.save_note(note, user, id, table)
    return redirect("/")

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
    table = "Location_note"
    note = operations.get_one(id, table)
    return render_template("edit_location_note.html", note=note)

@app.route("/edit_npc_note/<int:id>")
def edit_npc_note(id):
    table = "Npc_notes"
    note = operations.get_one(id, table)
    return render_template("edit_npc_note.html", note=note)

@app.route("/save/<int:id>", methods=["POST"])
def save(id):
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Locations"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check != True:
        return render_template("error.html", error=name_check)
    result = operations.save(id, name, describtion, table)
    if result != True:
        return render_template("error.html", error=result)
    return redirect("/")

@app.route("/save_npc/<int:id>", methods=["POST"])
def save_npc(id):
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Npcs"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check != True:
        return render_template("error.html", error=name_check)
    result = operations.save(id, name, describtion, table)
    if result != True:
        return render_template("error.html", error=result)
    return redirect("/")

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

@app.route("/save_npc_note/<int:id>", methods=["POST"])
def save_npc_note(id):
    note = request.form["note"]
    note_check = input_check.check_note(note)
    if note_check == "delete":
        sql = text("DELETE From Npc_notes WHERE id=:id")
        db.session.execute(sql, {"id":id, "note":note})
        db.session.commit()
    elif note_check != True:
        return render_template("error.html", error=note_check)
    else:
        sql = text("UPDATE Npc_notes SET note=:note WHERE id=:id")
        db.session.execute(sql, {"id":id, "note":note})
        db.session.commit()
    return redirect("/")

@app.route("/confirm_delete_npc/<int:id>")
def confirm_delete_npc(id):
    table = "Npcs"
    npc = operations.get_one(id, table)
    return render_template("delete_npc.html", npc=npc)

@app.route("/confirm_delete_npc_note/<int:id>")
def confirm_delete_npc_note(id):
    table = "Npc_notes"
    note = operations.get_one(id, table)
    return render_template("delete_npc_note.html", note=note)

@app.route("/delete_npc/<int:id>", methods=["POST"])
def delete_npc(id):
    table = "Npcs"
    operations.delete(id, table)
    return redirect("/")

@app.route("/delete_npc_note/<int:id>", methods=["POST"])
def delete_npc_note(id):
    table = "Npc_notes"
    operations.delete(id, table)
    return redirect("/")





