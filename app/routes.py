# Modules

from app import app
from flask import jsonify
from modules.ai import *

def rand():
    return("hello")

@app.route("/")
def index():
    return jsonify(message="hello!")


@app.route("/test")
def test():
    return jsonify(gemini_use())