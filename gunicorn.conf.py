"""General config file for gunicorn
"""

accesslog    = "access.log"
bind         = "0.0.0.0:8080"
preload      = True
wsgi_app     = "Abikalypse:app"
workers      = 3
worker_class = "aiohttp.GunicornWebWorker"
