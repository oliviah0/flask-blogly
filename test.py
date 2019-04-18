from unittest import TestCase
from app import app
from models import db, connect_db, User, Post

LOREM_IPSUM = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis hic reprehenderit reiciendis harum commodi incidunt iure, inventore veniam velit dolore placeat voluptatibus sed rem rerum nesciunt sunt exercitationem nemo quis."
class FlaskTest(TestCase):
    """Tests if the routing works"""

    def setUp(self):
        print("'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'LOOK HERE: I'm setting up")
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test'
        db.create_all()
        dimsum = User(first_name='Dim', last_name='Sum',
                      img_url='http://www.dimsumcentral.com/wp-content/uploads/2018/06/what-is-dim-sum-header-new.jpg')
        wonka = User(first_name='Willy', last_name='Wonka',
                     img_url='https://hips.hearstapps.com/digitalspyuk.cdnds.net/18/07/1518524211-gene-wilder-willy-wonka.jpg?resize=480:*')
        
        db.session.add_all([dimsum, wonka])
        db.session.commit()

        post1 = Post(title="Post example 1", content=LOREM_IPSUM, user_id=1)
        post2 = Post(title="Post example 2", content=LOREM_IPSUM.upper(), user_id=2)

        db.session.add_all([post1, post2])
        
        db.session.commit()


    def tearDown(self):
        db.drop_all()

    # def test_users(self):
    #     """Tests the index"""

    #     with self.client:
    #         response = self.client.get('/users')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'<ul>', response.data)
    #         self.assertIn(b'<h1> Users </h1>', response.data)


    # def test_user(self):

    #     with self.client:
    #         response = self.client.get('/users/user/2')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'Wonka', response.data)

    
    # def test_create(self):

    #     with self.client:

    #         response = self.client.post('/users/create',
    #                                     data = {"first-name": "Cactus", "last-name":"Prickle",
    #                                      "img-url":"https://cdn.shopify.com/s/files/1/1111/4656/products/20181115_125634_600x800_600x.jpg?v=1543815335"}, follow_redirects=True)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'Cactus', response.data)

    
    # def test_edit(self):

    #     with self.client:
    #         response = self.client.post('/users/user/1/edit',
    #                                     data = {"first-name": "SUM", "last-name":"DIM",
    #                                      "img-url":"http://www.dimsumcentral.com/wp-content/uploads/2018/06/what-is-dim-sum-header-new.jpg"}, follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'SUM', response.data) #response data returns HTML or whatever we return in app.py

    def test_new_post(self):
        """Tests the creation of a new post. """

        with self.client:
            response = self.client.post('/users/user/1/posts/new',
                                        data = {"post-title": "Mountains", "post-content":LOREM_IPSUM[::-1]}, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Mountains', response.data)
    
    def test_post_page(self):
        """Tests the post page UI """
        
        with self.client:
            response = self.client.get("/posts/1")
            self.assertIn(b'Post example 1', response.data)
            # Test if all the buttons are in there
            self.assertIn(b'<a href="/users/user/1" class="btn btn-outline-primary">Cancel</a>', response.data)
            self.assertIn(b'<a href="/posts/1/edit" class="btn btn-primary">Edit</a>', response.data)
            self.assertIn(b'<a href="/posts/1/delete" class="btn btn-danger">Delete</a>', response.data)
