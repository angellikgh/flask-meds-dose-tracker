from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_ENV'))

Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from tracker import views, models
