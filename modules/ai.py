# Modules
import os
from os.path import join, dirname
from dotenv import load_dotenv
import PIL.Image
import google.generativeai as genai

# API Key 는 GOOGLE_API_KEY 로 쓰시면 됩니다
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


#model tuning --> AI 학습 시스템




#embedding --> 

#global variables
model = genai.GenerativeModel( #나중에 바꾸기
    "models/gemini-1.5-pro-latest",
    system_instruction = "YOU ARE ALBERT EINSTEIN",
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,
        temperature=0.9,
    )
)



def get_text(response):
    return response.text

def get_token_count(input_text): #chat history까지의 모든 token count를 구할수 있지만 필요 X
    return model.count_tokens(input_text)




def gemini_use(input_text = "give me 10 random numbers"):
    return gemini_text_input(input_text)
    

def gemini_text_input(input_text):
    response = model.generate_content(input_text)
    return response

def gemini_chat(input_text_list = "what's ur name"):
    chat = model.start_chat()
    response = chat.send_message("hi my name is ryan")
    return response
    

print(get_text(gemini_chat()))