import os
import multiprocessing
import sys

port = os.environ.get("PORT", "8080")
bind = [f"localhost:{port}"]

workers = multiprocessing.cpu_count()

if sys.platform == "win32":
	worker_class = "asyncio"
else:
	worker_class = "uvloop"
	
keep_alive_timeout = 5.0