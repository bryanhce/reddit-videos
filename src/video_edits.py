from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, VideoFileClip, AudioFileClip
import json

def create_word_level_JSON():
    model_size = "medium"
    model = WhisperModel(model_size)

    segments, info = model.transcribe("../audio/0.mp3", word_timestamps=True)
    segments = list(segments)  # The transcription will actually run here.
    for segment in segments:
        for word in segment.words:
            print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))

    wordlevel_info = []

    for segment in segments:
        for word in segment.words:
            wordlevel_info.append({'word':word.word,'start':word.start,'end':word.end})

    # print(wordlevel_info)

    # Store word-level timestamps into JSON file
    with open('../data.json', 'w') as f:
        json.dump(wordlevel_info, f, indent=4)

# Use Moviepy to create an audiogram with word-level highlights as they are spoken
def create_caption(
        textJSON,
        framesize,
        font,
        color,
        highlight_color,
        stroke_color,
        stroke_width,
    ):

    full_duration = textJSON['end'] - textJSON['start']

    word_clips = []
    xy_textclips_positions =[]

    x_pos = 0
    y_pos = 0
    line_width = 0  # Total width of words in the current line
    frame_width = framesize[0]
    frame_height = framesize[1]

    x_buffer = frame_width * 1 / 10

    max_line_width = frame_width - 2 * (x_buffer)

    fontsize = int(frame_height * 0.05) #7.5 percent of video height

    space_width = ""
    space_height = ""

    duration = textJSON['end'] - textJSON['start']

    word_clip = TextClip(
            textJSON['word'], 
            font=font,
            fontsize=fontsize, 
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            ).set_start(textJSON['start']).set_duration(full_duration)
            
    
    word_clip_space = TextClip(
            " ", 
            font=font,
            fontsize=fontsize,
            color=color
            ).set_start(textJSON['start']).set_duration(full_duration)
    
    word_width, word_height = word_clip.size
    space_width, space_height = word_clip_space.size
    if line_width + word_width+ space_width <= max_line_width:
        # Store info of each word_clip created
        xy_textclips_positions.append({
            "x_pos":x_pos,
            "y_pos": y_pos,
            "width" : word_width,
            "height" : word_height,
            "word": textJSON['word'],
            "start": textJSON['start'],
            "end": textJSON['end'],
            "duration": duration
        })

        word_clip = word_clip.set_position((x_pos, y_pos))
        word_clip_space = word_clip_space.set_position((x_pos+ word_width, y_pos))

        x_pos = x_pos + word_width+ space_width
        line_width = line_width+ word_width + space_width
    # TODO: try remove else block and running, should still work
    else:
        # Move to the next line
        x_pos = 0
        y_pos = y_pos + word_height + 10
        line_width = word_width + space_width

        # Store info of each word_clip created
        xy_textclips_positions.append({
            "x_pos":x_pos,
            "y_pos": y_pos,
            "width" : word_width,
            "height" : word_height,
            "word": textJSON['word'],
            "start": textJSON['start'],
            "end": textJSON['end'],
            "duration": duration
        })

        word_clip = word_clip.set_position((x_pos, y_pos))
        word_clip_space = word_clip_space.set_position((x_pos+ word_width , y_pos))
        x_pos = word_width + space_width

    word_clips.append(word_clip)
    word_clips.append(word_clip_space)

    for highlight_word in xy_textclips_positions:
        word_clip_highlight = TextClip(highlight_word['word'], font = font,fontsize=fontsize, color=highlight_color,stroke_color=stroke_color,stroke_width=stroke_width).set_start(highlight_word['start']).set_duration(highlight_word['duration'])
        word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
        word_clips.append(word_clip_highlight)

    return word_clips,xy_textclips_positions

def create_video_with_subtitles(
        base_url,
        font="Helvetica",
        color='white',
        highlight_color='yellow',
        stroke_color='black',
        stroke_width=1.5,
        ):
    
    with open('../data.json', 'r') as f:
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
                                highlight_color=highlight_color,
                                stroke_color=stroke_color,
                                stroke_width=stroke_width,
                                )
        max_width = 0
        max_height = 0

        for position in positions:
            x_pos, y_pos = position['x_pos'],position['y_pos']
            width, height = position['width'],position['height']

            max_width = max(max_width, x_pos + width)
            max_height = max(max_height, y_pos + height)

            color_clip = ColorClip(
                            size=(int(max_width * 1.1), int(max_height * 1.1)),
                            color=(64, 64, 64)
                            )
            # for adjusting text background transparency
            color_clip = color_clip.set_opacity(0)

            color_clip = color_clip.set_start(obj['start']).set_duration(obj['end'] - obj['start'])

        clip_to_overlay = CompositeVideoClip([color_clip]+ out_clips)
        clip_to_overlay = clip_to_overlay.set_position("center") # was previously 'bottom'

        all_linelevel_splits.append(clip_to_overlay)    

    final_video = CompositeVideoClip([input_video] + all_linelevel_splits)
    audio_clip = AudioFileClip("../audio/0.mp3")
    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(audio_clip)

    # TODO: trim the video to be same duration as audio

    # Save the final clip as a video file with the audio included
    final_video.write_videofile("../video/output.mp4", fps=24, codec="libx264", audio_codec="libmp3lame")

    print('Final video successfully generated')