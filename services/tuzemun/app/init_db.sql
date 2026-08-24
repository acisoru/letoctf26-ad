CREATE TABLE IF NOT EXISTS users (
  id SERIAL,
  username VARCHAR(40),
  email VARCHAR(40),
  password VARCHAR,

  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS users_extra_data (
  id SERIAL, 
  userid INT,
  fio VARCHAR(100),
  passport VARCHAR(100),
  approved BOOLEAN,

  PRIMARY KEY(id),
  CONSTRAINT fk_user
    FOREIGN KEY(userid)
      REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS requests (
  id SERIAL,
  userid INT,

  PRIMARY KEY(id),
  CONSTRAINT fk_user
    FOREIGN KEY(userid)
      REFERENCES users(id)
);
