import subprocess
from gtts import gTTS
from utils import parse_string, remove_repeated_punctuations

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

        # parse the string to remove unwanted complications and errors
        final_str = parse_string(raw_str)

        # create a gTTS object
        tts = gTTS(
                text = final_str,
                lang='en',
                tld='com.au' # change accent
            )
        tts.save('../audio/' + str(i) + ".mp3")

    print("Text-to-speech conversion complete")

def speed_up_tts():
    output_audio_file = "../audio/0_sped_up.mp3"
    ffmpeg_command = ["ffmpeg", "-y", "-i", "../audio/0.mp3", "-filter:a", "atempo=1.5", output_audio_file]
    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)