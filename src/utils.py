import os
import re

def remove_repeated_punctuations(text):
    return re.sub(r'([^\w\s])\1+', r'\1', text)

def ensure_single_space(text):
    words = text.split()   
    result_string = ' '.join(words)

    return result_string

# TODO: use a LLM to sort out grammatical errors and typos
def parse_string(text):
    formatted_string = remove_repeated_punctuations(text)
    formatted_string = ensure_single_space(formatted_string)
    formatted_string = formatted_string.capitalize()

    return formatted_string

def clean_up():
    '''
    Delete mp3 files in audio
    '''
    folder_path = "../audio"
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            os.remove(os.path.join(folder_path, file))