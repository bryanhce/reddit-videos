import subprocess
from gtts import gTTS
from utils import *
from moviepy.editor import *
from config import SPEED_MULTIPLIER

def generate_audio_files(body):
    '''
    Creates mp3 files, normal speed and sped up speed,
    of speech from text and stores in audio folder.

    Parameters: 
    body: dictionary of thumbnail and content, 
    content takes 2 forms    
        1. [("s1", "s2"), ("s3", "s4")]
        2. ["s1", "s2", "s3", "s4"]
    
    Returns:
    No output
    '''
    THUMBNAIL_STR = 'thumbnail'
    CONTENT_STR = 'content' 
    # TODO might be able to use async here
    parsed_thumbnail = parse_string(body[THUMBNAIL_STR])
    parsed_content = parse_string(concat_content_to_str(body[CONTENT_STR]))
    generate_speech(parsed_thumbnail, THUMBNAIL_STR)
    generate_speech(parsed_content, CONTENT_STR)
    speed_up_tts(THUMBNAIL_STR)
    speed_up_tts(CONTENT_STR)

    sped_up_audio_files_to_stitch = [THUMBNAIL_STR, CONTENT_STR]
    stitch_audio_files(sped_up_audio_files_to_stitch)

    print("Audio files generated!")

def stitch_audio_files(arr_filenames):
    '''
    Stitch sped up aduio files generated together into a single file.

    Parameters:
    arr_filenames: array of file names to stitch

    Returns:
    No output but store mp3 in audio folder as combined.mp3 
    '''
    audio_arr = []
    for i in range(len(arr_filenames)):
        # Load audio files
        audio_arr.append(AudioFileClip(f"/code/audio/{arr_filenames[i]}_sped_up.mp3"))

    # Concatenate audio files
    combined = concatenate_audioclips(audio_arr)

    # Export the combined audio
    combined.write_audiofile("/code/audio/combined.mp3")

def generate_speech(string, name):
    '''
    Creates mp3 file of speech from text.

    Parameters: 
    string : string to be converted into audio
    name: name of the audio file created
    
    Returns:
    No output but stores mp3 in audio folder.
    '''        
    tts = gTTS(
            text = string,
            lang='en',
            tld='com.au' # edit to change accent
        )

    tts.save(f'/code/audio/{name}.mp3')

def speed_up_tts(name):
    '''
    Speeds up the combined audio file by certain speed.

    Parameters:
    name: name of the file to be sped up

    Returns:
    No returns but saves new sped up audio to audio folder.
    '''
    output_audio_file = f"/code/audio/{name}_sped_up.mp3"
    ffmpeg_command = ["ffmpeg", "-y", "-i", f"/code/audio/{name}.mp3",\
                       "-filter:a", f"atempo={SPEED_MULTIPLIER}", output_audio_file]
    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)