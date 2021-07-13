# Full Stack API Final Project


## Introduction

This project is a web app of trivia game. Users can display questions with different categories, add new questions and play the game. This project is a part of 
the Fullstack Nanodegree by Udacity. I worked on buliding APIs, test APIs and write API Documentation. 


## Getting Started

## Pre-requisites and Local Development

In this project, developres need Python3, pip and node installed on their local machines.

### 1. Backend 

**Install all required packages that are included in the requirements file.** 
```
cd backend
pip install -r requirements.txt
```
**Run the following commands to start the flask application**
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
### 1. Frontend 

**Installing project dependencies for frontend**
This project depends on Nodejs and Node Package Manager (NPM) ensure you already intall it from https://nodejs.com/en/download. 
NPM Relies on the package.json file located in the frontend directory of this repository. To install NPM run `
npm install` on terminal.

**Run the following commands to start the client**
```
cd frontend
npm start
```
Then Open http://localhost:3000 to view it in the browser.

## Tests

To tests move to `./backend` then run 
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Expected Errors and Messages


### Endpoints
Errors are returned as JSON objects in the following format:
```
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```
This API will return four error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
405: Method not allowed

### GET /categories

General:
Returns an object with a single key, categories, that contains an object of id: category_string key:value pairs.
Sample: curl http://127.0.0.1:5000/categories
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /questions or GET '/questions?page=${integer}'

General:
Returns a list of questions objects, success value, categories, current_category,and total number of questions
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/questions

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "ALL", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
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
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 17
}
```
### GET /categories/${id}/questions

General:
Returns a list of questions objects for specific category, success value, current_category,and total number of questions
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/categories/2/questions

```
{
  "currentCategory": [
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "success": true, 
  "totalQuestions": 3
}
```

### DELETE /questions/${id}

General:
Deletes the question of the given ID if it exists. Returns the id of the deleted book and success value.
Sample: curl -X DELETE http://127.0.0.1:5000/questions/18

```
{
  "deleted": 18, 
  "success": true
}
```

### POST /questions

General:
Based on what you send if you send searsh term that will return all the questions that have searsh term, categories, current_category, success value othrewis it creates a new questions using the submitted question, answer, difficulty and category. Returns success value.
Sample for searsh: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What is"}'
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "ALL", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Mercury", 
      "category": 1, 
      "difficulty": 1, 
      "id": 47, 
      "question": "What is the nearest planet to the sun?"
    }
  ], 
  "success": true, 
  "totalQuestions": 3
}
```
Sample for create: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the nearest planet to the sun?", "answer":"Mercury", "difficulty":"1" , "category":"1" }'

```
{
  "success": true
}
```

## Deployment N/A
## Authors
This project is provided by Udacity to practice API development and documentation for Nanodegree program.
Project Link : https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter
AMANI ALSHAMI . 



