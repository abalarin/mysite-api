from myapi.app import app
from .main import main

app.register_blueprint(main)
