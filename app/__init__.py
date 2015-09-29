from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask_login import LoginManager
from flask_ldap3_login import LDAP3LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.admin import Admin


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()              # Setup a Flask-Login Manager
ldap_manager = LDAP3LoginManager(app)          # Setup a LDAP3 Login Manager
bootstrap = Bootstrap(app)                     # Setup frontend Framework engine
manager = Manager(app)
db = SQLAlchemy(app)
# admin = Admin(app)
login_manager.init_app(app)

from app import views, admin_page, ldap