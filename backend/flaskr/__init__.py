from flask import Flask, jsonify, request, abort, Response
from flask_cors import CORS
from sqlalchemy import func

from flaskr.helper import get_all_categories_formatted, paginate_questions, search_questions
from models import setup_db, Question, Category


def create_app():
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/api/v1/categories', methods=['GET'])
    def get_all_categories() -> Response:
        """
        Get endpoint to fetch all categories
        :return: Json response containing categories as key value pairs
        """
        response = get_all_categories_formatted()

        return jsonify({
            'success': True,
            'categories': response
        })

    @app.route('/api/v1/questions', methods=['GET'])
    def get_all_questions() -> Response:
        """
        Get endpoint to fetch all questions
        :return: Json response containing all questions, categories, total questions
        """
        questions = Question.query.order_by(Question.id).all()
        if not questions:
            return abort(404, description='No question is present, please add a question and then try')
        questions_response = paginate_questions(request, questions)

        categories_response = get_all_categories_formatted()

        return jsonify({
            'success': True,
            'questions': questions_response,
            'categories': categories_response,
            'total_questions': len(questions),
            'current_category': None
        })

    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id) -> Response:
        """
        Delete endpoint to delete a question
        :param question_id: Id of the question to be deleted
        :return: Json response containing Id of the question delete
        """
        question = Question.query.get_or_404(question_id, description=f'Question with id={question_id} is not present')
        try:
            question.delete()
        except Exception as ex:
            return abort(500, description=f'Unable to delete the question. Error - {ex}')

        return jsonify({
            'success': True,
            'question_id': question_id
        })

    @app.route('/api/v1/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_based_on_categories(category_id) -> Response:
        """
        Get endpoint to fetch all questions for a particular category
        :param category_id: Id of the category
        :return: Json response containing current category id, questions and total questions
        """
        if Category.query.get(category_id):

            questions = Question.query.filter_by(category=category_id).order_by(Question.id).all()
            if not questions:
                abort(404, f'No question found for the category id {category_id}')
            questions_response = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'current_category': category_id,
                'questions': questions_response,
                'total_questions': len(questions)
            })
        else:
            abort(404, f'Category with id {category_id} doesn\'t exist')

    @app.route('/api/v1/questions', methods=['POST'])
    def post_question() -> Response:
        """
        Post endpoint to create a new question
        :return: Returns JSON response corresponding to created question
        """
        body = request.get_json()
        if not body:
            # posting an empty json should return a 400 error.
            abort(400, 'JSON passed is empty')
        if body['question'] and body['answer'] and body['difficulty'] and body['category']:
            question = Question(
                question=body['question'],
                answer=body['answer'],
                difficulty=body['difficulty'],
                category=body['category'],
            )
            question.insert()
            return jsonify({
                "success": True,
                "created_question": question.format(),
                "id": question.id
            })

        else:
            return abort(400, description='Either of the question, answer, difficulty or category is not passed')

    @app.route('/api/v1/questions/search', methods=['POST'])
    def search_question() -> Response:
        """
        Post endpoint to search questions based on search_term
        :return: Returns JSON response corresponding to Searched questions
        """
        body = request.get_json()
        if not body:
            # posting an empty json should return a 400 error.
            abort(400, 'JSON passed is empty')
        # if searchTerm key is present in the body, search questions, else create a new question
        if 'searchTerm' not in body.keys():
            abort(400, 'Invalid JSON, "searchTerm" key is not present')
        else:
            if body['searchTerm']:
                return search_questions(request, body['searchTerm'])
            else:
                return abort(400, description='Search term is empty')

    @app.route('/api/v1/quizzes', methods=['POST'])
    def play_quiz() -> Response:
        """
        Post endpoint to start the quiz
        :return: Returns JSON response containing a question
        """
        all_category_ids = [x.id for x in Category.query.all()]
        body = request.get_json()
        if not body:
            return abort(400, description='JSON passed is empty')

        # if quiz_category is not present in the body, return error
        if 'quiz_category' not in body.keys() or 'previous_questions' not in body.keys():
            return abort(400, description='Invalid input JSON, either quiz_category or previous_questions key is'
                                          ' missing')
        category_id = int(body['quiz_category']['id'])
        if category_id != 0 and category_id not in all_category_ids:
            return abort(404, description=f'Invalid category id {category_id}')

        previous_questions = body['previous_questions']

        # if quiz_category is 0, it means All option has been selected, so we have to return all questions
        if body['quiz_category']['id'] == 0:
            question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        else:
            question = Question.query.filter(Question.category == body['quiz_category']['id'],
                                             Question.id.notin_(previous_questions)).order_by(func.random()).first()

        if not question:
            return jsonify({
                'success': True,
                'message': 'All questions are played out'
            })

        return jsonify({
            "success": True,
            "question": question.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': getattr(error, 'description', 'Resource Not Found')
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': getattr(error, 'description', 'Bad Request')
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': getattr(error, 'description', 'Internal Server Error')
        }), 500

    return app
