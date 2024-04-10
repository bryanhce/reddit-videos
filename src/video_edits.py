from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, VideoFileClip, AudioFileClip, ImageClip
import json
from config import SPEED_MULTIPLIER
from utils import remove_punctuation

def get_audio_end_timing(audio_file_path):
    audio = AudioFileClip(audio_file_path)
    end_timing = audio.duration
    return end_timing

def create_word_level_JSON(body):
    '''
    Returns json that contains information on the duration
    each word should be displayed on the video.

    Parameters: Note param not currently in use
    body: Dictionary of thumbnail text and content which is an
    array of of tuple or string

    Returns:
    Creates a json that contains {word/phase, start, end}
    '''
    model_size = "medium"
    model = WhisperModel(model_size)

    offset = get_audio_end_timing("/code/audio/thumbnail_sped_up.mp3")

    segments, info = model.transcribe("/code/audio/content.mp3", word_timestamps=True)
    segments = list(segments)  # The transcription will actually run here.

    wordlevel_info = []

    # TODO: currently we are using text generated from the transcription of audio
    # which can contain errors, we need to figure out a way to get consistency 
    # of the word using content param
    for segment in segments:
        for word in segment.words:
            word_text = remove_punctuation(word.word)
            start = word.start * (1 / SPEED_MULTIPLIER) + offset # speeding up the subtitle display
            end = word.end * (1 / SPEED_MULTIPLIER) + offset
            wordlevel_info.append({
                                'word' : word_text, 
                                'start' : start, 
                                'end' : end
                                })
            # print("[%.2fs -> %.2fs] %s" % (start, end, word_text))

    # Store word-level timestamps into JSON file
    with open('/code/data.json', 'w') as f:
        json.dump(wordlevel_info, f, indent=4)

# Use Moviepy to create an audiogram with word-level highlights as they are spoken
def create_caption(
        textJSON,
        framesize,
        font,
        color,
        stroke_color,
        stroke_width,
    ):

    xy_textclips_positions =[]

    x_pos = 0
    y_pos = 0
    frame_height = framesize[1]

    font_size = int(frame_height * 0.045) # to change font size

    duration = textJSON['end'] - textJSON['start']

    word_clip = TextClip(
            textJSON['word'], 
            font=font,
            fontsize=font_size, 
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            ).set_start(textJSON['start']).set_duration(duration)
    
    word_width, word_height = word_clip.size

    xy_textclips_positions.append({
            "x_pos" : x_pos,
            "y_pos" : y_pos,
            "width" : word_width,
            "height" : word_height,
            "word" : textJSON['word'],
            "start" : textJSON['start'],
            "end" : textJSON['end'],
            "duration": duration
        })
    word_clip = word_clip.set_position((x_pos, y_pos))

    return [word_clip], xy_textclips_positions

def create_thumbnail():
    # Path to your image file
    image_path = "/code/image/output_image.png"

    # Load the image and create an ImageClip
    duration = get_audio_end_timing("/code/audio/thumbnail_sped_up.mp3")
    image_clip = ImageClip(image_path, duration=duration)

    # Position the image in the center of the video frame
    image_clip = image_clip.set_position((0.175, 0.2), relative=True)
    return image_clip

def create_video_with_subtitles(
        base_url,
        font,
        color,
        stroke_color,
        stroke_width,
        ):
    
    with open('/code/data.json', 'r') as f:
        wordlevel_info = json.load(f)

    input_video = VideoFileClip(base_url)
    frame_size = input_video.size

    all_linelevel_splits = []

    for obj in wordlevel_info:
        out_clips, positions = create_caption(
                                obj, 
                                frame_size,
                                font=font,
                                color=color,
                                stroke_color=stroke_color,
                                stroke_width=stroke_width,
                                )
        max_width = 0
        max_height = 0

        for position in positions:
            x_pos, y_pos = position['x_pos'], position['y_pos']
            width, height = position['width'], position['height']

            max_width = max(max_width, x_pos + width)
            max_height = max(max_height, y_pos + height)

            color_clip = ColorClip(
                            size=(max_width , max_height),
                            color=(64, 64, 64)
                            )
            # for adjusting text background transparency
            color_clip = color_clip.set_opacity(0)

            color_clip = color_clip.set_start(obj['start']).set_duration(position['duration'])

        clip_to_overlay = CompositeVideoClip([color_clip] + out_clips)
        clip_to_overlay = clip_to_overlay.set_position("center")

        all_linelevel_splits.append(clip_to_overlay)   

    # Path to audio file
    audio_clip = AudioFileClip("/code/audio/combined.mp3")

    image_clip = create_thumbnail()

    final_video = CompositeVideoClip([input_video, image_clip.set_start(0)] + all_linelevel_splits)

    # trim the video to be same duration as audio
    final_video = final_video.subclip(0, audio_clip.duration)

    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(audio_clip)

    # Save the final clip as a video file with the audio included
    final_video.write_videofile("/code/video/output.mp4", fps=24, codec="libx264", audio_codec="libmp3lame")

    print('Final video successfully generated')