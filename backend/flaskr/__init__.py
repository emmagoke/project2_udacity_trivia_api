import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_question(request, questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_request = [question.format() for question in questions]
    current_page = formatted_request[start:end]

    return current_page

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resource={r'*/api/*' : {'origin': '*'}})

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Context-Type, Authorization, True')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')

    return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.type).all()

    try:

      if len(categories) == 0:
        abort(404)
      
      return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories}
        })
    except:
      abort(400)

  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_question():
    questions = Question.query.order_by(Question.id).all()
    current_page = paginate_question(request, questions)

    # If there no more questions
    if len(current_page) == 0:
      abort(404)
    else:
      categories = Category.query.order_by(Category.type).all()

      return jsonify({
        'success': True,
        'questions': current_page,
        'total_questions': len(Question.query.all()),
        'categories': {category.id: category.type for category in categories}
        })

  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:
      question = Question.query.get(question_id)
      print('Question to be deleted -> ', question)

      if question is None:
        abort(404)

      else:
        question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id,
        'total_questions': len(Question.query.all()),
        'message': 'You successfully deleted the question'
        })
    except Exception as error:
      print(error)
      abort(422)

  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def new_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    search = body.get('searchTerm')
    # print('new_search -> :', body)
    # # print('new_search -> :', body)
    try:
      if search:
      
        questions = Question.query.order_by(Question.id).filter(
          Question.question.ilike(f'%{search}%')).all()
        current_page = paginate_question(request, questions)

        return jsonify({
          'success': True,
          'questions': current_page,
          'total_questions': len(questions),
          'current_category': None
          })

      elif search == '':
        abort(422)

      else:

        if (new_question == '' or new_answer=='' or new_category =='' or new_difficulty ==''):
          abort(422)

        question = Question(question=new_question, answer=new_answer,
          category=new_category,difficulty=new_difficulty)
        # print('This is the question: ', question.question)
        question.insert()

        questions = Question.query.all()
        current_page = paginate_question(request,questions)

        categories = Category.query.all()

        return jsonify({
          'success': True,
          'questions': current_page,
          'total_questions': len(Question.query.all()),
          'categories': {category.id: category.type for category in categories},
          })
    except:
      abort(404)

  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''


  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  # @app.route('/questions', methods=['POST'])
  # def search_question():
  #   body = request.get_json()
  #   search = body.get('search_term')

  #   if search is None:
  #     abort(404)

  #   else:
  #     questions = Question.query.order_by(Question.id).filter(
  #       Question.question.ilike(f'%{search}%')).all()
  #     current_page = paginate_question(request, questions)

  #     return jsonify({
  #       'success': True,
  #       'questions': current_page,
  #       'total_questions': len(questions),
  #       'current_category': None
  #       })

  '''
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def question_per_category(category_id):

    questions = Question.query.order_by(Question.id).filter(
                            Question.category == category_id).all()

    try:

      if len(questions) == 0:
        abort(422)

      else:
        current_page = paginate_question(request, questions)

        return jsonify({
          'success': True,
          'questions': current_page,
          'total_questions': len(questions),
          'categories': category_id 
          })
    except:
      abort(404)


  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quiz', methods=['POST'])
  def quiz():
    body = request.get_json()

    quiz_category = body.get('quiz_category')
    p_question = body.get('previous_questions')
    # print('This quiz_category ;; -> :' , quiz_category)
    # print('This quiz_pq ;; -> :' , p_question)

    try:

      if (quiz_category is None) or (p_question is None):
        abort(400)

      # default
      if (quiz_category['id'] == 0) and (quiz_category['type'] == 'click'):
        # questions = Question.query.order_by(Question.id).filter(
        #   ~Question.id.in_(p_question)).all()
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == quiz_category['id']).all()
        # questions = Question.query.filter(Question.id.not_in_(p_question)).all()
        # questions = Question.query.filter(
        #   ~Question.id.not_in_(p_question) ,
        #   Question.category == quiz_category['id']).all()

      next_question = questions.pop()

      while  next_question.id in p_question :
        if len(p_question) == 0:
          break
        elif len(questions) == 0:
          break
        else:
          next_question = questions.pop()
      # print(next_question)

      return jsonify({
        'success': True,
        'question': next_question.format()
      })
    except:
      abort(422)


  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad_request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):

    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def method_not_found(error):

    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not found'
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):

    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
      }), 422

  @app.errorhandler(500)
  def server_error(error):

    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
      }) , 500
  

  return app

    