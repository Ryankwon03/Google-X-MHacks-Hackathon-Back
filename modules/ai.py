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
import chromadb
import numpy as np
import pandas as pd
import google.generativeai as genai
import google.ai.generativelanguage as glm


# from dotenv import load_dotenv
# from os.path import join, dirname
from IPython.display import Markdown
from chromadb import Documents, EmbeddingFunction, Embeddings


# API Key 는 GOOGLE_API_KEY 로 쓰시면 됩니다
# dotenv_path = join(dirname(__file__),'.env')
# load_dotenv(dotenv_path)

# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# print(GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)



#model tuning --> AI 학습 시스템




#embedding --> 

#global variables
def declare_model(model_number = '1.5', ability = []):
    sys_instr_string = "Your names Dylan, an expert code commentator, specialized in providing clear and concise explanations for "
    for i in range(0,len(ability) - 1):
        sys_instr_string += f'{ability[i]}, '
    sys_instr_string += f'and {ability[len(ability) - 1]}. '
    sys_instr_string += "Your primary responsibility is to help others understand the functionality, structure, and logic of the code in the context of project. Within the context of project, you will explain the purpose of different variables, functions, and classes, as well as the interactions between them. Your comments will also highlight any edge cases, potential issues, or areas for improvement. Your goal is to make the code as accessible and understandable as possible to a wide range of developers, from beginners to experts."
    if(model_number == '1.0'):
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
    elif (model_number == 'image'): #FOR IMAGES
        model = genai.GenerativeModel(
            "gemini-pro-vision", #이미지
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                #max_output_tokens=2000,
                temperature=0.9
            )
        )
    elif (model_number == '1.5'):
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
    #print(response.text) Please, as I input the file directories and code, understand the relationships between the files and the code. Answer back in the format 'Received code in directory: ~/directory (with an empty line in the end)' for all the files in your project. 
    response = chat.send_message("Soon, I'll give you the file directory and its content (code) of a project that I'm currently working on. At the end, please provide me with a structural overview explaining the link between file names, functions names, etc.")
    print(response.text)
    return chat
    


def get_text(response):
    return response.text

def get_token_count(model, input_text): #chat history까지의 모든 token count를 구할수 있지만 필요 X
    return model.count_tokens(input_text)


def gemini_text(model, input_text = "What is your name?"):
    response = model.generate_content(input_text)
    return response.text

def gemini_image_and_text(model = 1.1, input_text = "", image = ""):
    response = model.generate_content([input_text, image])
    return response.text

def gemini_chat_send(chat, input_text_list = [('code.txt', 'return 0')]): #tuple_List (file_directory, content)
    input_text = ""
    for i in input_text_list:
        input_text += "In the directory (" + i[0] + "), the code is: " + i[1] + "\n\n\n"
    response = chat.send_message(input_text)
    print(response.text)
    return chat.history, response.text
    print(response.text)

        
    
def gemini_chat_return(chat, input_text = "Hello World"):
    response = chat.send_message(input_text) #Question the User Prompts
    return chat.history

def gemini_continue_asking(chat, training_data, user_chat_history, new_user_question,curBestContext):
    input_text = "The following is the code for my project: "
    # for i in training_data:
    #     input_text += (i + "\n")
    input_text += training_data

    input_text += "\n"

    input_text += "Here are the questions that I asked to you, along with your response, previously: "
    for chunk in user_chat_history:
        input_text += "My question was: " + chunk['user'] + ".\n"
        input_text += "Your response was: " + chunk['model'] + ".\n"

    # for i in range(0, len(user_chat_history), 2):
    input_text += "\n"

    input_text += "This is it for the background data about my project and our interaction! Can you start answering questions based on this informations?"

    initial_response = chat.send_message(input_text)
    user_question = f"Can you please answer this question for me: {new_user_question}"
    user_question += "\n"
    user_question += f"This can be some relevant information of my question, containing some explanations about a similar project: {curBestContext[0]}"
    print(user_question)
    print(initial_response.text)
    response = chat.send_message(user_question)
    # input_text += "\n"
    # input_text += ("Looking at the above, answer this question for me: " + new_user_question)
    # response = chat.send_message(input_text)
    return chat.history




#Embeddings
#text = "hello world"
#result = genai.embed_content(model = "models/embedding-001", context = text) --> embedding content
#content = ['text1', 'text2', 'text3']
#for embedding in result['embedding'] --> print(str(embedding)) --> values of embedded contents

#db = chroma db

    
#use this by doing db = create_chroma_db(documents, "googlecarsdatabase")



# #DEMO RUN OF THE ABOVE

# #model = declare_model() 
# #chat = text_init(model) #make a new chat with that model
# #asyncio.run(wait(1)) #time break를 줘서 코드 안터지게 관리 --> 솔직히 의미는 있을지는 불명
# #gemini_chat_send(chat, tuple_list) #나중에 tuple list 추가해서 데이터 전송


# DOCUMENT1 = "Operating the Climate Control System  Your Googlecar has a climate control system that allows you to adjust the temperature and airflow in the car. To operate the climate control system, use the buttons and knobs located on the center console.  Temperature: The temperature knob controls the temperature inside the car. Turn the knob clockwise to increase the temperature or counterclockwise to decrease the temperature. Airflow: The airflow knob controls the amount of airflow inside the car. Turn the knob clockwise to increase the airflow or counterclockwise to decrease the airflow. Fan speed: The fan speed knob controls the speed of the fan. Turn the knob clockwise to increase the fan speed or counterclockwise to decrease the fan speed. Mode: The mode button allows you to select the desired mode. The available modes are: Auto: The car will automatically adjust the temperature and airflow to maintain a comfortable level. Cool: The car will blow cool air into the car. Heat: The car will blow warm air into the car. Defrost: The car will blow warm air onto the windshield to defrost it."
# DOCUMENT2 = "Your Googlecar has a large touchscreen display that provides access to a variety of features, including navigation, entertainment, and climate control. To use the touchscreen display, simply touch the desired icon.  For example, you can touch the \"Navigation\" icon to get directions to your destination or touch the \"Music\" icon to play your favorite songs."
# DOCUMENT3 = "Shifting Gears Your Googlecar has an automatic transmission. To shift gears, simply move the shift lever to the desired position.  Park: This position is used when you are parked. The wheels are locked and the car cannot move. Reverse: This position is used to back up. Neutral: This position is used when you are stopped at a light or in traffic. The car is not in gear and will not move unless you press the gas pedal. Drive: This position is used to drive forward. Low: This position is used for driving in snow or other slippery conditions."

# documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3] #여기에 들어가는 query 는 유저가 넣은 query
# #박이안이 이렇게 추가해서 쓰는거
# db = create_chroma_db(documents, "googlecarsdatabase")
# passage = get_relavant_passage("phone screen", db)
# print(passage)


# query = "How do you use the touchscreen in the Google car?"
# prompt = make_prompt(query, passage)
# print(prompt)

