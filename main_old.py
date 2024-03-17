import os
from decouple import config
import praw
from gtts import gTTS


def get_posts(subR, nPosts):
    '''
    Call Reddit api to retrieve content.

    Parameters:
    subR: title of subreddit
    nPosts: number of posts to retrieve from that subreddit

    Returns:
    Tuples (title of post, description of post)
    '''
    # initialize the Reddit API wrapper
    reddit = praw.Reddit(
        client_id=config('REDDIT_CLIENT_ID'),
        client_secret=config('REDDIT_CLIENT_SECRET'),
        user_agent=config('REDDIT_USER_AGENT')
    )

    # define subreddit you want to fetch posts from
    subreddit = reddit.subreddit(subR)

    # get the top posts from the subreddit
    top_posts = subreddit.top(limit=nPosts)
    # print(type(top_posts)) # type: ListingGenerator

    arr = []
    # extract relevant fields from Submission object
    for post in top_posts:
        # print(type(post)) # type: Submission
        # print("Title:", post.title)
        # print("Text of post:", post.selftext)
        arr.append((post.title, post.selftext))
    print('Retrieved reddit content')
    return arr[0] # temporary when only getting 1 post

def tokenise(string, size):
    '''
    Splits 1 string into multiple strings of 3 words.

    Parameters:
    string: string content to be split
    size: number of words in each token

    Returns:
    Array of string of length size english words each 
    '''
    words = string.split()  
    arr = [] 

    for i in range(0, len(words), size):
        phrase = ' '.join(words[i : i + size])  
        arr.append(phrase)  

    return arr

def generate_speech(texts):
    '''
    Creates mp3 files of speech from text.

    Parameters: 
    texts : array of strings
    
    Returns:
    No output
    '''
    for i in range(len(texts)):
        # create a gTTS object
        tts = gTTS(
                text = texts[i],
                lang='en',
                tld='com.au' # change accent
            )
        tts.save('./audio/' + str(i) + ".mp3")

    print(f"Text-to-speech conversion complete")

def create_video():
    # TODO: not working
    # Load video clip
    video_clip = VideoFileClip("./video/base_1.mp4")

    # Load audio clip
    audio_clip = AudioFileClip("./audio/0.mp3")

#     # Set the duration of the audio to match the video
#     audio_clip = audio_clip.set_duration(video_clip.duration)

#     # Write the result to a file
#    final_clip.write_videofile("./video/output_video.mp4", codec="libx264", audio_codec="aac")
    
    final = video_clip.set_audio(audio_clip)
    final.write_videofile("./video/output.mp4",codec= "libx264" ,audio_codec="libmp3lame")


def generate_subtitles(subtitles):
    # subtitle_clips = []
    # for text, start_time in subtitles:
    #     end_time = start_time + 5  # Adjust this as needed
    #     sub_clip = SubtitlesClip([((start_time, end_time), text)])
    #     subtitle_clips.append(sub_clip)
    # return concatenate_videoclips(subtitle_clips)
    subtitle_clips = [SubtitlesClip(subtitles)]
    return concatenate_videoclips(subtitle_clips)

def add_subtitles():
    subtitles = [
        ((0, 4), "Subtitle 1"),          # Text, start time
        ((4, 9), "Subtitle 2"),          # Text, start time
        ((10, 14), "Subtitle 3"),         # Text, start time
    ]

    video_clip = VideoFileClip("./video/output.mp4")

    subtitle_clip = generate_subtitles(subtitles)

    final_clip = CompositeVideoClip([video_clip, subtitle_clip.set_pos(('center', 'bottom'))])

    final_clip.write_videofile("./video/video_with_subtitles.mp4", fps=video_clip.fps)

def clean_up():
    '''
    Delete mp3 files in audio
    '''
    folder_path = "audio"
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            os.remove(os.path.join(folder_path, file))

if __name__ == "__main__":
    subReddit = 'askSingapore'
    content = get_posts(subReddit, 1)
    # content_tokens = tokenise(content[1], 15)
    generate_speech([content[1]])
    # create_video()
    # add_subtitles()