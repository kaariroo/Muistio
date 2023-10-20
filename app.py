from os import getenv
from sqlalchemy.sql import text
from flask import Flask
from flask import url_for
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
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
        return render_template("error.html", error="Registration failed")

@app.route("/npc/<int:npc_id>")
def npc(npc_id):
    table = "Npcs"
    npc_data = operations.get_one(npc_id, table)
    user = users.id()
    notes = operations.get_notes(npc_id, user, table)
    return render_template("npc.html", npc=npc_data, notes=notes)

@app.route("/region/<int:region_id>")
def region(region_id):
    table = "Locations"
    place = operations.get_one(region_id, table)
    npcs = operations.get_locations_npcs(region_id)
    user = users.id()
    notes = operations.get_notes(region_id, user, table)
    return render_template("location.html", place=place, npcs=npcs, notes=notes)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/new_npc")
def new_npc():
    table = "Locations"
    places = operations.get_all(table)
    return render_template("new_npc.html", places=places)

@app.route("/new_location_note/<int:region_id>")
def new_location_note(region_id):
    table = "Locations"
    place = operations.get_one(region_id, table)
    return render_template("new_location_note.html", place=place)

@app.route("/new_npc_note/<int:npc_id>")
def new_npc_note(npc_id):
    table = "Npcs"
    npc_data = operations.get_one(npc_id, table)
    return render_template("new_npc_note.html", npc=npc_data)

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Locations"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check is not True:
        return render_template("error.html", error=name_check)
    location = None
    result = operations.send(name, describtion, table, location)
    if result is not True:
        return render_template("error.html", error=result)
    return redirect("/")

@app.route("/send_npc", methods=["POST"])
def send_npc():
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Npcs"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check is not True:
        return render_template("error.html", error=name_check)
    try:
        location = request.form["region"]
    except:
        return render_template("error.html", error="Choose a region")
    result = operations.send(name, describtion, table, location)
    if result is not True:
        return render_template("error.html", error=result)
    return redirect("/")
 
@app.route("/send_location_note/<int:region_id>", methods=["POST"])
def send_location_note(region_id):
    note = request.form["note"]
    table = "Locations"
    name_check = input_check.check_note(note)
    if name_check is not True:
        return render_template("error.html", error=name_check)
    user = users.id()
    operations.send_note(note, user, region_id, table)
    return redirect("/")

@app.route("/send_npc_note/<int:npc_id>", methods=["POST"])
def send_npc_note(npc_id):
    note = request.form["note"]
    table = "Npcs"
    name_check = input_check.check_note(note)
    if name_check is not True:
        return render_template("error.html", error=name_check)
    user = users.id()
    operations.send_note(note, user, npc_id, table)
    return redirect("/")

@app.route("/edit/<int:region_id>")
def edit(region_id):
    table = "Locations"
    place = operations.get_one(region_id, table)
    return render_template("edit.html", place=place)

@app.route("/edit_npc/<int:npc_id>")
def edit_npc(npc_id):
    table = "Npcs"
    npc_data = operations.get_one(npc_id, table)
    return render_template("edit_npc.html", npc=npc_data)

@app.route("/edit_location_note/<int:note_id>")
def edit_location_note(note_id):
    table = "Location_note"
    note = operations.get_one(note_id, table)
    return render_template("edit_location_note.html", note=note)

@app.route("/edit_npc_note/<int:npc_id>")
def edit_npc_note(npc_id):
    table = "Npc_notes"
    note = operations.get_one(npc_id, table)
    return render_template("edit_npc_note.html", note=note)

@app.route("/save/<int:region_id>", methods=["POST"])
def save(region_id):
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Locations"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check is not True:
        return render_template("error.html", error=name_check)
    result = operations.save(region_id, name, describtion, table)
    if result is not True:
        return render_template("error.html", error=result)
    return redirect("/")

@app.route("/save_npc/<int:npc_id>", methods=["POST"])
def save_npc(npc_id):
    name = request.form["name"]
    describtion = request.form["describtion"]
    table = "Npcs"
    name_check = input_check.check_name_and_describtion(name, describtion)
    if name_check is not True:
        return render_template("error.html", error=name_check)
    result = operations.save(npc_id, name, describtion, table)
    if result is not True:
        return render_template("error.html", error=result)
    return redirect("/")

@app.route("/save_location_note/<int:note_id>", methods=["POST"])
def save_location_note(note_id):
    table = "Location_note"
    note = request.form["note"]
    note_check = input_check.check_note(note)
    if note_check is not True:
        return render_template("error.html", error=note_check)
    operations.save_note(note_id, note, table)
    return redirect("/")

@app.route("/save_npc_note/<int:note_id>", methods=["POST"])
def save_npc_note(note_id):
    table = "Npc_note"
    note = request.form["note"]
    note_check = input_check.check_note(note)
    if note_check is not True:
        return render_template("error.html", error=note_check)
    operations.save_note(note_id, note, table)
    return redirect("/")

@app.route("/confirm_delete_npc/<int:npc_id>")
def confirm_delete_npc(npc_id):
    table = "Npcs"
    npc_data = operations.get_one(npc_id, table)
    return render_template("delete_npc.html", npc=npc_data)

@app.route("/confirm_delete_npc_note/<int:npc_id>")
def confirm_delete_npc_note(npc_id):
    table = "Npc_notes"
    note = operations.get_one(npc_id, table)
    return render_template("delete_npc_note.html", note=note)

@app.route("/delete_npc/<int:npc_id>", methods=["POST"])
def delete_npc(npc_id):
    table = "Npcs"
    operations.delete(npc_id, table)
    return redirect("/")

@app.route("/delete_npc_note/<int:note_id>", methods=["POST"])
def delete_npc_note(note_id):
    table = "Npc_notes"
    operations.delete(note_id, table)
    return redirect("/")
