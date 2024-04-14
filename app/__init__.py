from flask import Flask
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

dotenv_path = join('.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")   
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")
# print(GOOGLE_API_KEY)

from app import routes
from app import user