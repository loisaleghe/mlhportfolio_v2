-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;

-- CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   username TEXT UNIQUE NOT NULL,
--   password TEXT NOT NULL
-- );

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );


class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.Sring(), primary_key=True)
    password = db.Column(db.String())

    def __init__(seld, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"