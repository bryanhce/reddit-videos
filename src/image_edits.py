from wand.image import Image
from wand.drawing import Drawing
from wand.font import Font

# TODO: decide if we are keeping this unused function in
def wrap_text(text, font, max_width, draw):
    '''
    Split string into array of string, where each element
    is a string which represents the text on a single line.
    '''
    lines = []
    current_line = ""
    words = text.split()
    for word in words:
        # Check if the word itself fits on the current line
        if draw.textlength(current_line + word, font=font) <= max_width:
            current_line += " " + word
        else:
        # If the word doesn't fit, check if it's longer than max_width
            if draw.textlength(word, font=font) > max_width:
            # Handle long words that wouldn't fit on any line
                raise ValueError(f"Encountered word '{word}' that is longer than max width")
            else:
            # If the word fits on a single line, start a new line with it
                lines.append(current_line.strip())
                current_line = word
    lines.append(current_line.strip())
    return lines

def generate_image(text, font_url):
    '''
    Creates thumbnail for the video.

    Parameters:
    text: string to be overlayed on the template image.
    font_url: url to font file

    Returns:
    Does not return anything but saved generated image to 
    image folder as output_image.jpg
    '''
    # for testing
    # text = """This is a very long long long title for a post, did it wrap around? 
    #     well it should have, fix it! some text to make this even longer longer!"""

    image_path = "../image/rs_caption_template.png"
    output_url = "../image/output_image.png"

    try:        
        with Image(filename=image_path) as image:
            # TODO: add to config file
            left, top = 120, 175
            width, height = image.width - (left * 2), image.height - (top * 2)
            with Drawing() as context:
                context.fill_color = 'transparent'
                context.rectangle(left=left, top=top, width=width, height=height)
                font = Font(font_url, stroke_color="pink", stroke_width=3)
                context(image)
                image.caption(text, left=left, top=top, width=width, height=height, font=font, gravity='center')
            
            # Resize image to fit video width
            # TODO: remove this function and use image of correct size
            new_width = image.width // 3 
            new_height = image.height // 3
            resized_image = image.clone()
            resized_image.resize(new_width, new_height)

            resized_image.save(filename=output_url)
            print("Image generated!")

    except Exception as e:
        print(f"An error occurred: {e}")

# # for testing
# generate_image('', '../font/Bungee-Regular.ttf')
