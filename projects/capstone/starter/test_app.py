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

        token_casting_director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVQVNnbGZ1dUVyQW1iQm4zc1VxciJ9.eyJpc3MiOiJodHRwczovL2Rldi1xaXd3ZHpsay51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTY5OTQwNzAzMTE2NDc5MDgwMzMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY2NjUzNzIyMCwiZXhwIjoxNjY2NjIzNjIwLCJhenAiOiI2VVg2UlNhQXAxWVBmWUFmc25oZjlJaXZsZkRiM1JvQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllX2Nhc3QiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicHV0OmFjdG9yIiwicHV0Om1vdmllIl19.hK_VqtnFHhxj_VMTd_IDZVERQ-T6rfQwDCCb_qrnApZy7OhgrJKHq221RR_KE7qooPF9iL_9H1SRq-0allTPjr15gfeSbD22__KYZlAoB9Q3bVcRijoLi3wtvbOM7q3ULHURtSXDW-_K4OkoATAvLc-Tg7eKnhaQtYCHTXP-evmtQpVVQMOmP6n_jg-hHEBY-RC1mDKqCF_QKuwVn9BfNjfdJI1cgUmal7vWp4f_AQgRiwFcGiKu0rEcIp8LhVwFs_vN1V4zvBldIznvVNtTbeazegaZPgb8UFieFozw2696Rsxkl2OEyaqYC-X318kCNr_YUo0ySdvkfS5AYTknLQ"
        token_casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVQVNnbGZ1dUVyQW1iQm4zc1VxciJ9.eyJpc3MiOiJodHRwczovL2Rldi1xaXd3ZHpsay51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI0MzM1NjkzOTQwMjcwNTIxNDQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY2NjUzNTI4MCwiZXhwIjoxNjY2NjIxNjgwLCJhenAiOiI2VVg2UlNhQXAxWVBmWUFmc25oZjlJaXZsZkRiM1JvQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllX2Nhc3QiXX0.mmx60qxHUazncaTMWMsnlHSxGfhsO8QO6adk89xoB87hGQVpE1o6t4qia7VcfLMH9EGLsZcSXQVqcFreRUYEnY-eCnTIzPntxXjBrFNgOS6d4cHla8cU7-6zgTRKOJcSzKEXNUQhyjBnHfAsU0FoV_TcJqPGWiHRkpOXGZ85aRozY-ZtrpXief3WTFxnBzfc4hTpy0GfAzpv9h5D-dM3hevYxctFFnqbIQXAMDzW2S6rzpfY0WmevfTqJ4FCJBIP_KSgNj68J5E87AttQ2yDjsgTpia-yj0pb6ayIn2ORhQq9LT3AQp4WG3rnHtOFMEMpr518DaBYuZly_jse3CT8g"
        
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
            self.id1=''
        else:
            result
            self.id1=result[0]
        print(self._testMethodName +" actor "+ str(self.id1))

        cursor.execute('SELECT * from movie;')
        result = cursor.fetchone()
        if result is None:
            self.id2=''
        else:
            result
            self.id2=result[0]
        print(self._testMethodName +" movie "+ str(self.id2))

    def tearDown(self):
        print(self._testMethodName +" Ended")

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test1_get_actors_empty(self):
        print("id== "+ str(self.id))
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")
     
    def test2_update_actor_fails(self):
        res = self.client().patch("/actor/1000",headers=self.header, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def test3_create_new_actor(self):
        res = self.client().post("/actor",headers=self.header,json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)       

    def test4_update_actor(self):
        res = self.client().patch('/actor/{}'.format(self.id1),headers=self.header, json=self.update_actor)
        data = json.loads(res.data)
 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])


    def test5_get_actors(self):
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test6_delete_actor(self):
        res=self.client().delete('/actor/{}'.format(self.id1),headers=self.header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['delete'])

    def test7_delete_actor_notfound(self):
        res=self.client().delete('/actor/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")    

    def test8_get_movies_empty(self):
        res=self.client().get("/movie",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def test9_update_movie_fails(self):
        res = self.client().patch("/movie/1000",headers=self.header, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def test10_create_new_movie(self):
        res = self.client().post("/movie",headers=self.header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test11_update_movie(self):
        res = self.client().patch("/movie/{}".format(self.id2),headers=self.header, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])


    def test12_get_movies(self):
        res=self.client().get("/movie",headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def test13_delete_movie(self):
        res=self.client().delete("/movie/{}".format(self.id2),headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['delete'])

    def test14_delete_movie_notfound(self):
        res=self.client().delete('/movie/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

# Make the tests conveniently"currentCategory" executable
if __name__ == "__main__":
    conn = psycopg2.connect('dbname=moviedb_tst')
    cursor = conn.cursor()
    cursor.execute('delete from actor;')
    cursor.execute('delete from movie;')
    conn.commit()
    unittest.main()

