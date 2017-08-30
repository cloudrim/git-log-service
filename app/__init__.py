from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

from app import views, models, config
