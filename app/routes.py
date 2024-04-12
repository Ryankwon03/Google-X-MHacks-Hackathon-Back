# Modules

from app import app
from flask import jsonify
from modules.ai import *

def rand():
    return("hello")

@app.route("/")
def index():
    return jsonify(message="hello!")

@app.route("/realRandom", methods = ["GET"])
def realRandom():
    return jsonify(message=randomGen(3))
