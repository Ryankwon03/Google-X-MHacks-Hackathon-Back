# Modules
import os
import asyncio
from os.path import join, dirname
from dotenv import load_dotenv
from app import GOOGLE_API_KEY
# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

import PIL.Image
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession


# API Key 는 GOOGLE_API_KEY 로 쓰시면 됩니다
# dotenv_path = join(dirname(__file__),'.env')
# load_dotenv(dotenv_path)

# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# print(GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)



#model tuning --> AI 학습 시스템




#embedding --> 

#global variables
def declare_model(model_number = 1.5, ability = []):
    sys_instr_string = "You are an Senior full-stack developer at Google who did a PhD at MIT named Dylan and is fluent at programming and utilizing the following tools: "
    for i in ability: #ability = list of abilities
        sys_instr_string += (i + ", ")
    
    if(model_number == 1.0):
        #project_id = "PROJECT_ID"
        #location = "us-central1"
        #vertexai.init(project = project_id, location = location)
        model = genai.GenerativeModel(
            "models/gemini-1.0-pro", #짧게 많이
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                #max_output_tokens=2000,
                temperature=0.9
            )
        ) 
    elif (model_number == 1.5):
        model = genai.GenerativeModel(
            "models/gemini-1.5-pro-latest", #한번에 많은양
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                #max_output_tokens=2000,
                temperature=0.9
            )
        )
    return model

def text_init(model):
    chat = model.start_chat()
    #response = chat.send_message("Hi, what's your name and what do you do for living?")
    #print(response.text)
    response = chat.send_message("Soon, I'll give you the file directory and its content (code) of a project that I'm currently working on. Please, as I input the file directories and code, understand the relationships between the files and the code. Answer back in the format 'Received code in directory: ~/directory (with an empty line in the end)' for all the files in your project.")
    print(response.text)
    return chat
    


def get_text(response):
    return response.text

def get_token_count(model, input_text): #chat history까지의 모든 token count를 구할수 있지만 필요 X
    return model.count_tokens(input_text)


def gemini_text(model, input_text = "wait I need to go real quick, so I'll send you this later."):
    response = model.generate_content(input_text)
    return response.text

def gemini_chat_send(chat, input_text_list = [('code.txt', 'return 0')]): #tuple_List (file_directory, content)
    input_text = ""
    for i in input_text_list:
        input_text += "In the directory (" + i[0] + "), the code is: " + i[1] + "\n\n\n"
    response = chat.send_message(input_text)
    return response.text
    print(response.text)

        
    
def gemini_chat_return(chat, input_text_list = "Hello World"):
    response = chat.send_message(input_text_list) #Question the User Prompts
    return chat.history

async def wait(x):
    await asyncio.sleep(x)

#print(gemini_text())
#gemini_chat_return("User Question")

# model = declare_model()
# chat = text_init(model) #make a new chat with that model
# asyncio.run(wait(5)) #time break를 줘서 코드 안터지게 관리 --> 솔직히 의미는 있을지는 불명
# gemini_chat_send(chat, tuple_list) #나중에 tuple list 추가해서 데이터 전송


