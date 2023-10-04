CREATE TABLE Npcs (id SERIAL PRIMARY KEY, name TEXT, describtion TEXT, location_id INTEGER REFERENCES Locations);

CREATE TABLE Locations (id SERIAL PRIMARY KEY, name TEXT, describtion TEXT);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);

CREATE TABLE Location_notes (id SERIAL PRIMARY KEY, note TEXT, user_id INTEGER REFERENCES users, location_id INTEGER REFERENCES Locations);