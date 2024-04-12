# Modules
from app import GOOGLE_API_KEY
import os
import PIL.Image
import google.generativeai as genai

# API Key 는 GOOGLE_API_KEY 로 쓰시면 됩니다

genai.configure(api_key=GOOGLE_API_KEY)


#then run the function

#model.generate_content([text, image]) --> for gemini-pro-vision


#temperature = randomness of result
#token limit


#file API = audio file --> only lasts for 2 days, and upload whatever thing we want and bring that up later


#system instructions
#embedding

def gemini_use(input_text = "what's ur name", input_image = None, input_file_API = None):
    if(input_file_API != None):
        return ''
    elif(input_image != None): #image exists --> use vision pro
        return ''
    else: #제일 간단한 text-to-text
        return gemini_text_input(input_file_API)
    
    return ''
            
  

def gemini_text_input(input_text):
    genai.GenerativeModel('gemini-pro')
    return(genai.generate_text(input_text))


