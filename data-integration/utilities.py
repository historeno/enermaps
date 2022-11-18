import os
import time

import sqlalchemy


def get_engine() -> sqlalchemy.engine.Engine:
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_DB")
    # DB_URL = postgresql://test:example@db:5432/dataset
    DB_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_DB=DB_NAME,
    )
    if "None" in DB_URL:
        raise ValueError(f"The database url is not correct : {DB_URL}")
    # DB_URL = "postgresql://postgres:postgres@localhost:5432/dataset"
    time.sleep(15)
    engine = sqlalchemy.create_engine(url=DB_URL)
    print(f"DATA BASE URL : {DB_URL}")
    try:
        connection = engine.connect()
        connection.close()
    except Exception:
        raise NotImplementedError
    return engine
