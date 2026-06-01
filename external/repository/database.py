import sqlite3
import json
from .repositorySetup import Connections

connect = Connections()

def createChat(user_session, chats):

	with connect.acquire_connection() as conn:
		conn.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, name TEXT)")

		text = json.dumps(chats)

		user_id = conn.execute("INSERT INTO chats (user, name) VAlUES (?, ?) RETURNING id",(user_session, text)).fetchone()[0]

		conn.commit()

	return result

def readChat(user_id):

	with connect.acquire_connection() as conn:
		result = conn.execute("SELECT name FROM chats WHERE id=?",(user_id,))

	data = json.loads(result)
	return data

def readChats(user_session):

	with connect.acquire_connection() as conn:
		result = conn.execute("SELECT name FROM chats WHERE user=?",(user_session,))

	data = json.loads(result)
	return data
	
def updateChats(chats, user_id):

	with connect.acquire_connection() as conn:
		text = json.dumps(chats)
		conn.execute("UPDATE users SET name = ? WHERE id = ?", (text, user_id))
		conn.commit()

def removeChats(user):

	with connect.acquire_connection() as conn:
		conn.execute("DELETE FROM chats WHERE id = ?", (user_session,))
		conn.commit()