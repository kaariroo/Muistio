import app
from sqlalchemy.sql import text


def send(name, describtion, table, region):
    try:
        if table == "Locations":
            sql = text("INSERT INTO Locations (name,describtion) VALUES (:name,:describtion)")
            app.db.session.execute(sql, {"name":name, "describtion":describtion})
        elif table == "Npcs":
            sql = text("INSERT INTO Npcs (name,describtion,location_id) VALUES (:name,:describtion,:region)")
            app.db.session.execute(sql, {"name":name, "describtion":describtion, "region":region})
        app.db.session.commit()
    except:
        return "Sure you didn't choose a name already in use?"
    return True

def save(id, name, describtion, table):
    try:
        if table == "Locations":
            sql = text("UPDATE Locations SET name=:name, describtion=:describtion WHERE id=:id")
            app.db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
        elif table == "Npcs":
            sql = text("UPDATE Npcs SET name=:name, describtion=:describtion WHERE id=:id")
            app.db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
        app.db.session.commit()
    except:
        return "Sure you didn't choose a name already in use?"
    return True

def save_note(note, user, target, table):
    if table == "Locations":
        sql = text("INSERT INTO Location_notes (note,location_id,user_id) VALUES (:note,:target,:user_id)")
    elif table == "Npcs":
        sql = text("INSERT INTO Npc_notes (note,npc_id,user_id) VALUES (:note,:target,:user_id)")
    app.db.session.execute(sql, {"note":note, "user_id":user, "target":target})
    app.db.session.commit()
    return True

def delete(id, table):
    if table == "Npcs":
        sql = text("DELETE FROM Npc_notes WHERE npc_id=:id")
        app.db.session.execute(sql, {"id":id})
        app.db.session.commit()
        sql = text("DELETE FROM Npcs WHERE id=:id")
        app.db.session.execute(sql, {"id":id})
        app.db.session.commit()
    elif table == "Npc_notes":
        sql = text("DELETE FROM Npc_notes WHERE id=:id")
        app.db.session.execute(sql, {"id":id})
        app.db.session.commit()
    return True


def get_id(name):
    sql = text("SELECT id FROM Locations WHERE name=:name")
    result = app.db.session.execute(sql, {"name":name})
    return result.fetchone()[0]

def get_one(id, table):
    if table == "Locations":
        sql = text('SELECT id, name, describtion FROM Locations WHERE id=:id')
    elif table == "Npcs":
        sql = text("SELECT id, name, describtion FROM Npcs WHERE id=:id")
    elif table == "Location_note":
        sql = text("SELECT id, note FROM Location_notes WHERE id=:id")
    elif table == "Npc_notes":
        sql = text("SELECT id, note FROM Npc_notes WHERE id=:id")
    result = app.db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_all(table):
    if table == "Locations":
        result = app.db.session.execute(text('SELECT id, name, describtion FROM Locations ORDER BY id'))
    elif table == "Npcs":
        result = app.db.session.execute(text('SELECT id, name, describtion FROM Npcs ORDER BY id'))
    return result.fetchall()
    
def get_locations_npcs(id):
    sql = text('SELECT id, name FROM Npcs WHERE Npcs.location_id=:id ORDER BY id')
    result = app.db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_notes(id, user, table):
    if table == "Locations":
        sql = text('SELECT id, note FROM Location_notes WHERE Location_notes.location_id=:id AND Location_notes.user_id=:user ORDER BY id')
    if table == "Npcs":
        sql = text('SELECT id, note FROM Npc_notes WHERE Npc_notes.npc_id=:id AND Npc_notes.user_id=:user ORDER BY id')
    result = app.db.session.execute(sql, {"id":id, "user":user})
    return result.fetchall()

