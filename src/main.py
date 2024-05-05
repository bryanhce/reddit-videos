import json
from rubislices import RubiSlicesFactory

if __name__ == "__main__":
    with open('/code/parameters.json') as f:
        parameters = json.load(f)

    # Access individual parameters
    body = parameters.get('body')
    subreddit = parameters.get('subreddit')
    post_url = parameters.get('post_url')
    n = parameters.get('n')
    base_url = parameters.get('base_url')
    font_url = parameters.get('font_url')
    color = parameters.get('color')
    stroke_color = parameters.get('stroke_color')
    stroke_width = parameters.get('stroke_width')

    factory = RubiSlicesFactory()

    rubiSlice = factory.create(
        subreddit = subreddit,
        post_url = post_url,
        body = body,
        n = n,
        base_url = base_url,
        font_url = font_url,
        color = color,
        stroke_color = stroke_color,
        stroke_width = stroke_width,
    )
    rubiSlice.run()
    