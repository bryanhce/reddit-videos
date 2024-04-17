from rubislices import RubiSlicesFactory

if __name__ == "__main__":
    factory = RubiSlicesFactory()

    # Parameters to change with each video
    rubiSlice = factory.create(
        ##############################
        ## 3 choose 1, no multiples ##
        # subreddit = 'LifeProTips',
        # post_url='https://www.reddit.com/r/AskReddit/comments/1btvlvx/adults_who_are_married_what_small_things_that_you/',
        body = {
            'thumbnail' : "What is the biggest fail date you have ever had?",
            'content' : '''
                        I met a girl in one night at a party. Long word, advantageously
                        '''
        },
        ##############################
        n = 3, # number of comments or posts
        base_url = '/code/video/base_0m13s.mp4',
        font_url = '/code/font/Bungee-Regular.ttf',
        color = 'white',
        stroke_color = 'black',
        stroke_width = 3.0,
    )
    rubiSlice.run()
    