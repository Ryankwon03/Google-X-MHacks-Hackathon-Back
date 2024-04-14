import chromadb
from app import myChromaDB
import google.generativeai as genai
import google.ai.generativelanguage as glm

class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        model = 'models/embedding-001'
        title = "Custom Query"
        return genai.embed_content(model=model, content = input, task_type="retrieval_document",title=title)["embedding"]


questionQueriesFile = open("questionnaire.txt","r")
myQuestionQueries = []
for line in questionQueriesFile:
    print(line)
    myQuestionQueries.append(line)

for i, d in enumerate(myQuestionQueries):
    myChromaDB.add(
        documents = [d],
        ids = [str(i)]
    )