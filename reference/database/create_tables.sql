-- Library names table
CREATE TABLE "library_names" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "name" TEXT NOT NULL,
  UNIQUE ("id", "name")
);

-- External locations table
CREATE TABLE "external_locations" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "name" TEXT NOT NULL,
  UNIQUE ("id", "name")
);

-- Status names tables
CREATE TABLE "status_names" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "value" TEXT NOT NULL,
  UNIQUE ("id", "value")
);

-- Main table
CREATE TABLE "main" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "title" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'Archived',
  "date" TEXT NOT NULL,
  "date_time_start" TEXT NOT NULL,
  "date_time_end" TEXT NOT NULL,
  "library_name" TEXT NOT NULL,
  "external_location" TEXT NOT NULL,
  "person" TEXT NOT NULL,
  "email" TEXT NOT NULL,
  "invite_sent" INTEGER,
  CHECK (
    date LIKE '____-__-__ __:__:__'
    AND SUBSTR(date, 6, 2) BETWEEN '01' AND '12'
    AND SUBSTR(date, 9, 2) BETWEEN '01' AND '31'
  ),
  CHECK (
    date_time_start LIKE '____-__-__ __:__:__'
    AND SUBSTR(date_time_start, 6, 2) BETWEEN '01' AND '12'
    AND SUBSTR(date_time_start, 9, 2) BETWEEN '01' AND '31'
    AND SUBSTR(date_time_start, 12, 2) BETWEEN '00' AND '23'
    AND SUBSTR(date_time_start, 15, 2) BETWEEN '00' AND '59'
    AND SUBSTR(date_time_start, 18, 2) BETWEEN '00' AND '59'
  ),
  CHECK (
    date_time_end LIKE '____-__-__ __:__:__'
    AND SUBSTR(date_time_end, 6, 2) BETWEEN '01' AND '12'
    AND SUBSTR(date_time_end, 9, 2) BETWEEN '01' AND '31'
    AND SUBSTR(date_time_end, 12, 2) BETWEEN '00' AND '23'
    AND SUBSTR(date_time_end, 15, 2) BETWEEN '00' AND '59'
    AND SUBSTR(date_time_end, 18, 2) BETWEEN '00' AND '59'
  ),
  CHECK (email LIKE '%_@nypl.org'),
  CHECK (
    invite_sent IN (0, 1)
    OR invite_sent IS NULL
  ),
  UNIQUE ("id"),
  FOREIGN KEY ("library_name") REFERENCES "library_names" ("name"),
  FOREIGN KEY ("external_location") REFERENCES "external_locations" ("name"),
  FOREIGN KEY ("status") REFERENCES "status" ("value")
);
