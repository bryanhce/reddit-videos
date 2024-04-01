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
        body = summarise(body) # runs depending on the length of text
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
        print("Processing Comments from post URL:", self.post_url)
        body = {
            'thumbnail' : 'I thought she took me to the restroom to have intercourse. I was wrong.',
            'content' : ['I, a female, was about 8 years old at the time and had a new pet for 2 weeks. A goldfish named Ben in a small round aquarium. I loved him so much. My parents liked to party at our house with their friends on weekends. My uncle was always there too and he always overdid it with the alcohol. One Saturday evening I was already asleep in my bed. Suddenly I heard the door open and someone came in. I pretended to be sleeping. I thought the person would walk out again at any moment. I heard strange noises like someone was undoing their belt and taking off their pants. When I heard farting noises, loud moans and someone singing “what shall we do with the drunken sailor”, I couldn’t understand anything. The farts were getting louder and louder and I was starting to get scared. It started to smell disgusting. The person left my room again and I fell asleep at some point. The next morning I heard my mother screaming. I woke up and saw my aquarium full to the brim with shit. My goldfish Ben survived, thank God. To this day I still wonder how. It smelled like hell. We only found out it was my uncle when he did the exact same thing to my cousins spider. I still hate him to this day and whenever I hear the song “What shall we do with the drunken sailor” I get goosebumps.']
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