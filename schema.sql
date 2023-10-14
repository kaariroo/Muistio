CREATE TABLE Locations (id SERIAL PRIMARY KEY, name TEXT UNIQUE, describtion TEXT);

CREATE TABLE Npcs (id SERIAL PRIMARY KEY, name TEXT, describtion TEXT, location_id INTEGER REFERENCES Locations);

CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, usertype TEXT);

CREATE TABLE Location_notes (id SERIAL PRIMARY KEY, note TEXT, user_id INTEGER REFERENCES Users, location_id INTEGER REFERENCES Locations);
