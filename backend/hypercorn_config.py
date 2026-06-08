import os
import multiprocessing

port = os.environ.get("PORT", "8080")
bind = [f"0.0.0.0:{port}"]
workers = multiprocessing.cpu_count()
worker_class = "uvloop"
keep_alive_timeout = 5.0