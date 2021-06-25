from .config import Config
from flask import Flask
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config.from_object(Config)
Session(app)
toolbar = DebugToolbarExtension(app)

from . import routes
