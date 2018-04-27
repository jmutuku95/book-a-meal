'''This contains a a basetest case'''

from unittest import TestCase
import json
# local imports
try:
    from app import create_app, app_db
    from app.models import Meal, User, Menu, Admin, Order, Database
except ModuleNotFoundError:
    from ..app import create_app, app_db
    from ..app.models import Meal, User, Menu, Admin, Order, Database


class BaseTestClass(TestCase):
    '''An abstract base class for tests, contains
    all common variables methods'''

    def setUp(self):
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
        self.database = app_db
        self.meal_model = Meal
        self.order_model = Order
        self.menu_model = Menu
        self.order_model = Order
        self.user_model = User
        self.admin_model = Admin
        self.meal = {'meal_id': 1, 'name': 'Fish', 'price': 100,
                     'description': 'Tasty Tilapia'}
        self.meal2 = {'meal_id': 2, 'name': 'Beef', 'price': 150,
                     'description': 'Tasty beef'}
        self.register_user()

    def create_user(self):
        u = self.user_model(username=self.test_user['username'], email=self.test_user['email'], password=self.test_user['password'])
        self.database.add(u)
    
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
        data = {'password': 'password', 'email': 'admin@mail.com', 'username': 'admin'}
        res = self.client.post('v1/auth/signin', data=json.dumps(data))
        return res

    def create_meal(self):
        '''helper function to populate Meals so tests on menu and orders 
        can work'''
        meal = self.meal_model(
            meal_id=1, name='Fish', price=100, description='Tasty Tilapia')
        self.database.add(meal)

    def tearDown(self):
        # reset all database entries to empty dicts
        app_db.admins = {}
        app_db.meals = {}
        app_db.users = {}
        app_db.users_email = {}
        app_db.current_menu = {}
        app_db.orders = {}
        app_db.user_orders = {}