# wsgi.py
import os
from apps.app import create_app

# 環境名はあなたの config に合わせて。例: 'production' / 'development'
CONFIG_NAME = os.environ.get("FLASK_CONFIG", "development")
app = create_app(CONFIG_NAME)
