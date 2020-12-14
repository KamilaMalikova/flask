from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from provider.database_provider import DatabaseProvider

app = Flask(__name__)
app.config['SECRET_KEY'] = '5327276e6ca815ae038cf07a38f68975'
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseProvider('/home/kamila/Documents/auction_area_2').get_database_configuration(section='sqlite')
db = SQLAlchemy(app)