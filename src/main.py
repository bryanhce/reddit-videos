from rubislices import RubiSlicesFactory

if __name__ == "__main__":
    factory = RubiSlicesFactory()

    # Parameters to change with each video
    rubiSlice = factory.create(
        ##############################
        ## either OR cannot be both ##
        # subreddit = 'LifeProTips',
        post_url='https://www.reddit.com/r/AskReddit/comments/1btvlvx/adults_who_are_married_what_small_things_that_you/',
        ##############################
        n = 3, # number of comments or posts
        base_url = '/code/video/base_1m24s.mp4',
        font_url = '/code/font/Bungee-Regular.ttf',
        color = 'white',
        stroke_color = 'black',
        stroke_width = 3.0,
    )
    rubiSlice.run()
    