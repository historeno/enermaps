import os
import time

import psycopg2 as ps
import sqlalchemy

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_DB")
DB_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
    DB_HOST=DB_HOST,
    DB_PORT=DB_PORT,
    DB_USER=DB_USER,
    DB_PASSWORD=DB_PASSWORD,
    DB_DB=DB_NAME,
)


def get_engine() -> sqlalchemy.engine.Engine:
    if "None" in DB_URL:
        raise ValueError(f"The database url is not correct : {DB_URL}")
    time.sleep(15)
    engine = sqlalchemy.create_engine(url=DB_URL)
    print(f"DATA BASE URL : {DB_URL}")
    try:
        connection = engine.connect()
        connection.close()
    except Exception:
        raise NotImplementedError
    return engine


def remove_dataset(ds_id, engine):
    with engine.connect() as con:
        tables = ["datasets", "spatial", "data"]
        for table in tables:
            con.execute(f"DELETE FROM {table} WHERE ds_id = {ds_id};")
            print(f"{table} deleted")


def remove_lengends(engine):
    with engine.connect() as con:
        con.execute("DELETE FROM visualization;")
    print("lengends deleted")


# def datasetExists(
#     ds_id,
#     dbURL=DB_URL,
#     tables=["datasets", "spatial", "data"],
# ):
#     lengths = []
#     for table in tables:
#         with ps.connect(dbURL) as conn:
#             cur = conn.cursor()
#             cur.execute(
#                 ps.SQL("SELECT COUNT(*) FROM {} WHERE ds_id = %(ds_id)s;").format(
#                     ps.Identifier(table)
#                 ),
#                 {"ds_id": ds_id},
#             )
#             count = cur.fetchone()[0]
#             lengths.append(count)
#     print(lengths)
#     print(lengths)
#     print(lengths)
#     if lengths[0] > 0 or lengths[1] > 0 or lengths[2] > 0:
#         return True
#     else:
#         return False
