from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
import pandas


app = Flask(__name__)
app.config.from_object(config.Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
pd = pandas


from rest import routes
