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

print("**** test_tokens_app.py - 11 tests (7 tokens - 4 public) ****")
print(" ")


class CastingAppTokensTestCase(unittest.TestCase):
    """Class represents the CastingApp Token test cases - tested locally"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app()
        self.client = self.app.test_client
        self.assistant_accesstoken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiYXNzaXN0YW50Il0sImlzcyI6Imh0dHBzOi8vYXV0dW1uLXZvaWNlLTA2NjYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYjEyYzFhZTIwMGNiMDA3MDk3NmI1OSIsImF1ZCI6WyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vYXBpIiwiaHR0cHM6Ly9hdXR1bW4tdm9pY2UtMDY2Ni51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjI1OTUyMTE2LCJleHAiOjE2MjYwMzg1MTYsImF6cCI6ImY3WkxVMkRtV2VSY0x1aWt5RUtqcWswODkzS0EyTWJqIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3Rvci1pZCIsImdldDptb3ZpZS1pZCIsInBhdGNoOmFjdG9yLXB1Ymxpc2giLCJwYXRjaDphY3RvcnMiLCJwYXRjaDphY3Rvci11bnB1Ymxpc2giLCJwYXRjaDptb3ZpZS1wdWJsaXNoIiwicGF0Y2g6bW92aWVzIiwicGF0Y2g6bW92aWUtdW5wdWJsaXNoIl19.Z_KnnFNMwV90_5XLRHCh3bu3jp-FDRlLRIi_e1a6oUhhwUKg5DryXgrPOh6OboawMH7nJEQBpoi88IOtqm9V4TODnvfk2Ml6oaKqgVH_NjRR0qiUhyhc8q4l0aEhjShkc5wtX7PgcKS0nO3zZSdc3BrU6RKklDoh5Q6ieI4St7io502LBF8wT_rybHQZyC40bsdMTlzSbqpHHwVwV26v8BKKy_-ku4hBQF-6opSD_42UsaK1G8p1vOF_BiehVH-pdUa5OrnxZ0wmAf2OmAu4Z71tt-iqGXruBGIaf0R9Z0tHiJ7tpf7s9J9jcr-hJcv3iToJyK8ao3lBcf3OAW_eAA"
        self.director_accesstoken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiZGlyZWN0b3IiXSwiaXNzIjoiaHR0cHM6Ly9hdXR1bW4tdm9pY2UtMDY2Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBiMTI2NDg5MjNmZTIwMDZmMDgwOWZlIiwiYXVkIjpbImh0dHBzOi8vY2FzdC1hcHAuaGVyb2t1YXBwLmNvbS9hcGkiLCJodHRwczovL2F1dHVtbi12b2ljZS0wNjY2LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MjU5OTg4NDMsImV4cCI6MTYyNjA4NTI0MywiYXpwIjoiZjdaTFUyRG1XZVJjTHVpa3lFS2pxazA4OTNLQTJNYmoiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3ItaWQiLCJnZXQ6bW92aWUtaWQiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.r9wFhvCuvnKwVvz4tWiPyBiQItERyfGLGVBZwwSgIDk6LbWV3jc2_h_7tjpSL3ANED_vJpWyzL2OzVyjFYok1r9HDfWI-nF_aTByn4hDKw3unQ9qYFiu7uj7sQhIlN8l4aJDzj29NAWbZe3Hq1ktmr1cK38xwQEkxFNBKyaKzQiXEAFHtLh4s8zd5WU38x2jjCU1rA4ZN23RzPGrYGHhcFFtx5LwzGgdw717xKZ7v_c-yRDd8J8miKslOE7AJgCQbfZDMMFomAE8l4bGOB_LKbZmcBAPmORbfFViX5PzTX4bLBhyxe-maAg7leKHzI1Y3vFGxukEh-mWueegripVsg"
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
        """Executed after each test"""
        pass

    # '''
    # TESTS APIs for PUBLIC AND ACCESS TOKENS
    # Public is only able to get all movies, all actors and search
    # '''

    def test_401_get_movies_two_fails_no_token(self):
        print("*** Test '/api/movies/<ind:id>' GET error no token ***")
        res = self.client().get('/api/movies/2',
                                headers={'Authorization': 'Bearer ' + ''})
        self.assertEqual(res.status_code, 401)

    def test_200_get_movies_two_success_assistant_accesstoken(self):
        print("*** Test '/api/movies/<ind:id>' GET success - assistant ***")
        res = self.client().get('/api/movies/2',
                                headers={"Authorization": "Bearer {}".format(
                                    self.assistant_accesstoken)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_200_get_movies_two_success_director_accesstoken(self):
        print("*** Test '/api/movies/<ind:id>' GET success - director ***")
        res = self.client().get('/api/movies/2',
                                headers={"Authorization":
                                         "Bearer {}".format(
                                             self.director_accesstoken)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_200_patch_movies_success_assistant_accesstoken(self):
        print("*** Test '/api/movies/<int:id>' PATCH success - assistant ***")
        data = {
            'title': 'Test Robot Movie2',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().patch(
            '/api/movies/2',
            data=json.dumps(data),
            content_type='application/json',
            headers={
                "Authorization": "Bearer {}".format(
                    self.assistant_accesstoken)})
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_401_patch_movies_fails_director_accesstoken(self):
        print("*** Test '/api/movies/<int:id>' PATCH fails - director ***")
        data = {
            'title': 'Test Robot Movie2',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().patch(
            '/api/movies/2',
            data=json.dumps(data),
            content_type='application/json',
            headers={
                "Authorization": "Bearer {}".format(
                    self.director_accesstoken)})
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        json_res = json.loads(res.get_data(as_text=True))

    def test_200_post_movies_success_director_accesstoken(self):
        print("*** Test '/api/movies' POST success - director ***")
        data = {
            'id': None,
            'title': 'Test Robot Movie',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().post(
            '/api/movies',
            data=json.dumps(data),
            content_type='application/json',
            headers={
                "Authorization": "Bearer {}".format(
                    self.director_accesstoken)})
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))

    def test_401_post_movies_fails_assistant_accesstoken(self):
        print("*** Test '/api/movies' POST fails - assistant ***")
        data = {
            'id': None,
            'title': 'Test Robot Movie',
            'release_date': '2021-04-01',
            'movie_img': 'https://robotmovie.jpg',
            'movie_publish': 'False'
        }
        res = self.client().post(
            '/api/movies',
            data=json.dumps(data),
            content_type='application/json',
            headers={
                "Authorization": "Bearer {}".format(
                    self.assistant_accesstoken)})
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        json_res = json.loads(res.get_data(as_text=True))

    def test_get_all_movies_no_token_needed(self):
        print("*** Test '/api/movies' GET success - public ***")
        res = self.client().get('/api/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_all_actors_no_token_needed(self):
        print("*** Test '/api/actors' GET success - public ***")
        res = self.client().get('/api/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_search_movie_title_no_token_needed(self):
        print("*** Test '/api/movies/search' GET success - public ***")
        search_title = 'Star Wars'
        url = f'/api/movies/search?title={search_title}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_search_actor_first_name_no_token_needed(self):
        print("*** Test '/api/actors/search' GET success - public ***")
        search_firstname = 'C3PO'
        url = f'/api/actors/search?firstname={search_firstname}'
        res = self.client().get(url)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable


if __name__ == "__main__":

    unittest.main()
