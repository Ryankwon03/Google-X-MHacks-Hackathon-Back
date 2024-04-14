from flask import Flask
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv
import google.generativeai as genai
import google.ai.generativelanguage as glm

import chromadb

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

dotenv_path = join('.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")   
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")

class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        model = 'models/embedding-001'
        title = "Custom Query"
        return genai.embed_content(model=model, content = input, task_type="retrieval_document",title=title)["embedding"]

myChromaDB = chromadb.Client().create_collection(name="myCodingCollection", embedding_function=GeminiEmbeddingFunction())

from app import routes
from app import user