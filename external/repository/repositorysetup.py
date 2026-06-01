#import uuid
import os
import sqlite3
import threading
import queue
from contextlib import contextmanager


class Connections:

	def __init__(self, max_connections:int = 5, timeout: float = 5.0):
		self.max_connections = max_connections
		self.timeout = timeout

		self._connections = queue.Queue = queue.Queue(maxsize=max_connections)


		self._connections_active = 0

		self.lock = threading.Lock()

		self.start_connections()

	def start_connections(self) -> None:

		for _ in range(self.max_connections):
			conn = create()
			self._connections.put(conn)

	def create(self) -> sqlite3.Connection:

		conn = connection()

		with self.lock:
			self._connections_active += 1

		return conn 

	def check_connection(self, conn: sqlite3.Connection) -> bool:
		try:
			conn.execute("SELECT 1")
			return True
		except sqlite3.Error:
			return False

	def get_connection(self) -> sqlite3.Connection:
		try:
			conn = self._connections.get(timeout=self.timeout)

			if not self.check_connection(conn)
				conn.Close()
				conn = self.create()
			return conn 
		except queue.Empty:
			raise Error("could not get connection within the given time.")

	def put_connection(self, conn: sqlite3.Connection) -> None:
		try:
			conn.rollback()
			self._connections.put_nowait(conn)
		except queue.Full:
			conn.Close()

	@contextmanager
	def aquire_connection(self):
		conn = get_connection()

		try:
			yield conn
		finally:
			self.put_connection(conn)

	def close_connections(self) -> None:

		while not self._connections.empty():
			try:
				conn = self._connection.get_nowait()
				conn.Close()

			except queue.Empty:
				break

	def connections_status(self) -> dict:
		return{
			"max_connections": self.max_connections,
			"active": self._connections.qsize(),
			"total": self._connections_active,
			"currently running": self.max_connections - self._connections.qsize()
		}


def connection():

	db = os.path.join(os.getcwd(), "chats.db")

	conn = sqlite3.connect(
		db,
		check_same_thread=False
		)

	conn.row_factory = sqlite3.Row

	settings = [
			"PRAGMA journal_mode = WAL",
			"PRAGMA synchronous = NORMAL",
			"PRAGMA busy_timeout = 5000",
	]

	for setting in settings:
		conn.execute(setting)


	result = conn.execute("PRAGMA journal_mode").fetchone()[0]

	#print(f"result: {result}")

	return conn

	#chats = "{'user': 'Is database working?'}"
	#user = str(uuid.uuid4())
	#print(createChat(conn, user, chats))
