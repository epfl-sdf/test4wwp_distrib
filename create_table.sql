-- Creator:       MySQL Workbench 6.3.9/ExportSQLite Plugin 0.1.0
-- Author:        Unknown
-- Caption:       New Model
-- Project:       Name of the project
-- Changed:       2017-08-02 11:04
-- Created:       2017-07-31 11:54
PRAGMA foreign_keys = ON;

-- Schema: 

BEGIN;
CREATE TABLE "users"(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "first_name" VARCHAR(45),
  "last_name" VARCHAR(45),
  CONSTRAINT "idUsers_UNIQUE"
    UNIQUE("id")
);
CREATE TABLE "websites"(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45),
  "jahia" TEXT,
  "wordpress" TEXT,
  "userview" TEXT,
  "userpwd" TEXT,
  CONSTRAINT "id_UNIQUE"
    UNIQUE("id")
);
CREATE TABLE "browsers"(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45),
  "version" VARCHAR(45),
  "os" VARCHAR(45),
  CONSTRAINT "id_UNIQUE"
    UNIQUE("id")
);
CREATE TABLE "browsers_sites"(
  "browser_id" INTEGER NOT NULL,
  "website_id" INTEGER NOT NULL,
  PRIMARY KEY("browser_id","website_id"),
  FOREIGN KEY("browser_id") REFERENCES "browsers"("id"),
  FOREIGN KEY("website_id") REFERENCES "websites"("id")
);
CREATE TABLE "assigned_websites"(
  "user_id" INTEGER NOT NULL,
  "browser_id" INTEGER NOT NULL,
  "website_id" INTEGER NOT NULL,
  PRIMARY KEY("user_id","browser_id", "website_id"),
  FOREIGN KEY("user_id") REFERENCES "users"("id"),
  FOREIGN KEY("browser_id") REFERENCES "browsers"("id")
  FOREIGN KEY("website_id") REFERENCES "websites"("id")
);
CREATE TABLE "logs"(
  "user_id" INTEGER NOT NULL,
  "browser_id" INTEGER NOT NULL,
  "website_id" INTEGER NOT NULL,
  "date" DATETIME NOT NULL,
  "status" VARCHAR(45),
  PRIMARY KEY("user_id","browser_id", "website_id", "date"),
  FOREIGN KEY("user_id") REFERENCES "users"("id"),
  FOREIGN KEY("browser_id") REFERENCES "browsers"("id")
  FOREIGN KEY("website_id") REFERENCES "websites"("id")
);
COMMIT;
