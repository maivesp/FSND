import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "moviedb_tst"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {"age": 46,"gender": "Male","name": "Male Actor 6"}
        self.new_movie = {"title": "Film 1","release_date": "2022-10-10"}
        self.update_actor = {"age": 46,"gender": "Male","name": "Male Actor 6"}
        self.update_movie = {"title": "Film 1","release_date": "2022-10-10"}


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_actors(self):
        res=self.client().get("/actor")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_get_actors_empty(self):
        res=self.client().get("/actor")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_get_movies(self):
        res=self.client().get("/movie")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def test_get_movies_empty(self):
        res=self.client().get("/movie")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_delete_actor(self):
        res=self.client().delete("/actor/1")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['delete'])

    def test_delete_movie(self):
        res=self.client().delete("/movie/1")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['delete'])

    def test_delete_actor_notfound(self):
        res=self.client().delete("/actor/1000")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_delete_movie_notfound(self):
        res=self.client().delete("/movie/1000")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_create_new_actor(self):
        res = self.client().post("/actor", json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_actor_fails(self):
        res = self.client().post("/actor", json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],"unprocessable")

    def test_create_new_movie(self):
        res = self.client().post("/actor", json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_movie_fails(self):
        res = self.client().post("/movie", json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],"unprocessable")
        
    def test_update_actor(self):
        res = self.client().patch("/actor/1", json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["age"])
        self.assertTrue(data["gender"])
        self.assertTrue(data["name"])

    def test_update_actor_fails(self):
        res = self.client().patch("/actor/1", json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_update_movie(self):
        res = self.client().patch("/movie", json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["title"])
        self.assertTrue(data["release_date"])

    def test_update_movie_fails(self):
        res = self.client().patch("/actor", json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

# Make the tests conveniently"currentCategory" executable
if __name__ == "__main__":
    unittest.main()
