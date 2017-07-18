import os
from flask import Flask
#from sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir,ADMINS,MAIL_SERVER,MAIL_PORT,MAIL_USERNAME,MAIL_PASSWORD
from flask_mail import Mail
from .momentjs import momentjs
from flask_babel import Babel
from flask_bootstrap import Bootstrap








app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mail = Mail(app)

app.jinja_env.globals['momentjs'] = momentjs
babel = Babel(app)




from app import views,models
