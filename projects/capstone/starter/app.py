from hashlib import new
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import sys


from models import setup_db,db_drop_and_create_all, Movie, Actor, Movie_cast
from flask_cors import CORS
from auth import AuthError, requires_auth





def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization,true")
        response.headers.add("Access-Control-Allow-methods", "GET, POST, PATCH, DELETE")
        return response

    @app.route('/')
    def hello_world():
        return 'Hello World'

    @app.route('/actor',methods=['GET'])
    @requires_auth(permission='get:actor')
    def get_actor(payload):
        try:
            actors = Actor.query.all()
        except Exception as error:
            print(str(error))
            abort(404)

        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success" : True,
            "actors" : formatted_actors
            })

    @app.route('/movie',methods=['GET'])
    @requires_auth(permission='get:movie')
    def get_movie(payload):
        try:
            movies = Movie.query.all()
      #      print(movies, file=sys.stderr,flush=True)
        except Exception as error:
            print(str(error))
            abort(404)

        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success" : True,
            "movies" : formatted_movies
            })


    @app.route('/actor',methods=['POST'])
    @requires_auth(permission='put:actor')
    def create_actor(payload):
        body=request.get_json()

        new_name=body.get("name")
        new_age=body.get("age")
        new_gender=body.get("gender")
        actor=Actor(name=new_name,age=new_age,gender=new_gender)
    
        try:
            actor.insert()
        except Exception as error:
            print(str(error.orig) + " for parameters" + str(error.params))
            abort(422)
    
        return jsonify({
            "success": True
        })

    @app.route('/movie',methods=['POST'])
    @requires_auth(permission='put:movie')

    def create_movie(payload):
        body=request.get_json()
    
        new_title=body.get("title")
        print(new_title)
        new_release_date=body.get("release_date")
    
        movie=Movie(title=new_title,release_date=new_release_date)
    
        try:
            movie.insert()
        except Exception as error:
            print(str(error.orig) + " for parameters" + str(error.params))
            abort(422)
    
        return jsonify({
            "success": True
        })

    @app.route('/actor/<int:id>',methods=['PATCH'])
    @requires_auth(permission='patch:actor')
    def update_actor(payload,id):

        try:
            actor=Actor.query.filter(Actor.id==id).one_or_none()

        except Exception as error:
            print(str(error))
            abort(422)

        if actor is None:
            abort(404)
        else:
            body=request.get_json()

            actor.name = body.get("name")
            actor.age = body.get("age")
            actor.gender = body.get("gender")

            try:
                actor.update()

            except Exception as error:
                print(str(error.orig) + "for parameters" + str(error.params))
                abort(422)

        return jsonify({
            "success" : True,
            "actor" : [actor.format()]
            })

    @app.route('/movie/<int:id>',methods=['PATCH'])
    @requires_auth(permission='patch:movie')

    def update_movie(payload,id):

        try:
            movie=Movie.query.filter(Movie.id==id).one_or_none()

        except Exception as error:
            print(str(error))
            abort(422)

        if movie is None:
            abort(404)
        else:
            body=request.get_json()

            movie.title = body.get("title")
            movie.release_date = body.get("release_date")

            try:
                movie.update()

            except Exception as error:
                print(str(error.orig) + "for parameters" + str(error.params))
                abort(422)

        return jsonify({
            "success" : True,
            "movie" : [movie.format()]
            })

    @app.route('/actor/<int:id>',methods=['DELETE'])
    @requires_auth(permission='delete:actor')

    def delete_actor(payload,id):
        try:
            actor=Actor.query.filter(Actor.id==id).one_or_none()

        except Exception as error:
            print(str(error))
            abort(422)

        if actor is None:
            abort(404)
        else:
            try:
                actor.delete()
            except Exception as error:
                print(str(error))
                abort(422)

        return jsonify({
            "success":True,
            "delete":id
            })

    @app.route('/movie/<int:id>',methods=['DELETE'])
    @requires_auth(permission='delete:movie')

    def delete_movie(payload,id):
        try:
            movie=Movie.query.filter(Movie.id==id).one_or_none()

        except Exception as error:
            print(str(error))
            abort(422)

        if movie is None:
            abort(404)
        else:
            try:
                movie.delete()
            except Exception as error:
                print(str(error))
                abort(422)

        return jsonify({
            "success":True,
            "delete":id
            })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 422

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Not Authorized"
        }), 401

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
    
    return app

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8080, debug=True)