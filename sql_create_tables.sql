-- Creator:       MySQL Workbench 6.3.9/ExportSQLite Plugin 0.1.0
-- Author:        Unknown
-- Caption:       New Model
-- Project:       Name of the project
-- Changed:       2017-07-31 15:08
-- Created:       2017-07-31 11:54

BEGIN;
CREATE TABLE browsers(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45),
  "version" VARCHAR(45),
  "os" VARCHAR(45),
  CONSTRAINT "id_UNIQUE"
    UNIQUE("id")
);
CREATE TABLE users(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "firstName" VARCHAR(45),
  "lastName" VARCHAR(45),
  CONSTRAINT "idUsers_UNIQUE"
    UNIQUE("id")
);
CREATE TABLE websites(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45),
  "jahia" TEXT,
  "wordpress" TEXT,
  "userview" TEXT,
  "userpwd" TEXT,
  CONSTRAINT "id_UNIQUE"
    UNIQUE("id")
);
CREATE TABLE logs(
  "date" DATETIME NOT NULL,
  "status" VARCHAR(45),
  "userId" INTEGER NOT NULL,
  "browserId" INTEGER NOT NULL,
  "websiteId" INTEGER NOT NULL,
  PRIMARY KEY("websiteId","userId","browserId","date"),
    FOREIGN KEY("browserId")
    REFERENCES browsers("id")
    ON UPDATE CASCADE,
    FOREIGN KEY("websiteId")
    REFERENCES websites("id")
    ON UPDATE CASCADE,
    FOREIGN KEY("userId")
    REFERENCES users("id")
    ON UPDATE CASCADE
);
COMMIT;
