Markdown Live Preview
Reset
Copy

- geminiResponse: Output from Gemini after training the repository


Project Structure
Frontend
Backend
run.py : Main driver for Flask backend application
app/ : Application Package for Project Backend
routes.py : python file containing API endpoint routes
modules/ : This directory contains the logistics of using Gemini API.
ai.py : Temporary python file
venv/ : Configuration for Virtual Environment
API Endpoints
Initializing a New Project
URL: /init
Method: POST
Request Body:

repoName: (string) name of the repository
AuthKey: (string) Access Key for the repository
Response:

Message: "successfully read the repo {repoName}"
geminiResponse: Output from Gemini after training the repository
