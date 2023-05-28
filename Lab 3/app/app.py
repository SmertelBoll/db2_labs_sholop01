from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sholop01_lab2:21132113@localhost/sholop01_lab2_DB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/zno_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

__all__ = ['app', 'db']

