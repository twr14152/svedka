#adding sqlalchemy support
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'mysupersecretkey'

#
app.config['SQLACHEMY_DATABASE_URL'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
#toolbar = DebugToolbarExtension(app)


class userInfo(db.Model):
    __tablename__ = 'userData'
    id = db.Column(db.Integer, primary_key = True, next = True)
