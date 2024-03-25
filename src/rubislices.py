from video_edits import *
from reddit import get_reddit_posts, get_reddit_comments
from tts import generate_speech, speed_up_tts
from utils import clean_up
from abc import ABC, abstractmethod

# code follows (pseudo) factory method pattern

class RubiSlicesBase(ABC):
    '''
    Abstract parent class
    '''
    def __init__(self, n=1, base_url='', font_url='', color='', stroke_color='', stroke_width=0):
        self.n = n
        self.base_url = base_url
        self.font_url = font_url
        self.color = color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    @abstractmethod
    def run(self):
        pass

class Posts(RubiSlicesBase):
    '''
    Used to create video from multiple posts in the same subreddit.
    '''
    def __init__(self, subreddit, n, base_url, font_url, color, stroke_color, stroke_width):
        super().__init__(n, base_url, font_url, color, stroke_color, stroke_width)
        self.subreddit = subreddit

    def run(self):
        print("Processing Posts from subreddit:", self.subreddit)
        content = [('short title', 'advantageous magic (potatoes) rizz, ice cream! mother??')]
        # content = get_reddit_posts(self.subreddit, self.n)
        generate_speech(content) 
        speed_up_tts()
        create_word_level_JSON(content)
        create_video_with_subtitles(
            self.base_url,
            self.font_url,
            self.color,
            self.stroke_color,
            self.stroke_width
        )
        clean_up()

class Comments(RubiSlicesBase):
    '''
    Used to create video from multiple comments in the same post.
    '''
    def __init__(self, post_url, n, base_url, font_url, color, stroke_color, stroke_width):
        super().__init__(n, base_url, font_url, color, stroke_color, stroke_width)
        self.post_url = post_url

    def run(self):
        print("Processing Comments from post URL:", self.post_url)
        # content = ['post title', 'comment one hohoho', 'comment 2 tokyo']
        content = get_reddit_comments(self.post_url, self.n)
        generate_speech(content) 
        speed_up_tts()
        create_word_level_JSON(content)
        create_video_with_subtitles(
            self.base_url,
            self.font_url,
            self.color,
            self.stroke_color,
            self.stroke_width
        )
        clean_up()

class RubiSlicesFactory:
    @staticmethod
    def create(subreddit=None, post_url=None, **kwargs):
        if subreddit:
            return Posts(subreddit=subreddit, **kwargs)
        elif post_url:
            return Comments(post_url=post_url, **kwargs)
        else:
            raise ValueError("Either subreddit or post_url must be provided")