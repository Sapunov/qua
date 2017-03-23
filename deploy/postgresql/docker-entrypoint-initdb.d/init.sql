CREATE USER quauser WITH PASSWORD 'somestrongpassword';

CREATE DATABASE qua;
CREATE DATABASE qua_search_int;

GRANT ALL PRIVILEGES ON DATABASE qua to quauser;
GRANT ALL PRIVILEGES ON DATABASE qua_search_int to quauser;
ALTER USER quauser CREATEDB;
