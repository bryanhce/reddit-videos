from rubislices import RubiSlicesFactory

if __name__ == "__main__":
    factory = RubiSlicesFactory()

    # Parameters to change with each video
    rubiSlice = factory.create(
        # either OR
        subreddit = 'LifeProTips',
        # post_url='https://www.reddit.com/r/AskReddit/comments/135y5un/when_did_you_realise_that_youre_dating_an_idiot/',
        # cannot be both
        n = 4, # number of comments or posts
        base_url = '../video/base_1m05s.mp4',
        font_url = '../font/LTSaeada-ExtraBold.otf',
        color = 'white',
        stroke_color = 'black',
        stroke_width = 3.0,
    )
    rubiSlice.run()
    