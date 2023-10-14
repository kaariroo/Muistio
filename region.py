import app
from sqlalchemy.sql import text


def send(name, describtion):
    sql = text("INSERT INTO Locations (name,describtion) VALUES (:name,:describtion)")
    app.db.session.execute(sql, {"name":name, "describtion":describtion})
    app.db.session.commit()
    return True

def save(name, describtion):
    sql = text("UPDATE Locations SET name=:name, describtion=:describtion WHERE id=:id")
    app.db.session.execute(sql, {"id":id, "name":name, "describtion":describtion})
    app.db.session.commit()
    return True

def check_if_excists(name):
    sql = text("SELECT * FROM Locations WHERE name=:name")
    result = app.db.session.execute(sql, {"name":name})
    print(result.fetchone())
    return True
