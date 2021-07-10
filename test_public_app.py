# standard library imports
import os
import unittest
import json

# third party imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc

# local application imports
import app
import settings
from backend.src.database.models import setup_db, Movie, Actor, db

print("**** test_public_app.py ****")
print(" ")


class CastingAppPublicTestCase(unittest.TestCase):
    """Class represents the CastingApp Public test case - tested locally"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app()
        self.client = self.app.test_client
        self.database_name = "castapp_test"
        self.database_path = settings.LOCAL_DATABASE_PATH
        #self.test_asst = { 'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiYXNzaXN0YW50Il0sIm5pY2tuYW1lIjoiYXNzaXN0YW50LmNhc3QuYXBwIiwibmFtZSI6ImFzc2lzdGFudC5jYXN0LmFwcEBnbWFpbC5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvMjY0MGExNzA1MGI5ZmFmOTczMTQ2ZjViMzllMTI5MTg_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZhcy5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyMS0wNy0xMFQwMjozMjo1Ni41OTRaIiwiZW1haWwiOiJhc3Npc3RhbnQuY2FzdC5hcHBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYXV0dW1uLXZvaWNlLTA2NjYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYjEyYzFhZTIwMGNiMDA3MDk3NmI1OSIsImF1ZCI6ImY3WkxVMkRtV2VSY0x1aWt5RUtqcWswODkzS0EyTWJqIiwiaWF0IjoxNjI1ODg0NDA4LCJleHAiOjE2MjYzMTY0MDgsIm5vbmNlIjoiWVV0RGRXUnNRazQ1VUhkclgxOUNlazVoVUVwNFJFOWtlSGhVVEVjMWNEZFVkRmhYZm14SWFtVXhZZz09In0.Rxuj_nPSMDZYMqVQRf7irx7QravqINxD7j72uP77rPvr8KAxc92HpINRlguvqZkygfFHf_oz4o0cZkeomZsTGG5t-3gSCwRP5fNx60m2h-IE3KyPrO1eyFpHVageXxlhxyo3YrvDWXx0Uc8cOY2Bpnn7zKIXdzGGUBBU8YspZXBZGA9yhlg2eDIKWa6lGQGs72iANE09SbMEyqUGeVuRZwA-554C0vp7-HfULYZe-pdq2yUrWnMhrmoh1x6FutUUxMZxYLwOr_XLtybiXwCwNP6ZwQyq_BHT9V0IL8j0lGQRjwPLZXK7phXhfH6NrfOJ2LN2PvtlUzUKKADw4ydiUA' }
        # self.headers = {'Content-Type': 'application/json', 'Token': token, }
        ##self.test_asst = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiYXNzaXN0YW50Il0sImlzcyI6Imh0dHBzOi8vYXV0dW1uLXZvaWNlLTA2NjYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYjEyYzFhZTIwMGNiMDA3MDk3NmI1OSIsImF1ZCI6WyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vYXBpIiwiaHR0cHM6Ly9hdXR1bW4tdm9pY2UtMDY2Ni51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjI1ODcxNDg0LCJleHAiOjE2MjU5NTc4ODQsImF6cCI6ImY3WkxVMkRtV2VSY0x1aWt5RUtqcWswODkzS0EyTWJqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3Rvci1pZCIsImdldDptb3ZpZS1pZCIsInBhdGNoOmFjdG9yLXB1Ymxpc2giLCJwYXRjaDphY3RvcnMiLCJwYXRjaDphY3Rvci11bnB1Ymxpc2giLCJwYXRjaDptb3ZpZS1wdWJsaXNoIiwicGF0Y2g6bW92aWVzIiwicGF0Y2g6bW92aWUtdW5wdWJsaXNoIl19.oKsWr4rmholcC0KRBE5XD6uW0ctMZVWfFJrOy3TdNHyiJIpKpftERJNLShah3LMuY3jZvceg_Y1gkSb8bP5hYVLQ1CN27eScuIPEIWxIbbpwcG8EKvKLSzY4HjI6ZFkxHhQlO9_1_QMA-0n8bFhj0FmX80tUskI-iVdVSyi5suXuSTqtEY6B7xfOvsV5Mrv4Xh-wO1PazUjKWl_sbkFYU_Pjy0_4CpDqhw3lT_Q5uJPbqpmhUSgyRLwB8hvoOAgvfd5fIV4kXUWMo2ZAjbYEy76AzcfAjMbT0TUuZWpdFraii0Unu9wlJ4q4VVfU_npNYFKA4RcZfTHW0cUEl_fHyA'}
        #self.test_asst = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiYXNzaXN0YW50Il0sImlzcyI6Imh0dHBzOi8vYXV0dW1uLXZvaWNlLTA2NjYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYjEyYzFhZTIwMGNiMDA3MDk3NmI1OSIsImF1ZCI6WyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vYXBpIiwiaHR0cHM6Ly9hdXR1bW4tdm9pY2UtMDY2Ni51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjI1ODg0NDA4LCJleHAiOjE2MjU5NzA4MDgsImF6cCI6ImY3WkxVMkRtV2VSY0x1aWt5RUtqcWswODkzS0EyTWJqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3Rvci1pZCIsImdldDptb3ZpZS1pZCIsInBhdGNoOmFjdG9yLXB1Ymxpc2giLCJwYXRjaDphY3RvcnMiLCJwYXRjaDphY3Rvci11bnB1Ymxpc2giLCJwYXRjaDptb3ZpZS1wdWJsaXNoIiwicGF0Y2g6bW92aWVzIiwicGF0Y2g6bW92aWUtdW5wdWJsaXNoIl19.RS323uyqTAd6oK7OR0tcpoVvtEevtlMAbRu_pKHvHqB2LF2puyMu_R8IlP1zsViT_UQnzeMP6JXKVA_DhObJuEiD12RCSqW-2nZMkz02VGuU05-moNo1Zw3yCcxyRPKyPbBY5ohnOGTaDz8jlKz5bwYGejIzQz36XEBZlPI0-InUC5oPYs11zG4iLNSIlPgMMg9fke8fVvHdhdWftlqNO92pacOHclvw8kI-TGQGpgG-M9igee1vW5AImiP33wQTuX4ctaxHAVBOOj7AbTgAbJY6-sbsBr6MkYB6ch_MOQVFn7_Swr-qqE9M2vjfjUSGpDYJfw_7Py9F1XhqppCymg"
        self.test_asst = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiYXNzaXN0YW50Il0sIm5pY2tuYW1lIjoiYXNzaXN0YW50LmNhc3QuYXBwIiwibmFtZSI6ImFzc2lzdGFudC5jYXN0LmFwcEBnbWFpbC5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvMjY0MGExNzA1MGI5ZmFmOTczMTQ2ZjViMzllMTI5MTg_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZhcy5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyMS0wNy0xMFQwMjozMjo1Ni41OTRaIiwiZW1haWwiOiJhc3Npc3RhbnQuY2FzdC5hcHBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYXV0dW1uLXZvaWNlLTA2NjYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYjEyYzFhZTIwMGNiMDA3MDk3NmI1OSIsImF1ZCI6ImY3WkxVMkRtV2VSY0x1aWt5RUtqcWswODkzS0EyTWJqIiwiaWF0IjoxNjI1ODg0NDA4LCJleHAiOjE2MjYzMTY0MDgsIm5vbmNlIjoiWVV0RGRXUnNRazQ1VUhkclgxOUNlazVoVUVwNFJFOWtlSGhVVEVjMWNEZFVkRmhYZm14SWFtVXhZZz09In0.Rxuj_nPSMDZYMqVQRf7irx7QravqINxD7j72uP77rPvr8KAxc92HpINRlguvqZkygfFHf_oz4o0cZkeomZsTGG5t-3gSCwRP5fNx60m2h-IE3KyPrO1eyFpHVageXxlhxyo3YrvDWXx0Uc8cOY2Bpnn7zKIXdzGGUBBU8YspZXBZGA9yhlg2eDIKWa6lGQGs72iANE09SbMEyqUGeVuRZwA-554C0vp7-HfULYZe-pdq2yUrWnMhrmoh1x6FutUUxMZxYLwOr_XLtybiXwCwNP6ZwQyq_BHT9V0IL8j0lGQRjwPLZXK7phXhfH6NrfOJ2LN2PvtlUzUKKADw4ydiUA'
        #self.access_token = ""
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # '''
    # TEST HOME AND CORS APIs
    #
    # '''

    def test_given_home_page_behavior(self):
        print("*** Test '/' GET success ***")
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_404_home_page_not_found(self):
        print("*** Test '/home' GET error ***")
        res = self.client().get('/home')
        self.assertEqual(res.status_code, 404)

    def test_given_cors_behavior(self):
        print("*** Test '/test_cors' GET success ***")
        res = self.client().get('/test_cors')
        self.assertEqual(res.status_code, 200)

    def test_404_cors_not_found(self):
        print("*** Test '/test_cors' GET error ***")
        res = self.client().get('/test_cor')
        self.assertEqual(res.status_code, 404)

    # '''
    # TEST MOVIE APIs
    # Public is only able to get all movies, all actors and search
    # '''

    def test_get_all_movies(self):
        print("*** Test '/api/movies' GET success ***")
        res = self.client().get('/api/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_get_no_movies(self):
        print("*** Test '/api/movies' GET error ***")
        # simulate a bad get with removing "s" from movie
        res = self.client().get('/api/movie')
        self.assertEqual(res.status_code, 404)

    def test_401_get_movies_two_fails(self):
        print("*** Test '/api/movies/<ind:id>' GET error ***")
        res = self.client().get('/api/movies/2',
            headers={'Authorization': 'Bearer ' + self.test_asst})
            #headers=self.test_asst)
            #headers={"Authorization": "Bearer {}".format(self.test_asst)})
            #headers=self.auth_header)
            #headers={'Authorization':'Bearer ' + self.test_asst})
            #headers={'Authorization':'Bearer ' + str(self.test_asst)})
        #data = json.loads(res.data)
        #self.assertEqual(res.status_code, 500)
        self.assertEqual(res.status_code, 401)
        #self.assertEqual(data['message'], {'code': 'insufficient roles', 
        #'description':'You do not have roles for this operation.'})
        #self.assertEqual(data['code'], 'insufficient_roles')
        #self.assertEqual(data['message'], 'Token not found')
        #self.assertEqual(data['success'], False)

    # def test_200_get_movies_two_success(self):
    #     print("*** Test '/api/movies/<ind:id>' GET success ***")
    #     res = self.client().get('/api/movies/2', 
    #         headers={'Authorization':'Bearer ' +self.test_asst})
    #     self.assertEqual(res.status_code, 200)





    def test_post_movies(self):
        print("*** Test '/api/movies' POST success ***")
        data = {
            'id': None,
            'title': 'Test Robot Movie',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().post('/api/movies', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_post_no_movies(self):
        print("*** Test '/api/movies' POST error ***")
        data = {
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().post('/api/movie', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_patch_movies(self):
        print("*** Test '/api/movies/<int:id>' PATCH success ***")
        data = {
            'title': 'Test Robot Movie2',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().patch('/api/movies/2', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_patch_no_movies(self):
        print("*** Test '/api/movies' PATCH error ***")
        data = {
            'title': 'Test Robot Movie2',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        # set movie to invalid id of zero
        res = self.client().patch('/api/movies/0', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_movies_publish_patch(self):
        print("*** Test '/api/movies/<int:id>' Publish PATCH success ***")
        # publish movie
        res1 = self.client().patch('/api/movies/2/publish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertIn("success", data1, "success key present in body")
        self.assertTrue("success" in data1, "success is True")
        self.assertTrue(data1["success"], "value of success key in body")

        # verify movie is published
        res2 = self.client().get('/api/movies/2')
        data2 = json.loads(res2.data)
        movie = data2["movie"]
        self.assertTrue(movie['movie_publish'], "movie is published")

    def test_movies_unpublish_patch(self):
        print("*** Test '/api/movies/<int:id>' Unpublish PATCH success ***")
        # unpublish movie
        res1 = self.client().patch('/api/movies/2/unpublish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data2 = json.loads(res1.data)
        self.assertIn("success", data2, "success key present in body")
        self.assertTrue("success" in data2, "success is True")
        self.assertTrue(data2["success"], "value of success key in body")

        # verify movie is unpublished
        res2 = self.client().get('/api/movies/2')
        data3 = json.loads(res2.data)
        movie = data3["movie"]
        self.assertFalse(movie['movie_publish'], "movie is not published")

    def test_movies_toggle_publish_patch(self):
        print("*** Test '/api/movies/<int:id>' Toggle Publish PATCH success ***")
        res1 = self.client().get('/api/movies/2')
        data1 = json.loads(res1.data)

        if (data1["movie"]["movie_publish"]):
            self.test_movies_unpublish_patch()
            self.test_movies_publish_patch()
        else:
            self.test_movies_publish_patch()
            self.test_movies_unpublish_patch()

    def test_delete_movie(self):
        print("*** Test '/api/movies/<int:id>' DELETE success***")
        # insert movie to delete
        self.test_post_movies()

        # get id from object of inserted question to be deleted
        selected = Movie.query.order_by(desc(Movie.id)).limit(1)
        selected_id = [id.format() for id in selected]
        dict = selected_id[0]
        delete_id = dict['id']

        # pass parameter into url
        param = {'id': delete_id}
        res = self.client().delete('/api/movies/{id}'.format(**param))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_movie(self):
        print("*** Test '/api/movies/<int:id>' DELETE error ***")
        # invalid None record to delete
        res = self.client().delete('/api/movies/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_movie_title(self):
        print("*** Test '/api/movies/search' GET success ***")
        search_title = 'Star Wars'
        url = f'/api/movies/search?title={search_title}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    # # '''
    # # TEST ACTOR APIs
    # #
    # # '''

    def test_get_all_actors(self):
        print("*** Test '/api/actors' GET success ***")
        res = self.client().get('/api/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_get_no_actors(self):
        print("*** Test '/api/actors' GET error ***")
        # simulate a bad get with invalid url
        res = self.client().get('/api/actor')
        self.assertEqual(res.status_code, 404)

    def test_get_actors_equals_two(self):
        print("*** Test '/api/actors/<ind:id>' GET success ***")
        res = self.client().get('/api/actors/2')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_get_actors_not_equals_ten_thousand(self):
        print("*** Test '/api/actors/<ind:id>' GET error ***")
        res = self.client().get('/api/actors/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_actors(self):
        print("*** Test '/api/actors' POST success ***")
        data = {
            'id': None,
            'first_name': 'Test New Robot',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        res = self.client().post('/api/actors', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_post_no_actors(self):
        print("*** Test '/api/actors' POST error ***")
        data = {
            'first_name': 'Test New Robot',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        # attempt to post new record to invalid url
        res = self.client().post('/api/actor', data=json.dumps(data),
                                 content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_patch_actors(self):
        print("*** Test '/api/actors/<int:id>' PATCH success ***")
        data = {
            'id': None,
            'first_name': 'Test PATCH New Robot-2',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        res = self.client().patch('/api/actors/2', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_404_patch_no_actors(self):
        print("*** Test '/api/actors' PATCH error ***")
        data = {
            'id': 2,
            'first_name': 'Test New Robot',
            'last_name': 'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img': 'https://robotactor.jpg',
            'actor_publish': False
        }
        res = self.client().patch('/api/actors/0', data=json.dumps(data),
                                  content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_actors_publish_patch(self):
        print("*** Test '/api/actors/<int:id>' Publish PATCH success ***")
        # publish actor
        res1 = self.client().patch('/api/actors/2/publish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertIn("success", data1, "success key present")
        self.assertTrue("success" in data1, "success is True")
        self.assertTrue(data1["success"], "value of success key")

        # verify actor is published
        res2 = self.client().get('/api/actors/2')
        data2 = json.loads(res2.data)
        actor = data2["actor"]
        self.assertTrue(actor['actor_publish'], "actor is published")

    def test_actors_unpublish_patch(self):
        print("*** Test '/api/actors/<int:id>' Unpublish PATCH success ***")
        # unpublish actor
        res1 = self.client().patch('/api/actors/2/unpublish')

        # check http status code and return value
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertIn("success", data1, "success key present")
        self.assertTrue("success" in data1, "success is True")
        self.assertTrue(data1["success"], "value of success key")

        # verify actor is unpublished
        res2 = self.client().get('/api/actors/2')
        data2 = json.loads(res2.data)
        actor = data2["actor"]
        self.assertFalse(actor['actor_publish'], "actor is not published")

    def test_actors_toggle_publish_patch(self):
        print("*** Test '/api/actors/<int:id>' Toggle Publish PATCH success ***")
        res1 = self.client().get('/api/actors/2')
        data1 = json.loads(res1.data)

        if (data1["actor"]["actor_publish"]):
            self.test_actors_unpublish_patch()
            self.test_actors_publish_patch()
        else:
            self.test_actors_publish_patch()
            self.test_actors_unpublish_patch()

    def test_delete_actor(self):
        print("*** Test '/api/actors/<int:id>' DELETE success ***")

        # insert actor to delete
        self.test_post_actors()

        # get id from object of inserted actor to be deleted
        selected = Actor.query.order_by(desc(Actor.id)).limit(1)
        selected_id = [id.format() for id in selected]
        dict = selected_id[0]
        delete_id = dict['id']

        # pass parameter into url
        param = {'id': delete_id}
        res = self.client().delete('/api/actors/{id}'.format(**param))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_actor(self):
        print("*** Test '/api/actors/<int:id>' DELETE error ***")
        # invalid None record to delete
        res = self.client().delete('/api/actors/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_search_actor_first_name(self):
        print("*** Test '/api/actors/search' GET success ***")
        search_firstname = 'C3PO'
        url = f'/api/actors/search?firstname={search_firstname}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable


if __name__ == "__main__":

    unittest.main()
