from sqlite3 import connect

class Auth:
	def __init__(self, *, token: str) -> None:
		self.token = token

	def tokenCheck(self):
		with connect('./db/db.sqlite3') as conn:
			cur = conn.cursor()
			cur.execute(f"SELECT status FROM token_list WHERE token = '{self.token}'")
			if cur.fetchone() is None:
				exit(0)
			else:
				pass