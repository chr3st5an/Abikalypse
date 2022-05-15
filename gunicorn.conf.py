"""General config file for gunicorn
"""

import os


bind    = "0.0.0.0:8080"
workers = (os.cpu_count() * 2) + 1
