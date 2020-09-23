from flask import jsonify, abort, Response

from models import Category, Question

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selected_questions) -> list:
    """
    Returns paginated questions
    :param request: Request
    :param selected_questions: List of questions to be paginated
    :return: list of questions
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selected_questions]
    current_questions = questions[start:end]

    if not current_questions:
        return abort(404, description=f'No question is present for the page number {page}')

    return current_questions


def get_all_categories_formatted() -> dict:
    """
    Returns all categories formatted as key value pair
    :return: Categories as key value pairs
    """
    categories = Category.query.order_by(Category.id).all()
    if categories:
        return {category.id: category.type for category in categories}
    else:
        return abort(404, 'No category is present')


def search_questions(request, search_term) -> Response:
    """
    Search questions
    :param request: Request
    :param search_term: search term
    :return: JSON response containing all searched questions
    """
    questions = Question.query.filter(
        Question.question.ilike('%' + search_term + '%')
    ).all()
    if not questions:
        return abort(404, f'No question found with search term "{search_term}"')

    paginated_questions = paginate_questions(request, questions)

    return jsonify({
        "success": True,
        "questions": paginated_questions,
        "total_questions": len(questions)
    })
