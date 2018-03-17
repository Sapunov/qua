CREATE USER quauser WITH PASSWORD 'somestrongdbpassword';

CREATE DATABASE qua_controller;
CREATE DATABASE qua_suggests;

GRANT ALL PRIVILEGES ON DATABASE qua_controller to quauser;
GRANT ALL PRIVILEGES ON DATABASE qua_suggests to quauser;

ALTER USER quauser CREATEDB;
