from gtts import gTTS

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
        final_str = title + content

        # create a gTTS object
        tts = gTTS(
                text = final_str,
                lang='en',
                tld='com.au' # change accent
            )
        tts.save('../audio/' + str(i) + ".mp3")

    print("Text-to-speech conversion complete")