import sqlite3
import json
from .repositorySetup import Connections
import atexit
import signal 
import sys
import uuid
from datetime import datetime, timezone

connect = Connections()

def createChat(user_session, chats):

	with connect.acquire_connection() as connection:
		conn = connection.cursor()
		conn.execute("CREATE TABLE IF NOT EXISTS chats (id TEXT PRIMARY KEY, user TEXT, name TEXT, createdAt TEXT, updatedAt TEXT)")

		text = json.dumps(chats)

		user_id = str(uuid.uuid4())

		time_format = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")

		conn.execute("INSERT INTO chats (id, user, name, createdAt) VAlUES (?, ?, ?, ?)",(user_id, user_session, text, time_format))

	return user_id 

def readChat(user_id):

	with connect.acquire_connection() as connection:
		conn = connection.cursor()
		conn.execute("SELECT name FROM chats WHERE id=?",(user_id,))

		row = conn.fetchone()

		if row:
			result = row[0]

			data = json.loads(result)

	return data

def readChats(user_session):

	with connect.acquire_connection() as connection:
		conn = connection.cursor()
		conn.execute("SELECT name FROM chats WHERE user=?",(user_session,))

		rows = conn.fetchall()

		for row in rows:
			result = row[0]

			data = json.loads(result)
	return data
	
def updateChats(chats, user_id):

	with connect.acquire_connection() as conn:

		time_format = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
		text = json.dumps(chats)
		conn.execute("UPDATE chats SET name = ?,updatedAt = ? WHERE id = ?", (text, time_format, user_id))

def removeChats(user):

	with connect.acquire_connection() as conn:
		conn.execute("DELETE FROM chats WHERE id = ?", (user_session,))


atexit.register(connect.close_connections)

def handle_signals(signum, frame):

	try:
		connect.close_connections()
	except Exception as e:
		Error("error during closing of connections")
	sys.exit(0)

signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)