## Project Structure


### Frontend


### Backend
- `run.py` : Main driver for Flask backend application
- `app/` : Application Package for Project Backend
    - `routes.py`
        : python file containing API endpoint routes
- `modules/` : This directory contains the logistics of using Gemini API.
    - `ai.py` : Temporary python file
- `venv/` : Configuration for Virtual Environment

## API Endpoints

## User (`/user`)

### Signing Up a New User (`/user/signup`)
URL: `/user/signup`\
Method: `POST`\
Request Body:
- `email`: (string) email of the user
- `password`: (string) password of the user

Response:
- `statusCode`: 
    - 200: OK
    - 400: Bad Request
- `message`: Has Useful Message (successfully created user / Error Name)


### Initializing a New Project (`/init`)
URL: `/init`\
Method: `POST`\
Request Body:
- `repoName`: (string) name of the repository
- `authKey`: (string) Access Key for the repository

Response:
- `message`: "successfully read the repo {repoName}"
- `geminiResponse`: Output from Gemini after training the repository

