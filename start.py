from os import path
from sqlite3 import connect

def createDataBase() -> None:
	with connect('db/db.sqlite3') as conn:
		cur = conn.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS token_list (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			token TEXT,
			status INTEGER DEFAULT 1
			)""")

if path.exists('db/db.sqlite3'):
	pass
else:
	createDataBase()
