import os
import unittest
from unittest.mock import Mock
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import psycopg2

from app import create_app
from auth import requires_auth
from models import setup_db, Movie, Actor,db_drop_and_create_all


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "moviedb_tst"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format("postgres","postgres","localhost:5432",self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        token_casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVQVNnbGZ1dUVyQW1iQm4zc1VxciJ9.eyJpc3MiOiJodHRwczovL2Rldi1xaXd3ZHpsay51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTY5OTQwNzAzMTE2NDc5MDgwMzMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY2NjQ0NzM1MywiZXhwIjoxNjY2NTMzNzUzLCJhenAiOiI2VVg2UlNhQXAxWVBmWUFmc25oZjlJaXZsZkRiM1JvQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllX2Nhc3QiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicHV0OmFjdG9yIiwicHV0Om1vdmllIl19.QO_XRpsCdVl-8kZkPenbqUzJOX5gNCX8lFoBUeeixwuUqe4DVr9a8YSU6lMjZSvn1mBMuEdZaMxNsobU7q3eHxervMBnJKG4mfKoq84Ikkch2nb2b-I4WVtgv1UH1Du_ymRU34KYXkjdaETsi8-hPr5i8RZ1gZTM30We6Vf-W_Jr3QkCyuGXfDlIviVY5ONxogO9FsTIkxwARzm9Y7XPg1NXIuZAyd6co-zqp8TT3xxxPpnrQ8YXakQXUHxrYFExHW0AtrhNlU3njltGLnUpdQFZDQpUEBg3S9vU3YcewwhiReOJtP-YE-Z8iRNHo-BMpkJS9F5rMMwe0Z7MOguMPA"
        self.header = { 'Authorization': 'Bearer {}'.format(token_casting_director)}

        self.new_actor = {"age": 46,"gender": "Male","name": "Male Test"}
        self.new_movie = {"title": "Test Film","release_date": "2022-10-10"}
        self.update_actor = {"age": 46,"gender": "Male","name": "Male Test Upd"}
        self.update_movie = {"title": "Test Film","release_date": "2022-10-10"}

        conn = psycopg2.connect('dbname=moviedb_tst')
        cursor = conn.cursor()
        cursor.execute('SELECT * from actor;')
        result = cursor.fetchone()
        if result is None:
            self.id=''
        else:
            self.id=result[0]

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_actors_empty(self):
        print("id== "+ str(self.id))
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")
     
    def test_update_actor_fails(self):
        res = self.client().patch("/actor/1000",headers=self.header, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def test_create_new_actor(self):
        res = self.client().post("/actor",headers=self.header,json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)       

    def test_update_actor(self):
        print("id= "+ self.id)
        res = self.client().patch('/actor/{}'.format(self.id),headers=self.header, json=self.update_actor)
        data = json.loads(res.data)
 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])


    def test_get_actors(self):
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_delete_actor(self):
        res=self.client().delete('/actor/{}'.format(self.id),headers=self.header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['delete'])

    def test_delete_actor_notfound(self):
        res=self.client().delete('/actor/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")    

    #def test_get_movies_empty(self):
    #    res=self.client().get("/movie",headers=self.header)
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code,404)
    #    self.assertEqual(data['success'],False)
    #    self.assertEqual(data['error'],404)
    #    self.assertEqual(data['message'],"Resource not found")

    #def test_update_movie_fails(self):
    #    res = self.client().patch("/movie/1000",headers=self.header, json=self.update_movie)
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code,404)
    #    self.assertEqual(data['success'],False)
    #    self.assertEqual(data['error'],404)
    #    self.assertEqual(data['message'],"Resource not found")

    #def test_create_new_movie(self):
    #    res = self.client().post("/movie",headers=self.header, json=self.new_movie)
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 200)
    #    self.assertEqual(data["success"], True)

    #def test_update_movie(self):
    #    res = self.client().patch("/movie/1",headers=self.header, json=self.update_movie)
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 200)
    #    self.assertEqual(data["success"], True)
    #    self.assertTrue(data["title"])
    #    self.assertTrue(data["release_date"])

    #def test_get_movies(self):
    #    res=self.client().get("/movie",headers=self.header)
    #    data=json.loads(res.data)

    #    self.assertEqual(res.status_code,200)
    #    self.assertEqual(data['success'],True)
    #    self.assertTrue(data['movies'])

    #def test_delete_movie(self):
    #    res=self.client().delete("/movie/1",headers=self.header)
    #    data=json.loads(res.data)

    #    self.assertEqual(res.status_code,200)
    #    self.assertEqual(data['success'],True)
    #    self.assertTrue(data['delete'])

    #def test_delete_movie_notfound(self):
    #    res=self.client().delete('/movie/1000',headers=self.header)
    #    data=json.loads(res.data)

    #    self.assertEqual(res.status_code,404)
    #    self.assertEqual(data['success'],False)
    #    self.assertEqual(data['error'],404)
    #    self.assertEqual(data['message'],"Resource not found")

# Make the tests conveniently"currentCategory" executable
if __name__ == "__main__":
    conn = psycopg2.connect('dbname=moviedb_tst')
    cursor = conn.cursor()
    cursor.execute('delete from actor;')
    conn.commit()
    unittest.main()

