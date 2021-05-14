# Standard library imports
import os
import unittest 
import json

# Third party imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc

# Local application imports
from backend.src.database.models import setup_db, Movie, Actor, MovieActorLink, db
from backend.src.database.config import DATABASE_URL

class CastingAppTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castapp"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        #self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format('postgres','picasso0', 'localhost:5432', self.database_name)
        self.database_path = DATABASE_URL
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
        """Test Home page GET success"""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))
        self.assertEqual('Home page', json_res['message'])


    def test_404_home_page_not_found(self):
        """Test Home page GET error"""
        res = self.client().get('/home')
        self.assertEqual(res.status_code, 404)
        json_res = json.loads(res.get_data(as_text=False))
        self.assertEqual('Resource Not Found', json_res['message'])


    def test_given_cors_behavior(self):
        """Test CORS GET success"""
        res = self.client().get('/test_cors')
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))
        self.assertEqual('CORS is working...', json_res['message'])


    def test_404_home_page_not_found(self):
        """Test CORS GET error"""
        res = self.client().get('/home')
        self.assertEqual(res.status_code, 404)
        json_res = json.loads(res.get_data(as_text=False))
        self.assertEqual('Resource Not Found', json_res['message'])


    # '''
    # TEST MOVIE APIs
    # 
    # '''


    def test_get_all_movies(self):
        """Test '/movies' GET success"""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_404_get_no_movies(self):
        """Test '/movies' GET error"""
        res = self.client().get('/movies')
        #get movies set to length zero
        let res = 0
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')


    def test_get_movies_equals_two(self):
        """Test '/movies/<ind:id>' GET success"""
        res = self.client().get('/movies/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'])


    def test_404_get_movies_not_equals_ten_thousand(self):
        """Test '/movies/<ind:id>' GET error"""
        res = self.client().get('/movies/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


    def test_post_movies(self):
        """Test /movies' POST success"""         
        data = {
            'id': None,
            'title':'Test Robot Movie',
            'release_date':'2021-04-01',
            'movie_img':'https://robotmovie.jpg',
            'movie_publish':'False'
        }         
        res = self.client().post('/movies', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_422_post_no_movies(self):
        """Test /movies' POST error"""         
        data = {
            'id': '1',
            'title':'Test Robot Movie',
            'release_date':'2021-04-01',
            'movie_img':'https://robotmovie.jpg',
            'movie_publish':'False'
        }         
        res = self.client().post('/movies', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    def test_patch_movies(self):
        """Test /movies/<int:id>' PATCH success"""         
        data = {
            'title':'Test Robot Movie2',
            'release_date':'2021-04-01',
            'movie_img':'https://robotmovie.jpg',
            'movie_publish':'False'
        }         
        res = self.client().patch('/movies/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_422_patch_no_movies(self):
        """Test /movies' PATCH success"""         
        data = {
            'title':'Test Robot Movie2',
            'release_date':'2021-04-01',
            'movie_img':'https://robotmovie.jpg',
            'movie_publish':' '
        }         
        res = self.client().patch('/movies/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    def test_movies_publish_patch(self):
        """Test /movies/<int:id>' PATCH success"""         
        data = {
            'title':'Test Robot Movie2',
            'release_date':'2021-04-01',
            'movie_img':'https://robotmovie.jpg',
            'movie_publish':'True'
        }         
        res = self.client().patch('/movies/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_movies_unpublish_patch(self):
        """Test /movies/<int:id>' PATCH success"""         
        data = {
            'title':'Test Robot Movie2',
            'release_date':'2021-04-01',
            'movie_img':'https://robotmovie.jpg',
            'movie_publish':'False'
        }         
        res = self.client().patch('/movies/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_delete_movie(self):
        """Test '/movies/<int:id>' DELETE success"""

        #insert movie to delete
        self.test_post_movies()

        #get id from object of inserted question to be deleted
        selected = Movie.query.order_by(desc(Movie.id)).limit(1)
        selected_id = [id.format() for id in selected]
        dict = selected_id[0]
        delete_id = dict['id']      

        #pass parameter into url
        param = {'id' : delete_id}
        res = self.client().delete('/movies/{id}'.format(**param))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)


    def test_404_delete_movie(self):
        """Test '/questions/<int:id>' DELETE error"""  
        res = self.client().delete('/movies/0')
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


    def test_search_movie_title(self):
        """Test '/movies/search' GET success"""          
        data = {'search_title':'Jetsons'}
        res = self.client().get('/movies/search/{data}')
        data=json.dumps(data))
        results = json.loads(res.data)
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_404_search_title_unprocesssable(self):
        """Test '/movies/search' GET error"""
         data = {'search_title':' '}
        res = self.client().get('/movies/search/{data}')
        data=json.dumps(data))
        results = json.loads(res.data)
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


    # '''
    # TEST ACTOR APIs
    #
    # '''

    
    def test_get_all_actor(self):
        """Test '/actors' GET success"""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_404_get_no_actors(self):
        """Test '/actors' GET error"""
        res = self.client().get('/actors')
        #get actors set to length zero
        let res = 0
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')


    def test_get_actors_equals_two(self):
        """Test '/actors/<ind:id>' GET success"""
        res = self.client().get('/actors/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'])


    def test_404_get_actors_not_equals_ten_thousand(self):
        """Test '/actors/<ind:id>' GET error"""
        res = self.client().get('/actors/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


    def test_post_actors(self):
        """Test /actors' POST success"""         
        data = {
            'id': None,
            'first_name':'Test New Robot',
            'last_name':'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img':'https://robotactor.jpg',
            'actor_publish':'False'
        }         
        res = self.client().post('/actors', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_422_post_no_actors(self):
        """Test /actors' POST error"""         
        data = {
            'id': 1,
            'first_name':'Test New Robot',
            'last_name':'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img':'https://robotactor.jpg',
            'actor_publish':'False'
        }         
        res = self.client().post('/actors', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    def test_patch_actors(self):
        """Test /actors/<int:id>' PATCH success"""         
        data = {
            'id': None,
            'first_name':'Test PATCH New Robot-2',
            'last_name':'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img':'https://robotactor.jpg',
            'actor_publish':'False'
        }          
        res = self.client().patch('/actors/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_422_patch_no_actors(self):
        """Test /actors' PATCH success"""         
        data = {
            'id': 2,
            'first_name':'Test New Robot',
            'last_name':'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img':'https://robotactor.jpg',
            'actor_publish':'False'
        }          
        res = self.client().patch('/actors/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    def test_actors_publish_patch(self):
        """Test /actors/<int:id>' PATCH publish success"""         
        data = {
            'first_name':'Test PATCH New Robot-2',
            'last_name':'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img':'https://robotactor.jpg',
            'actor_publish':'True'
        }         
        res = self.client().patch('/actors/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_actors_unpublish_patch(self):
        """Test /actors/<int:id>' PATCH unpublish  success"""         
        data = {
            'first_name':'Test PATCH New Robot-2',
            'last_name':'Android',
            'birth_date': '2021-04-01',
            'gender': 'android',
            'actor_img':'https://robotactor.jpg',
            'actor_publish':'False'
        }       
        res = self.client().patch('/actors/2', 
        data=json.dumps(data),
        content_type='application/json')
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        json_res = json.loads(res.get_data(as_text=True))


    def test_delete_actor(self):
        """Test '/actors/<int:id>' DELETE success"""

        #insert actor to delete
        self.test_post_actors()

        #get id from object of inserted actor to be deleted
        selected = Actor.query.order_by(desc(Actor.id)).limit(1)
        selected_id = [id.format() for id in selected]
        dict = selected_id[0]
        delete_id = dict['id']      

        #pass parameter into url
        param = {'id' : delete_id}
        res = self.client().delete('/actors/{id}'.format(**param))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_404_delete_actor(self):
        """Test '/actors/<int:id>' DELETE error"""  
        res = self.client().delete('/actors/0')
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


    def test_search_actor_first_name(self):
        """Test '/actors/search' GET success"""          
        data = {'search_firstname':'Star Wars'}
        res = self.client().get('/actors/search/{data}')
        data=json.dumps(data))
        results = json.loads(res.data)
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    def test_404_search_title_unprocesssable(self):
        """Test '/movies/search' GET error"""
         data = {'search_title':' '}
        res = self.client().get('/movies/search/{data}')
        data=json.dumps(data))
        results = json.loads(res.data)
        self.data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)



# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()