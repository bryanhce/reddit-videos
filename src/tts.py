import subprocess
from gtts import gTTS
from utils import parse_string
from moviepy.editor import *

def stitch_audio_files(n):
    '''
    Stitch aduio files generated together into a single file.
    '''
    audio_arr = []
    for i in range(n):
        # Load audio files
        audio_arr.append(AudioFileClip(f"../audio/{i}.mp3"))

    # Concatenate audio files
    combined = concatenate_audioclips(audio_arr)

    # Export the combined audio
    combined.write_audiofile("../audio/combined.mp3")



def generate_speech(texts):
    '''
    Creates mp3 files of speech from text and stores in audio folder.

    Parameters: 
    texts: array of tuples (title, content) where all elements
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
    
    stitch_audio_files(len(texts))

    print("Text-to-speech conversion complete")

def speed_up_tts():
    '''
    Speeds up the combined audio file by 1.5x speed.
    '''
    output_audio_file = "../audio/combined_sped_up.mp3"
    ffmpeg_command = ["ffmpeg", "-y", "-i", "../audio/combined.mp3", "-filter:a", "atempo=1.5", output_audio_file]
    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)