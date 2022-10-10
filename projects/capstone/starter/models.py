
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db= SQLAlchemy()
# Test db setup
#database_filename = "database.db"
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
# End of test db setup

def setup_db(app):

  app.config.from_object('config')
  #app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app=app
  db.init_app(app) 

  migrate = Migrate(app, db)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    actors_in_movie = db.relationship('Movie_cast',backref='actors_in_movie',lazy=True)

    def __repr__(self):
        return f'''<Movie { self.id} { self.title} { self.release_date} >'''

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
 

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date   
 
            }


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    movies_acted_by = db.relationship('Movie_cast',backref='movies_acted_by',lazy=True)

    def __repr__(self):
        return f'''<Actor { self.id } { self.name } { self.age } { self.gender }>'''

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
 

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }

class Movie_cast(db.Model):
    __tablename__ = 'movie_cast'
    id = db.Column(db.Integer,primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    actor_id = db.Column(db.Integer,db.ForeignKey('actor.id'))

    def __repr__(self):
        return f'''<Actor { self.id } { self.movie_id } { self.actor_id } >'''

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id
 

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            }