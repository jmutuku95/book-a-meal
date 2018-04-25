'''This contains a a basetest case'''

from unittest import TestCase
import json
# local imports
try:
    from app import create_app
    from app.models import database, Meal, User, Menu, Admin, Order, Database
except ModuleNotFoundError:
    from ..app import create_app
    from ..app.models import database, Meal, User, Menu, Admin, Order, Database


class BaseTestClass(TestCase):
    '''An abstract base class for tests, contains
    all common variables methods'''

    def setUp(self):
        self.maxDiff = None
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.new_user = {'username': 'john', 'email': 'john@mail.com',
                         'password': 'password'}
        self.admin_user = {'username': 'admin', 'email': 'admin@mail.com',
                           'password': 'password', 'admin': True}
        self.test_user = {'username': 'martin', 'email': 'mar@ma.com',
                          'password': 'password'}
        self.Database = Database()
        self.Meal = Meal
        self.Order = Order
        self.Menu = Menu
        self.Order = Order
        self.User = User
        self.Admin = Admin
        self.meal = {'meal_id': 1, 'name': 'Fish', 'price': 100,
                     'description': 'Tasty Tilapia'}
        self.meal2 = {'meal_id': 2, 'name': 'Beef', 'price': 150,
                     'description': 'Tasty beef'}
        self.register_user()

    def create_user(self):
        u = self.User(username=self.test_user['username'], email=self.test_user['email'], password=self.test_user['password'])
        self.Database.add(u)
    
    def register_user(self):
        new_user = {'username': 'joe', 'email': 'jo@h.com', 'password': 'test1234'}
        self.client.post('/v1/auth/signup', data=json.dumps(new_user))

    def login_user(self, username='joe', password='test1234'):
        user_info = dict(username=username, password=password)
        res = self.client.post('/v1/auth/signin', data=json.dumps(user_info))
        return res

    def login_admin(self):
        '''helper function to create an admin user and log them in '''
        self.client.post('/v1/auth/signup', data=json.dumps(self.admin_user))
        data = {'password': 'password', 'email': 'admin@mail.com', 'username':'admin'}
        res = self.client.post('v1/auth/signin', data=json.dumps(data))
        return res


    def create_meal(self):
        '''helper function to populate Meals so tests on menu and orders 
        can work'''
        meal = self.Meal(
            meal_id=1, name='Fish', price=100, description='Tasty Tilapia')
        self.Database.add(meal)

    def tearDown(self):
        # reset all database entries to empty dicts
        self.Database = Database()