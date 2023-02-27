# Full Stack API Final Project


## Full Stack Trivia

This is an API that provide endpoints for Questions in the Categories of Science, Arts, Geography, History and Entertainment.



## Local Requirement
Requires Python 3.6 or Later

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

##### To Create a virtual Environment

```
python -m venv venv
```

##### To Start the environment for Windows Users
```using git bash
source venv/Script/activate
```
#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```git bash (For Windows Users)
pip install -r requirements.txt
```

## Database Setup

#### Running Postgresql server on windows
To `start` your server use
`  pg_ctl -D "c:\Program Files\PostgreSQL\[Your PostgreSQL Version]\data" start
`
>Example (using git bash)
```git bash
 pg_ctl -D "c:\Program Files\PostgreSQL\13\data" start
```

To `Stop` your server use
`  pg_ctl -D "c:\Program Files\PostgreSQL\[Your PostgreSQL Version]\data" stop
`
>Example (using git bash)
```bash
 pg_ctl -D "c:\Program Files\PostgreSQL\13\data" stop
```
 
 Create a database called `trivia` using [psql](https://www.postgresql.org/docs/9.2/app-psql.html)

 ```
 CREATE DATABASE trivia;
 ```

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal(For Windows Users) run:
`psql -f database_file -U user database_name`

```bash
psql -f trivia.psql - U postgres trivia 
```
## Running the server

From within the `backend` directory first en sure you are working using your created virtual environment.

To run the server, execute:

``` **bash**
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
If you are on a windows machine:

``` **cmd**
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

The server will be running on  [http://localhost:5000](http://localhost:5000) .

## Setting up the Frontend

> Note: The frontend is design to work with endpoints in the backend -> [Flask-based Backend](../backend). It is recommended you set up the backend first, using Postman or curl to test the backend first, update the endpoints in the frontend, and every thing will work perfectly.

### Installing Frontend Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```


## Required Tasks

## Running Your Frontend

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

```bash
npm start
```

## Endpoints

### GET '/categories'
- Gets a dictionary of categories from the Category database in which the keys are the ids and the value is the corresponding category in string format.
- Request: None
- Response: An object  that contains an object of id: category_string.

>Example: `curl http://127.0.0.1:5000/categories`
```
{
	'1' : "Science",
	'2' : "Art",
	'3' : "Geography",
	'4' : "History",
	'5' : "Entertainment",
	'6' : "Sports"
}
```

### GET '/questions'
- Gets a dictionary of questions, paginated in groups of 10. 
- Response JSON object of categories, questions dictionary with answer, category, difficulty, id and question.

>E.g: `curl http://127.0.0.1:5000/questions`
```
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": [],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 1,
            "difficulty": 5,
            "id": 24,
            "question": "The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?"
        }
        ... # remaining questions on the page 
    ],
    "success": true,
    "total_questions": 40
}
```

### DELETE '/questions/<int:question_id>'
- Deletes selected question by id
- Response: 200 if the question is successfully deleted from the database.
- Response: 404 if the question did not exist in the database
- Response: JSON object of deleted id, remaining questions, and length of total questions

>Example: `curl -X DELETE http://127.0.0.1:5000/question/14`
```
{
    "deleted": 14,
    "questions": [
        {
            "answer": "The Earth and the Sun",
            "category": 1,
            "difficulty": 5,
            "id": 14,
            "question": "The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?"
        }    
        ... # the remaining on the page 
    ],
    "success": true,
    "total_questions": 40
}
```

### POST '/questions'
- Creates a new question posted from the `add` page of the frontend.
- Fields are: answer, question, difficulty and category. 
- Response a success value and ID of the question.
- If search field is present will return matching expressions

>Example (Create a new entry):
`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?", "answer":"The Earth and the Sun", "category":"1", "difficulty":"5"}'`
```
{
... # show questions
  "success": true, 
  "total_questions": 35
}

E.g:
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Astronomical Unit (AU)"}'

{
  "questions": [
    {
      "answer": "The Earth and the Sun",
      "question": "The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?",
      "category": 1, 
      "difficulty": 5, 
      "id": 34 
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### GET '/categories/<category_id>/questions'
- Returns JSON response of current_category, and the questions pertaining to that category

>E.g: `curl http://127.0.0.1:5000/categories/2/questions`
```
{
 "current_category": {
    "id": 2, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Earth and the Sun", 
      "category": 1, 
      "difficulty": 5, 
      "id": 20, 
      "question": "The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?"
    }, 
   ... # omitted for brevity
  ], 
  "success": true, 
  "total_questions": 40
}
```


### POST '/quiz'
- Generates a quiz based on category  user chooses.
- Response: a random question is returned

E.g: `curl http://127.0.0.1:5000/quiz -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Science","id":1}, "previous_questions":[] }'`
```
{
  "question": {
    "answer": "The Earth and the Sun", 
    "category": 1, 
    "difficulty": 5, 
    "id": 18, 
    "question": "The Astronomical Unit (AU) is a unit of measurement based on the average distance between what two bodies?"
  }, 
  "success": true
}
```

## Error Handling

- Response: these error types  will return when the request fails
	- 400: bad bequest
	- 404: resource not found
	- 405: method not found
	- 422: unprocessable
	- 500: internal server error
E.g 
```
{
	"success": False,
	"error": 500,
	"message": "internal server error"
}
```
