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
global model

model = genai.GenerativeModel()

#global variables
def declare_model(model_number = 1.0, ability = []):
    sys_instr_string = "You are an full-stack developer at Google who is fluent at programming and utilizing the following tools: " + ability
    if(model_number == 1.0):
        model = genai.GenerativeModel(
            "models/gemini-1.0-pro", #짧게 많이
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                max_output_tokens=4000, #늘리기
                temperature=0.9,
            )
        )
    elif (model_number == 1.5):
        model = genai.GenerativeModel(
            "models/gemini-1.5-pro-latest", #한번에 많은양
            system_instruction = sys_instr_string,
            generation_config=genai.GenerationConfig(
                max_output_tokens=4000, #늘리기
                temperature=0.9,
            )
        )



def get_text(response):
    return response.text

def get_token_count(input_text): #chat history까지의 모든 token count를 구할수 있지만 필요 X
    return model.count_tokens(input_text)




def gemini_use(input_text = "give me 10 random numbers", model_number = 1.0, ability = []):
    declare_model(model_number, ability)

    
    return gemini_chat(input_text)
    

def gemini_model_1(input_text):
    
    response = model.generate_content(input_text)
    return response

def gemini_chat(input_text_list = "what's ur name"):
    chat = model.start_chat()
    response = chat.send_message("hi my name is ryan")
    response = chat.send_message("what's ur name again?")
    response = chat.send_message("bye i have to go now")
    return chat.history
    

print(gemini_chat())