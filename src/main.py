from rubislices import RubiSlicesFactory

if __name__ == "__main__":
    factory = RubiSlicesFactory()

    # Parameters to change with each video
    rubiSlice = factory.create(
        ##############################
        ## either OR cannot be both ##
        # subreddit = 'LifeProTips',
        post_url='https://www.reddit.com/r/AskReddit/comments/135y5un/when_did_you_realise_that_youre_dating_an_idiot/',
        ##############################
        n = 1, # number of comments or posts
        base_url = '../video/base_0m56s.mp4',
        font_url = '../font/Bungee-Regular.ttf',
        color = 'white',
        stroke_color = 'black',
        stroke_width = 3.0,
    )
    rubiSlice.run()
    