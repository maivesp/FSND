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

        token_executive_producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxVQVNnbGZ1dUVyQW1iQm4zc1VxciJ9.eyJpc3MiOiJodHRwczovL2Rldi1xaXd3ZHpsay51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTY5OTQwNzAzMTE2NDc5MDgwMzMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY2NzM2MjYxNiwiZXhwIjoxNjY3NDQ5MDE2LCJhenAiOiI2VVg2UlNhQXAxWVBmWUFmc25oZjlJaXZsZkRiM1JvQyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllX2Nhc3QiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.uYZyW0JgdwfJIG816PK6ByrdauLF6N8Hje5-WAumMtpLJ79Y28cTodQ8QjjuQ-rOXmhkwiAaFL9YEWo40vvVLUb3iL3oOVtOVSHjDpSmKXBpc1unjKMS6cdetK5tElo0Ia4EgzV4iZSHbWOw0V8NowPVWb4Zn1-1Ef2iIvl9Hh4Sg_yfhzFBLjSBImVyO7wxA5UNAqCqrjVhJ95Z9pffgvH1pOpAsmqwhUyxISNm5yxox0KaryKXnylmHwB-RukBNhZDTH_HEDQoC_1NUirhxsIGE7KqCJS7X8lMKiMQNpnzA0NY6JYHSoVUx6G1Nbm7JyhgR9A2Ie6qQcvnfbLcMA"
        self.header = { 'Authorization': 'Bearer {}'.format(token_executive_producer)}

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
     
    def testB_update_actor_notfound(self):
        res = self.client().patch("/actor/1000",headers=self.header, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def testC_create_new_actor(self):
        res = self.client().post("/actor",headers=self.header,json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)      
        self.assertTrue(data["actor"]) 

    def testD_update_actor(self):
        res = self.client().patch('/actor/{}'.format(self.id1),headers=self.header, json=self.update_actor)
        data = json.loads(res.data)
 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def testE_get_actors(self):
        res=self.client().get("/actor",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def testF_delete_actor(self):
        res=self.client().delete('/actor/{}'.format(self.id1),headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['deleted_actor'])

    def testG_delete_actor_notfound(self):
        res=self.client().delete('/actor/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")    

    def testH_get_movies_empty(self):
        res=self.client().get("/movie",headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def testI_update_movie_notfound(self):
        res = self.client().patch("/movie/1000",headers=self.header, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")

    def testJ_create_new_movie(self):
        res = self.client().post("/movie",headers=self.header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def testK_update_movie(self):
        res = self.client().patch("/movie/{}".format(self.id2),headers=self.header, json=self.update_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])


    def testL_get_movies(self):
        res=self.client().get("/movie",headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def testM_delete_movie(self):
        res=self.client().delete("/movie/{}".format(self.id2),headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['deleted_movie'])

    def testN_delete_movie_notfound(self):
        res=self.client().delete('/movie/1000',headers=self.header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource not found")
    
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

    def testS_create_moviecast_unauthorized(self):
        res = self.client().post("/moviecast",headers=self.header, json=self.new_moviecast)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertEqual(data['code'],"unauthorized")
        self.assertEqual(data['description'],"Permission not found")


# Make the tests conveniently"currentCategory" executable
if __name__ == "__main__":
    unittest.main()
