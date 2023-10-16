import app
from sqlalchemy.sql import text

def check_name_and_describtion(name, describtion):
    if len(name) < 1:
        return "Name cannot be empty"
    elif len(name) > 50:
        return "Name is too long"
    elif len(describtion) < 1:
        return "Describtion cannot be empty"
    elif len(describtion) > 10000:
        return "Describtion is too long"
    else:
        return True
    
def check_if_name_in_use(name, table):
    if table == "Locations":
        sql = text('SELECT id FROM Locations WHERE name=:name')
        result = app.db.session.execute(sql, {"name":name})
        if result.fetchone() != None:
            return "Name taken!"
        return True
    elif table == "Npcs":
        sql = text('SELECT id FROM Npcs WHERE name=:name')
        result = app.db.session.execute(sql, {"name":name})
        if result.fetchone() != None:
            return "Name taken!"
        return True
    
def check_note(note):
    if len(note) > 10000:
        return "Note too long"
    elif len(note) < 1:
        return "delete"
    else:
        return True

