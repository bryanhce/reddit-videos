from gtts import gTTS
from utils import remove_repeated_punctuations

def generate_speech(texts):
    '''
    Creates mp3 files of speech from text and stores in audio folder.

    Parameters: 
    texts : array of tuples (title, content) where all elements
            are type String
    
    Returns:
    No output
    '''
    for i in range(len(texts)):
        # concat title and content into 1 string
        title, content = texts[i]
        raw_str = title + content

        # parse the string to remove unwanted complications
        final_str = remove_repeated_punctuations(raw_str)

        # create a gTTS object
        tts = gTTS(
                text = final_str,
                lang='en',
                tld='com.au' # change accent
            )
        tts.save('../audio/' + str(i) + ".mp3")

    print("Text-to-speech conversion complete")