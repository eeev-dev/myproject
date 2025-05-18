# gunicorn_config.py

bind = "0.0.0.0:8080"
workers = 4
threads = 2
worker_class = "gthread"
graceful_timeout = 30
timeout = 60
accesslog = "-"
errorlog = "-"
