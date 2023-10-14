import app
from sqlalchemy.sql import text


def send(name, describtion, table, region):
    if table == "Locations":
        sql = text("INSERT INTO Locations (name,describtion) VALUES (:name,:describtion)")
        app.db.session.execute(sql, {"name":name, "describtion":describtion})
    elif table == "Npcs":
        sql = text("INSERT INTO Npcs (name,describtion,location_id) VALUES (:name,:describtion,:region)")
        app.db.session.execute(sql, {"name":name, "describtion":describtion, "region":region})
    app.db.session.commit()
    return True

def save(id, name, describtion, table):
    if table == "Locations":
        sql = text("UPDATE Locations SET name=:name, describtion=:describtion WHERE id=:id")
        app.db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
    elif table == "Npcs":
        sql = text("UPDATE Npcs SET name=:name, describtion=:describtion WHERE id=:id")
        app.db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
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
    elif table == "Note":
        sql = text("SELECT id, note FROM Location_notes WHERE id=:id")
    result = app.db.session.execute(sql, {"id":id})
    return result.fetchone()
    
def get_locations_npcs(id):
    sql = text('SELECT id, name FROM Npcs WHERE Npcs.location_id=:id ORDER BY id')
    result = app.db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_notes(id, user):
    sql = text('SELECT id, note FROM Location_notes WHERE Location_notes.location_id=:id AND Location_notes.user_id=:user ORDER BY id')
    result = app.db.session.execute(sql, {"id":id, "user":user})
    return result.fetchall()

