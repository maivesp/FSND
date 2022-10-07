

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

app = create_app()
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)

    def __repr__(self):
        return f'''<Movie { self.id} { self.title} { self.release_date} >'''



class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    def __repr__(self):
        return f'''<Actor { self.id } { self.name } { self.age } { self.gender }>'''

class Movie_cast(db.Model):
    __tablename__ = 'movie_cast'
    id = db.Column(db.Integer,primary_key=True)
    movie_id = db.Column(db.String)
    actor_id = db.Column(db.Integer)
    movie_actor = db.relationship('Actor',backref='actors',lazy=True)
    actor_movie = db.relationship('Movie',backref='movies',lazy=True)
   

