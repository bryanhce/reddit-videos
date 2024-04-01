import os
import re

def remove_punctuation(word):
    '''
    Remove trailing punctuation and white spaces
    from a single string.
    '''
    text = word.strip()
    # Matches leading or trailing punctuation (\W matches non-word characters)
    punctuation_pattern = r'^\W+|\W+$'  
    clean_text = re.sub(punctuation_pattern, '', text)
    return clean_text

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

def has_tuples(arr):
    '''
    Returns a boolean if array contains a tuple
    '''
    for item in arr:
        if isinstance(item, tuple):
            return True
    return False

def concat_content_to_str(content):
    '''
    Content take on 2 forms
    1. [("s1", "s2"), ("s3", "s4")]
    2. ["s1", "s2", "s3", "s4"]

    Return single string.
    E.g. "s1 s2 s3 s4"
    '''
    if has_tuples(content):
        arr = []
        for c in content:
            title, subtitle = c
            arr.append(title + ' ' + subtitle)
        return ' '.join(arr)
    else:
        return ' '.join(content)

def clean_up():
    '''
    Delete mp3 files in audio
    '''
    folder_path = "../audio"
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            os.remove(os.path.join(folder_path, file))