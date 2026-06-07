import os
import sqlite3
import threading
import queue
from contextlib import contextmanager
import stat


class Connections:

	def __init__(self, max_connections:int = 5, timeout: float = 5.0):

		self.max_connections = max_connections
		self.timeout = timeout
		self._connections: queue.Queue = queue.Queue(maxsize=max_connections)
		self._connections_active = 0
		self.lock = threading.Lock()
		self.start_connections()

	def start_connections(self) -> None:

		for _ in range(self.max_connections):
			conn = self.create()
			self._connections.put(conn)

	def create(self) -> sqlite3.Connection:
		db = os.path.join(os.getcwd(), "external","repository","database","chats.db")

		database_dir = os.path.dirname(db)

		if not os.path.exists(database_dir):
			os.makedirs(database_dir, mode=0o700)

		conn = sqlite3.connect(
			db,
			timeout=5.0,
			check_same_thread=False,
			isolation_level=None
		)

		conn.row_factory = sqlite3.Row

		settings = [
			"PRAGMA journal_mode = WAL",
			"PRAGMA synchronous = NORMAL",
			"PRAGMA busy_timeout = 5000",
		]

		for setting in settings:
			conn.execute(setting)

		os.chmod(database_dir, stat.S_IRWXU)
		os.chmod(db, stat.S_IRUSR | stat.S_IWUSR)

		file_stat = os.stat(db)
		if file_stat.st_mode & 0o077:
			TimeoutError("Error: Database is not secured")

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

			if not self.check_connection(conn):
				conn.close()
				conn = self.create()
			return conn 

		except queue.Empty:
			raise TimeoutError("could not get connection within the given time.")

	def put_connection(self, conn: sqlite3.Connection) -> None:
		try:
			if conn is not None:
				conn.rollback()
				self._connections.put_nowait(conn)

		except queue.Full:
			conn.Close()

	@contextmanager
	def acquire_connection(self):
		conn = self.get_connection()

		try:
			yield conn
		finally:
			self.put_connection(conn)

	def close_connections(self) -> None:

		while not self._connections.empty():
			try:
				conn = self._connections.get_nowait()
				conn.close()

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
	db = os.path.join(os.getcwd(), "external","repository","database","chats.db")

	database_dir = os.path.dirname(db)

	if not os.path.exists(database_dir):
		os.makedirs(database_dir, mode=0o700)

	conn = sqlite3.connect(
		db,
		timeout=5.0,
		check_same_thread=False,
		isolation_level=None
		)

	conn.row_factory = sqlite3.Row

	settings = [
			"PRAGMA journal_mode = WAL",
			"PRAGMA synchronous = NORMAL",
			"PRAGMA busy_timeout = 5000",
	]

	for setting in settings:
		conn.execute(setting)

	os.chmod(database_dir, stat.S_IRWXU)
	os.chmod(db, stat.S_IRUSR | stat.S_IWUSR)

	file_stat = os.stat(db)
	if file_stat.st_mode & 0o077:
		Error("Error: Database is not secured")

	return conn