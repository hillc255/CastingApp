# Standard library imports
import os
import unittest
import json

# Third party imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc

# Local application imports
import app
import settings
from backend.src.database.models import setup_db, Movie, Actor, db


print(f"**** test_app.py ****")
print(" ")


class CastingAppTestCase(unittest.TestCase):
    """This class represents the CastingApp test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app()
        self.client = self.app.test_client
        self.database_name = "castapp_test"
        self.database_path = settings.LOCAL_DATABASE_PATH
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # '''
    # TEST HOME AND CORS APIs
    #
    # '''

    def test_given_home_page_behavior(self):
        print("*** Test '/' GET success ***")
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))
        self.assertEqual('Home page', json_res['message'])

    def test_404_home_page_not_found(self):
        print("*** Test '/home' GET error ***")
        res = self.client().get('/home')
        self.assertEqual(res.status_code, 404)
        json_res = json.loads(res.get_data(as_text=False))
        self.assertEqual('Resource Not Found', json_res['message'])

    def test_given_cors_behavior(self):
        print("*** Test '/test_cors' GET success ***")
        res = self.client().get('/test_cors')
        self.assertEqual(res.status_code, 200)

    def test_404_home_page_not_found(self):
        print("*** Test '/test_cors' GET error ***")
        res = self.client().get('/test_cor')
        self.assertEqual(res.status_code, 404)

    # '''
    # TEST MOVIE APIs
    #
    # '''

    def test_get_all_movies(self):
        print("*** Test '/movies' GET success ***")
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_get_no_movies(self):
        print("*** Test '/movies' GET error ***")
        # simulate a bad get with removing "s" from movie
        res = self.client().get('/movie')
        self.assertEqual(res.status_code, 404)

    def test_get_movies_equals_two(self):
        print("*** Test '/movies/<ind:id>' GET success ***")
        res = self.client().get('/movies/2')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_get_movies_not_equals_ten_thousand(self):
        print("*** Test '/movies/<ind:id>' GET error ***")
        res = self.client().get('/movies/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_movies(self):
        print("*** Test '/movies' POST success ***")
        data = {
            'id': None,
            'title': 'Test Robot Movie',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().post('/movies', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_post_no_movies(self):
        print("*** Test '/movies' POST error ***")
        data = {
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().post('/movie', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_patch_movies(self):
        print("*** Test '/movies/<int:id>' PATCH success ***")
        data = {
            'title': 'Test Robot Movie2',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().patch('/movies/2', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_patch_no_movies(self):
        print("*** Test '/movies' PATCH error ***")
        data = {
            'title': 'Test Robot Movie2',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        # set movie to invalid id of zero
        res = self.client().patch('/movies/0', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_movies_publish_patch(self):
        print("*** Test '/movies/<int:id>' Publish PATCH success ***")
        # publish movie
        res1 = self.client().patch('/movies/2/publish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertIn("success", data1, "success key present in body")
        self.assertTrue("success" in data1, "success is True")
        self.assertTrue(data1["success"], "value of success key in body")

        # verify movie is published
        res2 = self.client().get('/movies/2')
        data2 = json.loads(res2.data)
        movie = data2["movie"]
        self.assertTrue(movie['movie_publish'], "movie is published")

    def test_movies_unpublish_patch(self):
        print("*** Test '/movies/<int:id>' Unpublish PATCH success ***")
        # unpublish movie
        res1 = self.client().patch('/movies/2/unpublish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data2 = json.loads(res1.data)
        self.assertIn("success", data2, "success key present in body")
        self.assertTrue("success" in data2, "success is True")
        self.assertTrue(data2["success"], "value of success key in body")

        # verify movie is unpublished
        res2 = self.client().get('/movies/2')
        data3 = json.loads(res2.data)
        movie = data3["movie"]
        self.assertFalse(movie['movie_publish'], "movie is not published")

    def test_movies_toggle_publish_patch(self):
        print("*** Test '/movies/<int:id>' Toggle Publish PATCH success ***")
        res1 = self.client().get('/movies/2')
        data1 = json.loads(res1.data)

        if (data1["movie"]["movie_publish"]):
            self.test_movies_unpublish_patch()
            self.test_movies_publish_patch()
        else:
            self.test_movies_publish_patch()
            self.test_movies_unpublish_patch()

    def test_delete_movie(self):
        print("*** Test '/movies/<int:id>' DELETE success***")
        # insert movie to delete
        self.test_post_movies()

        # get id from object of inserted question to be deleted
        selected = Movie.query.order_by(desc(Movie.id)).limit(1)
        selected_id = [id.format() for id in selected]
        dict = selected_id[0]
        delete_id = dict['id']

        # pass parameter into url
        param = {'id': delete_id}
        res = self.client().delete('/movies/{id}'.format(**param))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_movie(self):
        print("*** Test '/movies/<int:id>' DELETE error ***")
        # invalid None record to delete
        res = self.client().delete('/movies/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_movie_title(self):
        print("*** Test '/movies/search' GET success ***")
        search_title = 'Star Wars'
        url = f'/movies/search?title={search_title}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    # # '''
    # # TEST ACTOR APIs
    # #
    # # '''

    def test_get_all_actors(self):
        print("*** Test '/actors' GET success ***")
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_get_no_actors(self):
        print("*** Test '/actors' GET error ***")
        # simulate a bad get with invalid url
        res = self.client().get('/actor')
        self.assertEqual(res.status_code, 404)

    def test_get_actors_equals_two(self):
        print("*** Test '/actors/<ind:id>' GET success ***")
        res = self.client().get('/actors/2')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_get_actors_not_equals_ten_thousand(self):
        print("*** Test '/actors/<ind:id>' GET error ***")
        res = self.client().get('/actors/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_actors(self):
        print("*** Test '/actors' POST success ***")
        data = {
            'id': None,
            'first_name': 'Test New Robot',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        res = self.client().post('/actors', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_post_no_actors(self):
        print("*** Test '/actors' POST error ***")
        data = {
            'first_name': 'Test New Robot',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        # attempt to post new record to invalid url
        res = self.client().post('/actor', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_patch_actors(self):
        print("*** Test '/actors/<int:id>' PATCH success ***")
        data = {
            'id': None,
            'first_name': 'Test PATCH New Robot-2',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        res = self.client().patch('/actors/2', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_patch_no_actors(self):
        print("*** Test '/actors' PATCH error ***")
        data = {
            'id': 2,
            'first_name': 'Test New Robot',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        res = self.client().patch('/actors/0', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_actors_publish_patch(self):
        print("*** Test '/actors/<int:id>' Publish PATCH success ***")
        # publish actor
        res1 = self.client().patch('/actors/2/publish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertIn("success", data1, "success key present")
        self.assertTrue("success" in data1, "success is True")
        self.assertTrue(data1["success"], "value of success key")

        # verify actor is published
        res2 = self.client().get('/actors/2')
        data2 = json.loads(res2.data)
        actor = data2["actor"]
        self.assertTrue(actor['actor_publish'], "actor is published")

    def test_actors_unpublish_patch(self):
        print("*** Test '/actors/<int:id>' Unpublish PATCH success ***")
        # unpublish actor
        res1 = self.client().patch('/actors/2/unpublish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertIn("success", data1, "success key present")
        self.assertTrue("success" in data1, "success is True")
        self.assertTrue(data1["success"], "value of success key")

        # verify actor is unpublished
        res2 = self.client().get('/actors/2')
        data2 = json.loads(res2.data)
        actor = data2["actor"]
        self.assertFalse(actor['actor_publish'], "actor is not published")

    def test_actors_toggle_publish_patch(self):
        print("*** Test '/actors/<int:id>' Toggle Publish PATCH success ***")
        res1 = self.client().get('/actors/2')
        data1 = json.loads(res1.data)

        if (data1["actor"]["actor_publish"]):
            self.test_actors_unpublish_patch()
            self.test_actors_publish_patch()
        else:
            self.test_actors_publish_patch()
            self.test_actors_unpublish_patch()

    def test_delete_actor(self):
        print("*** Test '/actors/<int:id>' DELETE success ***")

        # insert actor to delete
        self.test_post_actors()

        # get id from object of inserted actor to be deleted
        selected = Actor.query.order_by(desc(Actor.id)).limit(1)
        selected_id = [id.format() for id in selected]
        dict = selected_id[0]
        delete_id = dict['id']

        # pass parameter into url
        param = {'id': delete_id}
        res = self.client().delete('/actors/{id}'.format(**param))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_actor(self):
        print("*** Test '/actors/<int:id>' DELETE error ***")
        # invalid None record to delete
        res = self.client().delete('/actors/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_search_actor_first_name(self):
        print("*** Test '/actors/search' GET success ***")
        search_firstname = 'C3PO'
        url = f'/actors/search?firstname={search_firstname}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable


if __name__ == "__main__":

    unittest.main()
