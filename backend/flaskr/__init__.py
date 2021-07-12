import os
from flask import Flask, request, abort, jsonify
from flask.globals import current_app
from flask.helpers import make_response
from flask.signals import message_flashed
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS , cross_origin
import random
from sqlalchemy.sql.elements import Null

from sqlalchemy.sql.expression import select
from sqlalchemy.sql.type_api import NULLTYPE

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  #CORS(app)
# DONE
  ''' 
  @TODO: Use the after_request decorator to set Access-Control-Allow 
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response


  def pagination(request, selection):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions =[question.format() for question in selection]
    current = questions[start:end]

    return current

  def formated_categories():

    categories = Category.query.all()
    list_categories =[category.format() for category in categories]
    formated_categories = {}
    for i in list_categories:
      formated_categories[i['id']] = i['type']

    return formated_categories

  
  '''
  @TODO: DONE 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories' , methods=['GET'])
  @cross_origin()
  def get_categories():
    
    return jsonify({
          'success': True,
          'categories':formated_categories()
          })

  '''
  @TODO: [DONE]
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])  
  @cross_origin()
  def get_questions():
   

    questions = Question.query.order_by(Question.id).all()
    current_questions = pagination(request,questions)

    if len(current_questions) == 0:
      abort(404)


    return jsonify({
          'success': True,
          'questions':current_questions,
          'total_questions':len(questions),
          'categories':formated_categories(),
          'current_category': 'ALL'
          })



  '''
  @TODO: DONE 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True})
    except:
      abort(422)

    

  '''
  @TODO: [DONE]
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score. 
 
   TODO -> TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  @cross_origin()
  def create_question():
    body = request.get_json()

    new_question = body.get('question',None)
    new_answer = body.get('answer',None)
    new_category =  body.get('category',None)
    new_difficulty =  body.get('difficulty',None)
    search_term = body.get('searchTerm')


    try:
      if search_term :
          questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
          current_questions = pagination(request,questions)

          return jsonify({
                'success': True,
                'questions':current_questions,
                'totalQuestions':len(questions),
                'categories':formated_categories(),
                'current_category': 'ALL'
                })
      else:
          if new_question and new_answer:
            question = Question(new_question,new_answer,new_category,new_difficulty)
            question.insert()

            return jsonify({
            'success': True
                  })

          
          else: ## dosen't work .
            return jsonify({
            'success': False
                  })

          
    except:
      abort(422)

   

  '''


  @TODO: [DONE]
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''


  '''
  @TODO: [DONE]
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_per_category(category_id):

    if category_id not in formated_categories():
       abort(404)
   

    questions = Question.query.filter(Question.category == category_id).all()
    current_questions = pagination(request,questions)

    current_category =  Category.query.filter(Category.id == category_id).all()
    formated_category =[category.format() for category in current_category]
    return jsonify({
          'success': True,
          'questions':current_questions,
          'totalQuestions':len(questions),
          'currentCategory':formated_category
          })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  
  @app.route('/quizzes',methods=['POST'])
  @cross_origin()
  def play_quize():
    body = request.get_json()

    #previous_questions = body.get('previous_questions',None) # TO avoid duplication
    quiz_category = body.get('quiz_category','Entertainment')

    category_id = Category.query(Category.id).filter(Category.type == quiz_category).all()
    questions = Question.query.filter(Question.category == category_id).all()
    formated_questions =[question.format() for question in questions]
    question = random.choice(formated_questions)

    return jsonify({
      'success': True,
      'question':question
    })
  
  '''
  @TODO: [DONE]
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
      
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405
  
  
  return app

    