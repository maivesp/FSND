API Reference
Getting Started
Base URL: 
	This app and its backend postgres database are hosted in heroku cloud hosting service. The backend app is hosted at the default, https://maivesp.herokuapp.com
Authentication: This application endpoints are secured using JWT usage using auth0 integration. 

URL where the application is hosted:
------------------------------------
	https://maivesp.herokuapp.com	

Instructions to set up authentication:
---------------------------------------
	One Postman script file has been included for each of the 3 roles. Bearer JWT has been copied in the authorization tab of the parent postman and individual test "has been set to inherit auth from parent postman"
	01_Executive Producer.postman_collection.json
	Casting_Assistant.postman_collection (1).json
	Casting_director.postman_collection.json

For the unittests. one separate python file has been created for each role and the JWT has been hardcoded in the python file itself.

	test_app-castingassistant.py
	test_app-castingdirector.py
	test_app-executiveproducer.py
	
Unittest scripts has been created as per the permission allowed for each role. Following are the permissions allowed for each role and corresponding the unittest created.

casting assistant:	
------------------

"permissions": [
    "get:actor",
    "get:movie",
    "get:movie_cast"
  ]

testE_get_actors
testH_get_movies_empty
testL_get_movies
testO_get_moviecast
testP_get_moviecast_empty
testR_create_moviecast_unauthorized
testT_create_movie_unauthorized
testU_create_actor_unauthorized
testV_update_movie_unauthorized
testW_delete_movie_unauthorized
testW_update_actor_unauthorized
testX_delete_actor_unauthorized

casting_director:
-----------------

  "permissions": [
    "delete:actor",
    "get:actor",
    "get:movie",
    "get:movie_cast",
    "patch:actor",
    "patch:movie",
    "put:actor",
    "put:moviecast"
  ]

testA_get_actors_empty
testB_update_actor_notfound
testC_create_new_actor
testD_update_actor
testE_get_actors
testF_delete_actor
testG_delete_actor_notfound
testH_get_movies_empty
testI_update_movie_notfound
testK_update_movie
testL_get_movies
testO_get_moviecast
testP_get_moviecast_empty
testQ_create_moviecast
testT_create_movie_unauthorized
testW_delete_movie_unauthorized

executive_PRODUCER:
-------------------

  "permissions": [
    "delete:actor",
    "delete:movie",
    "get:actor",
    "get:movie",
    "get:movie_cast",
    "patch:actor",
    "patch:movie",
    "put:actor",
    "put:movie"
  ]

testA_get_actors_empty
testB_update_actor_notfound
testC_create_new_actor
testD_update_actor
testE_get_actors
testF_delete_actor
testG_delete_actor_notfound
testH_get_movies_empty
testI_update_movie_h
testJ_create_new_movie
testK_update_movie
testL_get_movies
testM_delete_movie
testN_delete_movie_notfound
testO_get_moviecast
testP_get_moviecast_empty
testS_create_moviecast_unauthorized


Error Handling
--------------
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return 2 error types when requests fail:

404: Resource Not Found
422: Not Processable
403: Not Authorized


Roles and permissions allowed:
------------------------------

Casting Assistant:
-----------------
"permissions": [
    "get:actor",
    "get:movie",
    "get:movie_cast"
  ]
Casting director:
-----------------
  "permissions": [
    "delete:actor",
    "get:actor",
    "get:movie",
    "get:movie_cast",	
    "patch:actor",
    "patch:movie",
    "post:actor",
    "post:moviecast"
  ]

Executive Producer:
-------------------
  "permissions": [
    "delete:actor",
    "delete:movie",
    "get:actor",
    "get:movie",
    "get:movie_cast",
    "patch:actor",
    "patch:movie",
    "post:actor",
    "post:movie"
  ]

Endpoints
---------
GET/actor
---------
General:
Returns a list of all actors

Sample: curl -X GET https://maivesp.herokuapp.com/actor

{
    "actors": [
        {
            "age": 76,
            "gender": "Male",
            "id": 1,
            "name": "Al PAcino"
        },
        {
            "age": 74,
            "gender": "Male",
            "id": 2,
            "name": "Robert De Niro"
        },
        {
            "age": 70,
            "gender": "Female",
            "id": 3,
            "name": "Merly Streep"
        },
    ],
    "success": true
}
GET/movie
---------
Returns a list of movies

