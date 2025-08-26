# wsgi.py
import os
from apps.app import create_app

CONFIG_NAME = os.environ.get("FLASK_CONFIG", "development")
app = create_app(os.environ.get("FLASK_CONFIG", "local"))
