from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '24446f27d7e8540adcaf914f0aea6bd7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fish.db'
db = SQLAlchemy(app)

from fishshop import routes # must be after app instantiation