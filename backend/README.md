# Full Stack Trivia API Backend


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## API Reference

### Getting Started
- Base URL: currently the server runs locally on `http://127.0.0.1:5000/`.
- Authentication: Is not configured as of now. 

### Error Handling
Flask's `@app.errorhandler` decorators are implemented for:
- 400: Resource not found
- 404: Resource not found
- 405: Resource not found
- 500: Internal server error

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "<Custom error message>"
}
```


### Endpoints 

### Categories

#### GET /api/v1/categories
- General:
    - Returns the list of all categories
- Sample: `curl http://127.0.0.1:5000/api/v1/categories`

```{
    "categories": {
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "success":true
}
```

#### GET /api/v1/categories/{category_id}/questions
- General:
    - Returns list of questions corresponding to the passed category_id.
    - Results are paginated in groups of 10.
    - Also returns the current_category and total questions for that category_id.
    - Returns 404 if category_id doesn't exist or no question is found the for the giver category_id
- Sample: `curl http://127.0.0.1:5000/api/v1/categories/6/questions`
```
{
    "current_category": 6,
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

### Questions

#### GET /api/v1/questions
- General:
    - Fetches list of all questions
    - Results are paginated in groups of 10
    - Returns the list of categories, the current category, a list of questions, the total number of questions. 
    - It requires one optional question parameter `page` which defaults to 1 if not passed
- Sample: `curl http://127.0.0.1:5000/api/v1/questions`
```
{
   "categories":{
      "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
   },
   "current_category":null,
   "questions":[
      {
         "answer":"Maya Angelou",
         "category":4,
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
         "answer":"Edward Scissorhands",
         "category":5,
         "difficulty":3,
         "id":6,
         "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
         "answer":"Muhammad Ali",
         "category":4,
         "difficulty":1,
         "id":9,
         "question":"What boxer's original name is Cassius Clay?"
      },
      {
         "answer":"Brazil",
         "category":6,
         "difficulty":3,
         "id":10,
         "question":"Which is the only team to play in every soccer World Cup tournament?"
      },
      {
         "answer":"Uruguay",
         "category":6,
         "difficulty":4,
         "id":11,
         "question":"Which country won the first ever soccer World Cup in 1930?"
      },
      {
         "answer":"George Washington Carver",
         "category":4,
         "difficulty":2,
         "id":12,
         "question":"Who invented Peanut Butter?"
      },
      {
         "answer":"Lake Victoria",
         "category":3,
         "difficulty":2,
         "id":13,
         "question":"What is the largest lake in Africa?"
      },
      {
         "answer":"The Palace of Versailles",
         "category":3,
         "difficulty":3,
         "id":14,
         "question":"In which royal palace would you find the Hall of Mirrors?"
      },
      {
         "answer":"Agra",
         "category":3,
         "difficulty":2,
         "id":15,
         "question":"The Taj Mahal is located in which Indian city?"
      },
      {
         "answer":"Escher",
         "category":2,
         "difficulty":1,
         "id":16,
         "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }
   ],
   "success":true,
   "total_questions":19
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question with the given ID if it exists. 
    - Returns the question_id of the deleted question. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/v1/questions/20`
```
{
    "question_id": 20,
    "success": true
}
```
#### POST /api/v1/questions/
- General:
    - Creates a new question based on the payload consisting of answer, question, category and difficulty
    - Returns the created question and id of the question created 
    
- Sample: `curl http://127.0.0.1:5000/api/v1/questions? -X POST -H "Content-Type: application/json" -d '{"question": "This is a test question?", "answer": "Yes", "difficulty": 2, "category": 1}'`
```
{
  "id": 20, 
  "created_question": {
    "answer": "Yes", 
    "category": 1, 
    "difficulty": 2, 
    "id": 20, 
    "question": "This is a test question?"
  }, 
  "success": true
}
```

#### POST /api/v1/questions/search
- General:
    - Searches for questions based on the `searchTerm` provided in the request body. Returns a list of matching questions, the number of matching questions.
- Sample: `curl http://127.0.0.1:5000/api/v1/questions/search? -X POST -H "Content-Type: application/json" -d '{"searchTerm": "soccer World Cup in 1930"}'`
```
{
   "questions":[
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
   ],
   "success":true,
   "total_questions":1
}
```

#### POST /api/v1/quizzes
- General:
    - This endpoint is used to start the quiz. It takes list of ids of previous questions and quiz_category as json input in the request.
    - If we want to play quiz with all questions the quiz_category has to be passed as '0'.
    - If there are no previous_questions, pass an empty list/array.
    - Returns one question at a time and if no question is left, it returns a message saying that all questions have been played out
- Sample: `curl http://127.0.0.1:5000/api/v1/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [10], "quiz_category": {"id": 6}}'`
```
{
   "question":{
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
   },
   "success":true
}
```
- Sample when all questions are played out: `curl http://127.0.0.1:5000/api/v1/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3], "quiz_category": {"id": 5}}'`
```
{
   'message': 'All questions are played out'
   "success":true
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
