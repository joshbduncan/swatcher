import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env.example"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # flask session setup
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "examples/flask_app/flask_session"
    PERMANENT_SESSION_LIFETIME = 1800
    # flask debig toolbar setup
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # set max upload size to 5MB
    AMAX_CONTENT_LENGTH = (5 * 1024) * 1024
