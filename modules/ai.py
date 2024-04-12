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


#temperature = randomness of result
#token limit
#system instructions --> you are fucking albert einstein who can solve every fucking problem in the world (ㅈ나 빨아주기)
#embedding

#박이안 참고용:
    #gemini_use(input_text = text, input_image = image, input_file_API = fileAPI) --> output = response

def get_text(response):
    return response.text

#get_index
#get_token_count
#get_safety_rating_warnings
#get_finish_reason --> 1 = completed


def gemini_use(input_text = "give me 10 random numbers", input_image = None, input_file_API = None):
    if(input_file_API != None):
        return ''
    elif(input_image != None): #image exists --> use vision pro
        return ''
    else: #제일 간단한 text-to-text
        return gemini_text_input(input_text)
    
    return ''
            
  

def gemini_text_input(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response


print(get_text(gemini_use()))