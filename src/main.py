from rubislices import RubiSlicesFactory

if __name__ == "__main__":
    factory = RubiSlicesFactory()

    # Parameters to change with each video
    rubiSlice = factory.create(
        # either OR
        # subreddit = 'LifeProTips',
        post_url='https://www.reddit.com/r/AskReddit/comments/147rws8/wedding_photographers_of_reddit_what_was_your',
        # cannot be both
        n = 4, # number of comments or 
        base_url = '../video/base_2m04s.mp4',
        font_url = '../font/LTSaeada-Bold.otf',
        color = 'white',
        stroke_color = 'black',
        stroke_width = 3.0,
    )
    rubiSlice.run()
    