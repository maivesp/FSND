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
            self.db.drop_all()
            self.db.create_all()

        token_casting_assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVQVNnbGZ1dUVyQW1iQm4zc1VxciJ9.eyJpc3MiOiJodHRwczovL2Rldi1xaXd3ZHpsay51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI0MzM1NjkzOTQwMjcwNTIxNDQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY2NzM2MjQwMiwiZXhwIjoxNjY3NDQ4ODAyLCJhenAiOiI2VVg2UlNhQXAxWVBmWUFmc25oZjlJaXZsZkRiM1JvQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllX2Nhc3QiXX0.dikB3UnBalpS9FPTStMjiGhkf_bnPDKDaa7spIcpz9lUpIZiNiIVONX0ZtJSjlTMjIMO0UV11FDdkRmg6FKOtXSNfKFg9u7YyZSlc2l8Bhz0Mfag7Z0L1bon16FvvXbwjRPmA8wAEyPB-ByxR-Aou0jKNlsol7UP5CHQx7qQcoTRsPBdANc8nVFwIN9TTJWOi6T4dfiXsqtWl3fvZ9wdqPU8BvhH8YAvPWtxv-0PBLEJobP8dYS9NYnp7Uqr04KiyqxexW9K5OCSzBN0pL6Nd1EnbUD8VnsinU3DGTY2TcHBce4HXnL1RQjnUKzyQpm0voIvRQTILuQwfUUCV8z8iA"
        self.header = { 'Authorization': 'Bearer {}'.format(token_casting_assistant)}

        self.new_actor = {"age": 46,"gender": "Male","name": "Male Test"}
        self.new_movie = {"title": "Test Film","release_date": "2022-10-10"}
        self.update_actor = {"age": 46,"gender": "Male","name": "Male Test Upd"}
        self.update_movie = {"title": "Test Film","release_date": "2022-10-10"}
        self.new_moviecast = {"movie_id": 1,"actor_id": 1}

        conn = psycopg2.connect('dbname=moviedb_tst')
        cursor = conn.cursor()
        cursor.execute('delete from movie_cast;')     
        cursor.execute('delete from movie;')
        cursor.execute('delete from actor;')     
        cursor.execute('delete from movie_cast;')     
        conn.commit()             

        if self._testMethodName == 'testA_get_actors_empty':
            cursor.execute('delete from actor;')
            conn.commit()

        if self._testMethodName == 'testD_update_actor' or self._testMethodName == 'testW_update_actor_unauthorized':
            cursor.execute("insert into actor values(1,'Male Actor 1',41,'Male');")
            conn.commit()
            cursor.execute('SELECT * from movie;')
            result = cursor.fetchone()
            if result is None:
                self.id1='1'
            else:
                result
                self.id1=result[0]

        if self._testMethodName == 'testE_get_actors':      
            cursor.execute("insert into actor values(1,'Male Actor 1',41,'Male');")
            conn.commit()

        if self._testMethodName == 'testF_delete_actor'or self._testMethodName == 'testX_delete_movie_unauthorized':
            cursor.execute("insert into actor values(1,'Male Actor 1',41,'Male');")
            conn.commit()
            cursor.execute('SELECT * from movie;')
            result = cursor.fetchone()
            if result is None:
                self.id1='1'
            else:
                result
                self.id1=result[0]

        if self._testMethodName == 'testH_get_movies_empty':
            cursor.execute('delete from movie;')
            conn.commit()             

        if self._testMethodName == 'testK_update_movie' or self._testMethodName == 'testV_update_movie_unauthorized':         
            cursor.execute("insert into movie values(1,'Film 1','2022-01-01');")
            conn.commit()
            cursor.execute('SELECT * from movie;')
            result = cursor.fetchone()
            if result is None:
                self.id2='1'
            else:
                result
                self.id2=result[0]

        if self._testMethodName == 'testL_get_movies':      
            cursor.execute("insert into movie values(1,'Film 1','2022-01-01');")
            conn.commit()

        if self._testMethodName == 'testM_delete_movie' or self._testMethodName == 'testW_delete_movie_unauthorized':
            cursor.execute("insert into movie values(1,'Film 1','2022-01-01');")
            conn.commit()
            cursor.execute('SELECT * from movie;')
            result = cursor.fetchone()
            if result is None:
                self.id2='1'
            else:
                result
                self.id2=result[0]
        
        if self._testMethodName == 'testO_get_moviecast':    
            cursor.execute("insert into movie values(1,'Film 1','2022-01-01');")    
            cursor.execute("insert into actor values(1,'Male Actor 1',41,'Male');")
            cursor.execute("insert into movie_cast values(1,1,1);")
            conn.commit()

        if self._testMethodName == 'testP_get_moviecast_empty':
            cursor.execute('delete from movie_cast;')          
            conn.commit()

        if self._testMethodName == 'testQ_create_moviecast':
            cursor.execute("insert into movie values(1,'Film 1','2022-01-01');")    
            cursor.execute("insert into actor values(1,'Male Actor 1',41,'Male');")      
            conn.commit()

    def tearDown(self):
        # print(self._testMethodName)
        pass


    def testA_get_actors_empty(self):
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")


    def testE_get_actors(self):
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors']) 

    def testH_get_movies_empty(self):
        res=self.client().get("/movie",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def testL_get_movies(self):
        res=self.client().get("/movie",headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    
    def testO_get_moviecast(self):
        res=self.client().get('/movie/1/cast',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movietitle'])
        self.assertTrue(data['casts'])

    def testP_get_moviecast_empty(self):
        res=self.client().get('/movie/1/cast',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def testR_create_moviecast_unauthorized(self):
        res = self.client().post("/moviecast",headers=self.header, json=self.new_moviecast)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")

    def testT_create_movie_unauthorized(self):
        res = self.client().post("/movie",headers=self.header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")
        
    def testU_create_actor_unauthorized(self):
        res = self.client().post("/movie",headers=self.header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")
    
    def testV_update_movie_unauthorized(self):
        res = self.client().patch("/movie/{}".format(self.id2),headers=self.header, json=self.update_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")

    def testW_update_actor_unauthorized(self):
        res = self.client().patch("/movie/{}".format(self.id1),headers=self.header, json=self.update_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")

    def testW_delete_movie_unauthorized(self):
        res=self.client().delete('/movie/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")

    def testX_delete_actor_unauthorized(self):
        res=self.client().delete('/actor/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")

# Make the tests conveniently"currentCategory" executable
if __name__ == "__main__":
    unittest.main()

