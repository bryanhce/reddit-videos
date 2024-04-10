from video_edits import *
from reddit import get_reddit_posts, get_reddit_comments
from tts import generate_audio_files
from utils import clean_up
from abc import ABC, abstractmethod
from image_edits import generate_image
from summary import summarise

# code follows (pseudo) factory design pattern

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

    def sub_run(self, body):
        #summarise(body) # runs depending on the length of text
        generate_audio_files(body)
        generate_image(body['thumbnail'], self.font_url)
        create_word_level_JSON(body)
        create_video_with_subtitles(
            self.base_url,
            self.font_url,
            self.color,
            self.stroke_color,
            self.stroke_width
        )
        clean_up()

class Posts(RubiSlicesBase):
    '''
    Used to create video from multiple posts in the same subreddit.
    '''
    def __init__(self, subreddit, n, base_url, font_url, color, stroke_color, stroke_width):
        super().__init__(n, base_url, font_url, color, stroke_color, stroke_width)
        self.subreddit = subreddit

    def run(self):
        print("Processing Posts from subreddit:", self.subreddit)
        body = {
            'thumbnail' : 'subreddit name, LifeProTip',
            'content' : [('title of post', 'advantageous magic (potatoes) rizz, ice cream! mother??')]
        }
        # body = get_reddit_posts(self.subreddit, self.n)
        self.sub_run(body)

class Comments(RubiSlicesBase):
    '''
    Used to create video from multiple comments in the same post.
    '''
    def __init__(self, post_url, n, base_url, font_url, color, stroke_color, stroke_width):
        super().__init__(n, base_url, font_url, color, stroke_color, stroke_width)
        self.post_url = post_url

    def run(self):
        # print("Processing Comments from post URL:", self.post_url)
        body = {
            'thumbnail' : 'My boyfriend talks to me in my sleep',
            'content' : ['He’s a bit shy and doesn’t express love verbally when I’m awake. The other day, for some reason I decided to fake sleep. 30 minutes in, he checked to make sure I was asleep by saying “I love you”. When I didn’t respond he started humming which he never does so it made me very happy. Then he started talking. It was small at first like “you’re so cute” and “I love snuggling with you.” He then went into detail about all the things he loves about me and how happy I make him and then out of the blue said “I’m going to marry you.” I tried to contain my smile and I started tearing up. Now I fake sleep all the time to hear him talk about things he’s too scared to tell me when I’m awake. I love him.']
        }
        # body = get_reddit_comments(self.post_url, self.n)
        self.sub_run(body)

class RubiSlicesFactory:
    @staticmethod
    def create(subreddit=None, post_url=None, **kwargs):
        if subreddit and post_url:
            raise ValueError("Either subreddit or post_url is provided not both")
        elif subreddit:
            return Posts(subreddit=subreddit, **kwargs)
        elif post_url:
            return Comments(post_url=post_url, **kwargs)
        else:
            raise ValueError("Either subreddit or post_url must be provided")