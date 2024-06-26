# 2024 Google x Mhacks Hackathon Backend
**by Ian Park, Sungmo Kwon**
## Main Features
- Provides basic CRUD for managing users and projects
- Utilizes embedding to filter out best resources for each projects, which includes queries, context, etc.
- Adapt Gemini 1.5's API calls in a way that amplifies its strength


## Backend Project Structure
- `run.py` : Main driver for Flask backend application
- `app/` : Application Package for Project Backend
    - `routes.py` : python file containing API endpoint routes
    - `firebase.py` : Functions that helps with using Firebase features, especially Realtime Database and FireStore Database
    - `gitReader.py` : Functions that helps with reading GitHub repositories using PyGitHub Library

- `modules/` : This directory contains the logistics of using Gemini API.
    - `ai.py` : AI Library for this app
- `venv/` : Configuration for Virtual Environment

# API Endpoints

## User (`/user`)

### Signing In a User (`/user/signin`)
URL: `/user/signin`\
Method: `POST`\
Request Body:
- `email`: (string) email of the user
- `firstName`: First Name of the user
- `lastName`: Last Name of the user

Response:
- `isNew`: (boolean) true if the user is newly created in the Database
- `userid`: id of the user signed in
- `hasProjects`: (boolean) true if the user has AT LEAST ONE project


## Project (`/project`)

### Initializing a New Project (`/project/init`)
URL: `/project/init`\
Method: `POST`\
Request Body:
- `repoName`: (string) name of the repository
- `authKey`: (string) Access Key for the repository
- `userid`: (string) userid
- `projectName`: (string) Project Name
- `techTags`: (list) list of technical Tags

Response:
- `message`: "successfully read the repo {repoName}"
- `geminiResponse`: Output from Gemini after training the repository


### Sending a Chat to Initialized Project (`/project/askQuestion`)
URL: `/project/askQuestion`\
Method: `POST`\
Request Body:
- `userid`: userid
- `projectid`: id of the project
- `query`: text input of the question of the user

Response:
- `geminiAnswer`: Markdown Format of Gemini's answer

### Retrieving Projects as List (`/project/loadProjects`)
URL: `/project/loadProjects`\
Method: `GET`\
Request Parameters:
- `userid`: userid

Response:
- `projectList`: List of dictionary. Each index contains two pairs of key & value. Keys include:
    - `projectid` : id of the project
    - `projectName` : name of the project
* Example: responseObj[0]['projectid'] = id of the first project (each dictionary entries are sorted by creation time)

### Getting Previous Chat History (`/project/getChatHistory/<userid>/<projectid>`)
URL: `/project/getChatHistory/<userid>/<projectid>`\
Method: `GET`\
Request Parameters:
- `userid`: userid
- `projectid`: id of the project


Response:
- `user_chat_history`: List of dictionary. Each index contains two paris of key & value. Keys include:
    - `user`: Question that user asked
    - `model`: Answer from Gemini
    * Obviously, indexes are sorted in chronological order
* Example: responseObj[0]['user'] contains the first question of the user, and responseObj[0]['model'] contains the answer to that question.

### Deleting a Project from a user (`/project/deleteProject`)
URL: `/project/deleteProject`\
Method: `DELETE`\
Request Parameters:
- `userid`: userid
- `projectid`: projectid

Response:
- `statusCode` : 200 if successfully Deleted
- `message` : "delte!!"