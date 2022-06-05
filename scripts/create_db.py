from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY,
    email VARCHAR(256),
    password VARCHAR(256),
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    nickname VARCHAR(256),
    create_at VARCHAR(256)
    );""")

    session.execute("""CREATE TABLE auth_token (
    id INTEGER NOT NULL PRIMARY KEY,
    token VARCHAR(256),
    user_id INTEGER REFERENCES users,
    create_at VARCHAR(256)
    );""")

    session.execute("""CREATE TABLE stream (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    title VARCHAR(256),
    topic VARCHAR(256),
    status VARCHAR(256),
    create_at VARCHAR(256)
    );""")

    session.close()


if __name__ == '__main__':
    main()
