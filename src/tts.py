import subprocess
from gtts import gTTS
from utils import *
from moviepy.editor import *

def stitch_audio_files(n):
    '''
    DEPRECATED

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
    texts: takes 2 forms    
        1. [("s1", "s2"), ("s3", "s4")]
        2. ["s1", "s2", "s3", "s4"]
    
    Returns:
    No output
    '''        
    raw_str = parse_content_to_str(texts)

    # parse the string to remove unwanted complications and errors
    final_str = parse_string(raw_str)

    # create a gTTS object
    tts = gTTS(
            text = final_str,
            lang='en',
            tld='com.au' # change accent
        )
    # as parse_content_to_str func returns a 
    # single string, there will only be 1 audio file
    tts.save('../audio/0.mp3')

    print("Text-to-speech conversion complete")

def speed_up_tts():
    '''
    Speeds up the combined audio file by 1.3x speed.
    '''
    output_audio_file = "../audio/0_sped_up.mp3"
    ffmpeg_command = ["ffmpeg", "-y", "-i", "../audio/0.mp3", "-filter:a", "atempo=1.3", output_audio_file]
    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)