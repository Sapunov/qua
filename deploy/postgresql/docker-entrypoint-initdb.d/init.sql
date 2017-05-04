CREATE USER quauser WITH PASSWORD 'somestrongdbpassword';

CREATE DATABASE qua;
CREATE DATABASE qua_suggests;

GRANT ALL PRIVILEGES ON DATABASE qua to quauser;
GRANT ALL PRIVILEGES ON DATABASE qua_suggests to quauser;

ALTER USER quauser CREATEDB;
