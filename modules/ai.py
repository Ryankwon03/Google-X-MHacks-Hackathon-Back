# Modules
import os
import asyncio
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
global model
global chat

model = genai.GenerativeModel()
chat = model.start_chat()

#global variables
def declare_model(model_number = 1.0, ability = []):
    sys_instr_string = "You are an full-stack developer at Google who is fluent at programming and utilizing the following tools: "
    for i in ability: #ability = list of abilities
        sys_instr_string += (i + ", ")

    if(model_number == 1.0):
        model = genai.GenerativeModel(
            "models/gemini-1.0-pro", #짧게 많이
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                temperature=0.9,
            )
        )
    elif (model_number == 1.5):
        model = genai.GenerativeModel(
            "models/gemini-1.5-pro-latest", #한번에 많은양
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                temperature=0.9,
            )
        )
    
    chat = model.start_chat()



def get_text(response):
    return response.text

def get_token_count(input_text): #chat history까지의 모든 token count를 구할수 있지만 필요 X
    return model.count_tokens(input_text)


def gemini_text(input_text):
    
    response = model.generate_content(input_text)
    return response

def gemini_chat_send(input_text_list = ""):
    chat.send_message("hi my name is ryan")
    chat.send_message("what's ur name again?")


def gemini_chat_return(input_text_list = ""):
    # response = chat.send_message("this is my friend sean.")
    # response = chat.send_message("whos the guy right next to you?")
    # response = chat.send_message("bye i have to go now")
    return chat.history



declare_model()
gemini_chat_send()
print(gemini_chat_return(''))