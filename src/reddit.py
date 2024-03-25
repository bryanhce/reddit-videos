import praw
from decouple import config

def get_reddit_posts(sub_reddit, n):
    '''
    Call Reddit api to retrieve posts from a subreddit.

    Parameters:
    sub_reddit: title of subreddit
    n: number of posts to retrieve from that subreddit

    Returns:
    Array of tuples where each (title of post, description of post)
    '''
    # TODO can use singleton pattern for this, let Ritika do?
    # initialize the Reddit API wrapper
    reddit = praw.Reddit(
        client_id=config('REDDIT_CLIENT_ID'),
        client_secret=config('REDDIT_CLIENT_SECRET'),
        user_agent=config('REDDIT_USER_AGENT')
    )

    # define subreddit you want to fetch posts from
    subreddit = reddit.subreddit(sub_reddit)

    # get the top posts from the subreddit
    top_posts = subreddit.top(limit=n)

    arr = []
    # extract relevant fields from Submission object
    for post in top_posts:
        # print(type(post)) # type: Submission
        # print("Title:", post.title)
        # print("Text of post:", post.selftext)
        arr.append((post.title, post.selftext))
    print('Retrieved reddit content')
    return arr

def get_reddit_comments(url, n):
    '''
    Call Reddit api to retrieve comments from a subreddit post.

    Parameters:
    url: url of subreddit post
    n: number of comments to retrieve from that post

    Returns:
    Array with with each element being a string in the format like
    [title of post, top comment 1, top comment 2, ... top comment n]
    '''
    # initialize the Reddit API wrapper
    reddit = praw.Reddit(
        client_id=config('REDDIT_CLIENT_ID'),
        client_secret=config('REDDIT_CLIENT_SECRET'),
        user_agent=config('REDDIT_USER_AGENT')
    )

    submission = reddit.submission(url=url)

    # first element in arr is post title
    arr = [submission.title]

    submission.comments.replace_more(limit=0)

    top_level_comments = []
    for top_lvl_comment in submission.comments:
        if (top_lvl_comment.body != '[deleted]'):
            top_level_comments.append(top_lvl_comment)

    # Sorting top-level comments based on upvotes
    sorted_comments = sorted(top_level_comments, key=lambda comment: comment.score, reverse=True)

    # TODO is it wasted that we dont use more of the comments after sorting?
    # maybe we can think of a way to use those other comments

    # Selecting top n comments
    top_n_comments = [comment.body for comment in sorted_comments[0 : n]]
    arr.extend(top_n_comments)
    return arr