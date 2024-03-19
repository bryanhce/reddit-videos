import praw
from decouple import config

def get_reddit_posts(subR, nPosts):
    '''
    Call Reddit api to retrieve content.

    Parameters:
    subR: title of subreddit
    nPosts: number of posts to retrieve from that subreddit

    Returns:
    Array of tuples where each (title of post, description of post)
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
    return arr