import os
import sqlite3

try:
    database_url = os.environ["DATABASE_URL"]
    print(database_url)
except KeyError:
    raise RuntimeError("The DATABASE_URL environment variable is missing.")

database = sqlite3.connect(database_url)