Sample: curl -X GET https://maivesp.herokuapp.com/movie


Response Body:
--------------

{
    "count": 3,
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 23 Feb 1979 00:00:00 GMT",
            "title": "Taxi Driver"
        },
        {
            "id": 2,
            "release_date": "Fri, 27 Sep 2019 00:00:00 GMT",
            "title": "The Irishman"
        },
        {
            "id": 3,
            "release_date": "Mon, 10 Oct 2022 00:00:00 GMT",
            "title": "The Deer Hunter"
        }
    ],
    "success": true
}

GET /movie/<int:id>/cast
-------------------------

General:
Returns a list of cast for the id of the movie that is passed, along with the success value and the movie title.

curl -X GET https://maivesp.herokuapp.com/movie/2/cast


Response Body:
--------------
{
    "casts": [
        {
            "Age": 74,
            "Name": "Robert De Niro",
            "id": 2
        },
        {
            "Age": 70,
            "Name": "Merly Streep",
            "id": 3
        }
    ],
    "movietitle": "The Deer Hunter",
    "success": true
}


DELTE /actor/<int:id>
--------------------------
Delete the actor the ID of which is passed. Returns the name of the deleted actor and success value.

curl -X DELETE https://maivesp.herokuapp.com/actor/2

{
    "deleted_actor": "Al PAcino",
    "success": true
}

DELTE /movie/<int:id>
--------------------------
Delete the movie the Id of which is passed. Returns the name of the deleted movie and success value.

curl -X DELETE https://maivesp.herokuapp.com/movie/2

{
    "deleted_movie": "The Deer Hunter",
    "success": true
}



POST /actor
---------------
General:
Creates an Actor record with the age, gender and name passed in the body of the request.

curl "https://maivesp.herokuapp.com/actor" -X POST -H "Content-Type: application/json" --data "{\"age\": 42,\"gender\": \"male\",\"name\": \"Rober De Niro\"}"

Request Body:
-------------
{
    "age": 76,
    "gender": "Male",
    "name": "Al PAcino"
}

Response Body:
--------------
{
    "actor:": {
        "age": 76,
        "gender": "Male",
        "id": 4,
        "name": "Al PAcino"
    },
    "success": true
}

PATCH /actor/<int:id>
---------------
General:
Updates the Actor belonging to the ID that is passed, record with the age, gender and name passed in the body of the request.

curl "https://maivesp.herokuapp.com/actor/1" -X POST -H "Content-Type: application/json" --data "{\"age\": 42,\"gender\": \"male\",\"name\": \"Rober De Niro\"}"

Request Body:
-------------
{
    "age": 76,
    "gender": "Male",
    "name": "Al PAcino"
}

Response Body:
--------------
{
    "actor:": {
        "age": 76,
        "gender": "Male",
        "id": 4,
        "name": "Al PAcino"
    },
    "success": true
}

PATCH /movie
---------------
General:
Updates the movie belonging to the ID that is passed, record with the age, gender and name passed in the body of the request.

curl "https://maivesp.herokuapp.com/movie/3" -X PATCH -H "Content-Type: application/json" --data "{\"release_date\": \"Mon, 10 Oct 2022 00:00:00 GMT\",\"title\": \"The Deer Hunter"\}"

Request Body:
-------------
        {
            "id": 3,
            "release_date": "Mon, 10 Oct 2022 00:00:00 GMT",
            "title": "The Deer Hunter"
        }

Response Body:
--------------
{
    "movie": {
        "id": 3,
        "release_date": "Mon, 10 Oct 2022 00:00:00 GMT",
        "title": "The Deer Hunter"
    },
    "success": true
}


POST /moviecast
---------------
General:
Creates a record for a cast of the movie with the acor_id and movie_id passed in the body of the request.

curl "https://maivesp.herokuapp.com/moviecast" -X POST -H "Content-Type: application/json" --data "{\"movie_id\": 2,\"actor_id\": 4}"

Request Body:
-------------
{
    "movie_id": 2,
    "actor_id": 4
}


Response Body:
--------------
{
    "actor": "Al PAcino",
    "movie": "The Irishman",
    "success": true
}





