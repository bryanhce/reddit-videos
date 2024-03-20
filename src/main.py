from video_edits import *
from reddit import get_reddit_posts
from tts import generate_speech
from utils import clean_up

if __name__ == "__main__":
    # Parameters to change with each video
    subReddit = 'LifeProTips'
    nPosts = 1
    base_url = '../video/base_2.mp4'
    font = '../font/LTSaeada-Black.otf'
    color = 'white'
    highlight_color = 'white'
    stroke_color = 'black'
    stroke_width = 2.0

    # TODO: short content for testing
    # note: if duration audio generated from text is less then base duration, error
    content = [('short title', 'advantageous magic (potatoes) rizz, ice cream! mother??')]

    # content = get_reddit_posts(subReddit, nPosts)
    # generate_speech(content) # TODO edit if changing structure
    # create_word_level_JSON(content)
    create_video_with_subtitles(
        base_url,
        font,
        color,
        highlight_color,
        stroke_color,
        stroke_width
    )
    # clean_up()