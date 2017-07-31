BEGIN;
CREATE TABLE browsers(
  id INTEGER PRIMARY KEY NOT NULL,
  name VARCHAR(45),
  version VARCHAR(45),
  os VARCHAR(45)
);
CREATE TABLE users(
  id INTEGER PRIMARY KEY NOT NULL,
  firstName VARCHAR(45),
  lastName VARCHAR(45)
);
CREATE TABLE websites(
  id INTEGER PRIMARY KEY NOT NULL,
  name VARCHAR(45),
  jahia TEXT,
  wordpress TEXT,
  userview TEXT,
  userpwd TEXT
);
CREATE TABLE logs(
  date DATETIME NOT NULL,
  status VARCHAR(45),
  userId INTEGER NOT NULL,
  browserId INTEGER NOT NULL,
  websiteId INTEGER NOT NULL,
  PRIMARY KEY(browserId, websiteId, userId)
 FOREIGN KEY(browserId)
 REFERENCES browsers(id)
 ON UPDATE CASCADE,
 FOREIGN KEY(websiteId)
 REFERENCES websites(id)
 ON UPDATE CASCADE,
 FOREIGN KEY(userId)
 REFERENCES users(id)
 ON UPDATE CASCADE
);
COMMIT;
