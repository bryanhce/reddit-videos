from video_edits import create_video_with_subtitles
from reddit import get_reddit_posts
from tts import generate_speech
from utils import clean_up

if __name__ == "__main__":
    # Parameters to change with each video
    subReddit = 'LifeProTips'
    nPosts = 1
    base_url = '../video/base_2.mp4'
    font = 'Liberation-Serif-Bold'
    color = 'red'
    highlight_color = 'red'
    stroke_color = 'black'
    stroke_width = 1.3

    content = get_reddit_posts(subReddit, nPosts)
    generate_speech(content) # TODO edit if changing structure
    create_video_with_subtitles(
        base_url,
        font,
        color,
        highlight_color,
        stroke_color,
        stroke_width
    )
    # clean_up()