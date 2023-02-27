import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represponseents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'presidenT98!'
            ,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
                'question': 'The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?',
                'answer': 'The Earth and the Sun',
                'category': 1,
                'difficulty': 5,
            }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # paginated_questions
    def test_paginated_questions(self):
        response = self.client().get('/questions')
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['questions'])
        self.assertTrue(len(body['questions']))
        self.assertEqual(body['success'], True)
        

    def test_404_paginated_questions(self):
        response = self.client().get('/questions?page=100', json={'category': 1})
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'resource not found')

    # Testing deletion
    def test_delete_question(self):
        response = self.client().delete('/questions/20')
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['deleted'], 20)
        self.assertTrue(body['total_questions'])
        self.assertTrue(len(body['questions']))

    def test_422_if_question_to_delete_does_not_exist(self):
        response = self.client().delete('/questions/100')
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')

    # Testing categories
    def test_categories(self):
        response = self.client().get('/categories')
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['categories'])
        self.assertTrue(len(body['categories']))

    

    def test_questions_by_categories(self):
        response = self.client().get('categories/1/questions')
        body = json.loads(response.data)

        self.assertEqual(body['success'], True)
        self.assertTrue(body['questions'])
        self.assertTrue(body['categories'])

    def test_404_questions_by_categories(self):
        response = self.client().get('categories/100/questions')
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'resource not found')

    # Testing the add route on the frontend
    def test_question(self):
        response = self.client().post('/questions', json=self.new_question)

        body = json.loads(response.data)
        # print(body)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertTrue(body['total_questions'])
        self.assertTrue(len(body['questions']))

    def error_422_test_question(self):
        response = self.client().post('/questions', json={'question': '',
            'answer': '','category': 1,'difficulty': 5,})
        body = json.loads(response.data)

        self.assertTrue(response.status_code, 422)
        self.assertTrue(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')

    def test_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': 'based'})
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['questions'])
    
    def test_422_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': ''})
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')

    # Testing the quiz route
    def test_quiz(self):
        response = self.client().post('/quiz',
                                 json={'previous_questions': [],
                                       'quiz_category':
                                       {'id': '1', 'type': 'Science'}})
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['question'])
        self.assertEqual(body['question']['category'], 1)

    def test_422_quiz(self):
        response = self.client().post('/quiz',
                                 json={
                                     'previous_questions': []
                                 })
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()